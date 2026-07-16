import argparse, cv2, json, threading, time, serial
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List, Optional, Any
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto

# --- 1. 领域模型与配置 (SSOT) ---

NORMALIZED_SIZE = (320, 240)
PROCESS_SIZE = (512, 512)
CONFIG_FILE = Path(__file__).with_name("serial_config.json")

class DriveState(Enum):
    NORMAL = auto()
    BRAKING = auto()
    PAUSED = auto()
    REVERSING = auto()
    POST_REVERSE_PAUSE = auto()

@dataclass(frozen=True)
class BeaconStrategy:
    target_x_near: float
    target_x_far: float
    target_gamma: float
    base_gain: float
    gain_y_start: float
    gain_y_end: float
    max_steer: float = 1.0

@dataclass
class ControlProfile:
    name: str
    roi_side: str
    polarity: float
    strategies: Dict[str, BeaconStrategy]
    beacon_gain: float = 1.0
    lane_gain: float = 1.0
    lane_roi_w_ratio: float = 0.25
    lane_roi_h_ratio: float = 0.7
    lane_density_high: float = 0.5
    lane_density_low: float = 0.1
    # 减速区与油门控制
    decel_zone_y_start: float = 0.6
    decel_zone_y_end: float = 0.75
    decel_avoid_thresh: float = 0.8
    decel_warn_thresh: float = 0.5
    # 信标避障增强（共享减速区域）
    beacon_avoid_h_dist_thresh: float = 0.1

# --- 策略实例定义 ---

HSV_RANGES = {
    'RED': [
        (np.array([0, 100, 60]), np.array([5, 255, 255])),
        (np.array([170, 100, 60]), np.array([180, 255, 255]))
    ],
    'GREEN': [
        (np.array([40, 100, 60]), np.array([85, 255, 255]))
    ]
}

PROFILE_CW = ControlProfile(
    name="CW", 
    roi_side='RIGHT', 
    polarity=-1.0,
    strategies={
        'RED':   BeaconStrategy(target_x_near=0.0, target_x_far=0.25, target_gamma=0.25, base_gain=2.0, gain_y_start=0.1, gain_y_end=0.5),
        'GREEN': BeaconStrategy(target_x_near=1, target_x_far=0.8, target_gamma=0.25, base_gain=4.0, gain_y_start=0, gain_y_end=0)
    },
    beacon_gain=2.0,
    lane_gain=1.0,
    decel_zone_y_start=0.6,
    decel_zone_y_end=0.75,
    decel_avoid_thresh=0.8,
    decel_warn_thresh=0.5,
    beacon_avoid_h_dist_thresh=0.3
)

PROFILE_CCW = ControlProfile(
    name="CCW", 
    roi_side='LEFT', 
    polarity=1.0,
    strategies={
        'RED':   BeaconStrategy(target_x_near=0.0, target_x_far=0.5, target_gamma=0.25, base_gain=4.0, gain_y_start=0, gain_y_end=0),
        'GREEN': BeaconStrategy(target_x_near=1, target_x_far=0.8, target_gamma=0.25, base_gain=2.0, gain_y_start=0.1, gain_y_end=0.5)
    },
    beacon_gain=2.0,
    lane_gain=1.0,
    decel_zone_y_start=0.6,
    decel_zone_y_end=0.75,
    decel_avoid_thresh=0.8,
    decel_warn_thresh=0.5,
    beacon_avoid_h_dist_thresh=0.3
)

# --- 2. 硬件抽象层 (IO) ---
class VehicleIO:
    def __init__(self):
        self.config = self._load_config()
        self.ser: Optional[serial.Serial] = None
        self.current_steer = 0
        self.current_speed = 0
        # 安全默认值：程序启动后保持停车，必须由明确操作设置速度。
        self.target_speed = 0
        self.running = True
        self.switch_command: Optional[str] = None
        self._init_serial()
        threading.Thread(target=self._io_loop, daemon=True).start()

    def _load_config(self) -> dict:
        if not CONFIG_FILE.exists():
            print(f"ℹ️ Serial config not found: {CONFIG_FILE}; using safe defaults")
            return {"port": "COM3", "baudrate": 115200}
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"⚠️ Invalid serial config: {exc}; using safe defaults")
            return {"port": "COM3", "baudrate": 115200}

    def _init_serial(self):
        try: 
            self.ser = serial.Serial(
                self.config.get('port', 'COM3'), 
                self.config.get('baudrate', 115200), 
                timeout=0.1
            )
        except Exception as e: print(f"⚠️ Serial Error: {e}")

    def _io_loop(self):
        while self.running:
            if self.ser and self.ser.is_open:
                try:
                    cmd_str = f"{self.current_steer},{self.current_speed}\n"
                    self.ser.write(cmd_str.encode())
                    if self.ser.in_waiting:
                        line = self.ser.readline().decode(errors='ignore').strip()
                        if line in ["CW", "CCW"]: self.switch_command = line
                except Exception: pass
            time.sleep(0.05)
    
    def stop(self):
        self.current_steer = 0
        self.current_speed = 0
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(b"0,0\n")
                self.ser.flush()
            except Exception as exc:
                print(f"⚠️ Failed to send final stop command: {exc}")
        self.running = False
        if self.ser:
            self.ser.close()

    def set_control(self, steer: float, speed: int):
        self.current_steer = int(np.clip(steer * 100, -100, 100))
        self.current_speed = int(np.clip(speed, -100, 100))

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEWHEEL:
            delta = 5 if flags > 0 else -5
            self.target_speed = np.clip(self.target_speed + delta, -100, 100)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.target_speed = 0
            self.current_speed = 0
            print("🛑 EMERGENCY STOP (User)")

# --- 3. 核心自动驾驶逻辑 (Autopilot) ---
class Autopilot:
    def __init__(self, video_source: Optional[str], profile: ControlProfile):
        src = int(video_source) if (video_source and video_source.isdigit()) else (video_source or 0)
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise RuntimeError(f"Unable to open video source: {src}")
        self.profile = profile
        self.io = VehicleIO()
        
        self.reference_color = np.array([128, 128, 128.0])
        self.color_history = deque(maxlen=120)
        
        self.drive_state = DriveState.NORMAL
        self.state_start_time = 0.0
        self.obs_hits_counter = 0
        self.last_steer_value = 0.0
        self.saved_cruise_speed = 0
        
        self.emergency_cfg = {
            'brake_duration': 0.1,
            'pause_duration': 0.2,
            'reverse_duration': 0.4, 
            'reverse_speed': -100, 
            'min_hits': 3, 
            'beacon_bottom_limit': 0.7,
            'beacon_center_width': 0.4
        }

    def _process_vision_layer(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        h, w = frame.shape[:2]
        # 裁剪顶部干扰区域
        cropped = cv2.resize(frame[int(h*0.1):, :], PROCESS_SIZE)
        
        # 动态参考色自适应
        roi_h, roi_w = PROCESS_SIZE
        sample_pixels = cropped[int(roi_h*0.8):, int(roi_w*0.3):int(roi_w*0.7)].reshape(-1, 3)
        if len(sample_pixels) > 50:
            self.color_history.append(np.median(sample_pixels, axis=0))
            self.reference_color = np.median(self.color_history, axis=0)
        
        # 颜色距离计算
        diff_map = np.linalg.norm(cropped.astype(np.float32) - self.reference_color, axis=2)
        is_brighter = np.mean(cropped, axis=2) >= np.mean(self.reference_color)
        diff_map[is_brighter] = 0 
        
        return cropped, diff_map

    def _find_beacons(self, hsv_image: np.ndarray) -> List[Dict[str, Any]]:
        detected_targets = []
        h, w = hsv_image.shape[:2]
        min_area = 800
        solidity_threshold = 0.5
        
        for color_name, ranges in HSV_RANGES.items():
            mask = np.zeros((h, w), dtype=np.uint8)
            for lower, upper in ranges: 
                mask |= cv2.inRange(hsv_image, lower, upper)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < min_area: continue
                x, y, bw, bh = cv2.boundingRect(cnt)

                if not (solidity_threshold < area/ (bw * bh) < 1): continue
                
                aspect_ratio = bw / float(bh)
                if aspect_ratio >= 2.5: continue 
                
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    detected_targets.append({
                        'color': color_name, 
                        'center_x': int(M["m10"]/M["m00"]), 
                        'center_y': int(M["m01"]/M["m00"]), 
                        'bbox': (x, y, bw, bh), 
                        'area': area
                    })
        return detected_targets

    def _calculate_control_signals(self, dist_map: np.ndarray, targets: List[Dict]) -> Tuple[float, float, bool, Dict]:
        h, w = dist_map.shape
        debug_info = {'targets': [], 'lane': None, 'signals': {}, 'decel_zone': {}}
        em = self.emergency_cfg
        p = self.profile
        has_obstacle_risk = False
        
        # --- 1. 减速区与油门控制 ---
        y_start_px = int(h * p.decel_zone_y_start)
        y_end_px = int(h * p.decel_zone_y_end)
        decel_roi = dist_map[y_start_px:y_end_px, :]
        
        decel_density = (np.sum(decel_roi) / 255.0) / max(1, decel_roi.size)
        
        if decel_density > p.decel_avoid_thresh:
            has_obstacle_risk = True
            throttle_factor = 0.0
            zone_state = 'AVOID'
        elif decel_density > p.decel_warn_thresh:
            throttle_factor = 1.0 - (decel_density - p.decel_warn_thresh) / (p.decel_avoid_thresh - p.decel_warn_thresh)
            zone_state = 'DECEL'
        else:
            throttle_factor = 1.0
            zone_state = 'NORMAL'
        
        debug_info['decel_zone'] = {
            'rect': (0, y_start_px, w, y_end_px - y_start_px),
            'density': decel_density,
            'throttle_factor': throttle_factor,
            'state': zone_state
        }

        # --- 2. 信标策略：最近优先 (Nearest Beacon Priority) ---
        beacon_steer = 0.0
        nearest_beacon = None
        beacon_out_of_range = False  # 新增：跟踪beacon是否"拐不过去"
        
        # 选择面积最大（最近）的信标
        for t in targets:
            # 避障检测
            is_bottom_center = (t['center_y'] > h * em['beacon_bottom_limit']) and \
                               (abs(t['center_x'] - w/2) < w * em['beacon_center_width'] / 2)
            has_obstacle_risk |= is_bottom_center
            
            # 增强的信标避障逻辑：在统一的减速区域ROI内判断
            roi_y1 = p.decel_zone_y_start
            roi_y2 = p.decel_zone_y_end
            t['in_roi'] = False  # 标记beacon是否在ROI内
            t['h_dist'] = 0.0    # 记录水平距离
            if roi_y1 <= (t['center_y'] / h) <= roi_y2:
                t['in_roi'] = True
                strategy = self.profile.strategies.get(t['color'])
                if strategy:
                    y_ratio = t['center_y'] / h
                    gamma_ratio = np.power(y_ratio, strategy.target_gamma)
                    target_x = strategy.target_x_far + (strategy.target_x_near - strategy.target_x_far) * gamma_ratio
                    h_dist = abs(target_x - (t['center_x'] / w))
                    t['h_dist'] = h_dist
                    if h_dist > p.beacon_avoid_h_dist_thresh:
                        has_obstacle_risk |= True
                        beacon_out_of_range = True
            
            strategy = self.profile.strategies.get(t['color'])
            if not strategy: continue
            
            # 计算转向力
            y_ratio = t['center_y'] / h
            gamma_ratio = np.power(y_ratio, strategy.target_gamma)
            target_x = strategy.target_x_far + (strategy.target_x_near - strategy.target_x_far) * gamma_ratio
            error_x = target_x - (t['center_x'] / w)
            
            gain = 0.0
            if y_ratio >= strategy.gain_y_end:
                gain = strategy.base_gain
            elif y_ratio >= strategy.gain_y_start:
                denominator = strategy.gain_y_end - strategy.gain_y_start
                if denominator > 0:
                    gain = strategy.base_gain * ((y_ratio - strategy.gain_y_start) / denominator)
            
            steer_force = np.clip(-error_x * gain, -strategy.max_steer, strategy.max_steer)
            
            t_info = {**t, 'steer_force': steer_force, 'target_x': target_x}
            debug_info['targets'].append(t_info)
            
            # 选择面积最大的信标作为主导信标
            if nearest_beacon is None or t['area'] > nearest_beacon['area']:
                nearest_beacon = t_info
                beacon_steer = steer_force

        # --- 3. 车道保持策略 (Lane Strategy) ---
        lane_w = int(w * self.profile.lane_roi_w_ratio)
        lane_h = int(h * self.profile.lane_roi_h_ratio)
        lane_x_start = (w - lane_w) if self.profile.roi_side == 'RIGHT' else 0
        lane_roi = dist_map[h - lane_h:, lane_x_start : lane_x_start + lane_w]
        
        lane_density = (np.sum(lane_roi) / 255.0) / max(1, lane_roi.size)
        
        lane_steer = 0.0
        if lane_density > self.profile.lane_density_high:
            lane_steer = 1.0 * self.profile.polarity
        elif lane_density < self.profile.lane_density_low:
            lane_steer = -1.0 * self.profile.polarity
        else:
            norm_val = (lane_density - self.profile.lane_density_low) / (self.profile.lane_density_high - self.profile.lane_density_low)
            lane_steer = (2.0 * norm_val - 1.0) * self.profile.polarity

        debug_info['lane'] = {
            'rect': (lane_x_start, h - lane_h, lane_w, lane_h),
            'density': lane_density
        }
        
        # --- 4. 直接叠加 (Direct Superposition) ---
        final_steer = np.clip(
            self.profile.beacon_gain * beacon_steer + self.profile.lane_gain * lane_steer,
            -1.0, 1.0
        )
        
        # 记录信号数据用于可视化
        debug_info['signals'] = {
            'beacon_val': beacon_steer,
            'beacon_gain': self.profile.beacon_gain,
            'lane_val': lane_steer,
            'lane_gain': self.profile.lane_gain,
            'final_val': final_steer,
            'nearest_beacon': nearest_beacon,
            'beacon_out_of_range': beacon_out_of_range
        }
        
        return final_steer, throttle_factor, has_obstacle_risk, debug_info

    def run(self):
        cv2.namedWindow("Dashboard")
        cv2.setMouseCallback("Dashboard", self.io.mouse_callback)
        print(f"🚀 System Start. Initial Mode: {self.profile.name}")
        
        try:
            while True:
                if new_cmd := self.io.switch_command:
                    self.io.switch_command = None
                    new_profile = PROFILE_CW if new_cmd == "CW" else PROFILE_CCW
                    if new_profile != self.profile:
                        self.profile = new_profile
                        self.obs_hits_counter = 0
                        print(f"🔄 MODE SWITCHED: {new_cmd}")

                ret, frame = self.cap.read()
                if not ret:
                    self.io.set_control(0, 0)
                    print("⚠️ Video source lost; stopping vehicle output")
                    break
                
                # 视觉处理
                processed_img, dist_map = self._process_vision_layer(cv2.resize(frame, NORMALIZED_SIZE))
                hsv_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2HSV)
                targets = self._find_beacons(hsv_img)
                
                # 决策计算
                calc_steer, throttle, obs_risk, debug_data = self._calculate_control_signals(dist_map, targets)

                # 状态机管理
                self.obs_hits_counter = (self.obs_hits_counter + 1) if obs_risk else 0 
                is_confirmed_risk = (self.obs_hits_counter >= self.emergency_cfg['min_hits'])
                
                current_time = time.time()
                
                if self.drive_state == DriveState.NORMAL:
                    if is_confirmed_risk:
                        self.drive_state = DriveState.BRAKING
                        self.state_start_time = current_time
                        self.last_steer_value = calc_steer
                        self.saved_cruise_speed = self.io.target_speed
                        self.io.set_control(0, 0)
                        print(f"⚠️ EMERGENCY: Obstacle Detected -> BRAKING")
                    else:
                        self.io.set_control(calc_steer, self.io.target_speed * throttle)
                
                elif self.drive_state == DriveState.BRAKING:
                    if current_time - self.state_start_time > self.emergency_cfg['brake_duration']:
                        self.drive_state = DriveState.PAUSED
                        self.state_start_time = current_time
                        self.io.set_control(0, 0)
                        print(f"🔄 BRAKING -> PAUSED (Steering Reset)")
                
                elif self.drive_state == DriveState.PAUSED:
                    if current_time - self.state_start_time > self.emergency_cfg['pause_duration']:
                        self.drive_state = DriveState.REVERSING
                        self.state_start_time = current_time
                        self.io.set_control(0, self.emergency_cfg['reverse_speed'])
                        print(f"⬅️ PAUSED -> REVERSING")
                
                elif self.drive_state == DriveState.REVERSING:
                    if current_time - self.state_start_time > self.emergency_cfg['reverse_duration']:
                        self.drive_state = DriveState.POST_REVERSE_PAUSE
                        self.state_start_time = current_time
                        self.io.set_control(calc_steer, 0)
                        print("🔄 REVERSING -> POST_REVERSE_PAUSE (Steering Reset)")
                
                elif self.drive_state == DriveState.POST_REVERSE_PAUSE:
                    self.io.set_control(calc_steer, 0)
                    if current_time - self.state_start_time > self.emergency_cfg['pause_duration']:
                        self.drive_state = DriveState.NORMAL
                        self.obs_hits_counter = 0
                        self.io.set_control(calc_steer, self.saved_cruise_speed)
                        print("✅ POST_REVERSE_PAUSE -> NORMAL (Recovery Complete)")

                final_vis = self._draw_dashboard(dist_map, debug_data)

                # 如果处于避障状态 (REVERSING 或 PAUSED)，绘制红色外框
                if self.drive_state != DriveState.NORMAL:
                    h, w = final_vis.shape[:2]
                    cv2.rectangle(final_vis, (0, 0), (w-1, h-1), (0, 0, 255), 5) # 红色，5像素宽

                cv2.imshow("Dashboard", final_vis)
                if cv2.waitKey(1) & 0xFF == ord('q'): break
        finally:
            self.io.stop()
            self.cap.release()
            cv2.destroyAllWindows()

    def _draw_dashboard(self, dist_map, debug):
        # 1. 基础图像
        base_h, base_w = dist_map.shape
        vis = cv2.cvtColor((np.clip(dist_map, 0, 100) * 2.55).astype(np.uint8), cv2.COLOR_GRAY2BGR)
        
        # 2. 绘制减速区和车道ROI
        # 减速区（增强可视化）
        dz_info = debug['decel_zone']
        dz_x, dz_y, dz_w, dz_h = dz_info['rect']
        zone_state = dz_info['state']
        density = dz_info['density']
        throttle_factor = dz_info['throttle_factor']
        
        # 根据状态选择颜色
        state_colors = {
            'NORMAL': (0, 255, 0),    # 绿色
            'DECEL': (0, 255, 255),   # 黄色
            'AVOID': (0, 0, 255)      # 红色
        }
        border_color = state_colors.get(zone_state, (128, 128, 128))
        
        # 绘制ROI边框（加粗以突出显示）
        cv2.rectangle(vis, (dz_x, dz_y), (dz_x + dz_w, dz_y + dz_h), border_color, 2)
        
        # 绘制占用比例填充（从底部向上填充）
        fill_h = int(dz_h * density)
        if fill_h > 0:
            # 使用半透明效果
            overlay = vis.copy()
            cv2.rectangle(overlay, (dz_x, dz_y + dz_h - fill_h), (dz_x + dz_w, dz_y + dz_h), border_color, -1)
            cv2.addWeighted(overlay, 0.3, vis, 0.7, 0, vis)
        
        # 显示状态文本
        status_text = f"{zone_state} D:{density:.2f} T:{throttle_factor:.2f}"
        cv2.putText(vis, status_text, (dz_x + 5, dz_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, border_color, 1)
        
        # 如果beacon超出阈值，显示警告
        if debug['signals'].get('beacon_out_of_range', False):
            cv2.putText(vis, "BEACON OUT!", (dz_x + 5, dz_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)

        # 车道ROI
        l_info = debug['lane']
        lx, ly, lw, lh = l_info['rect']
        cv2.rectangle(vis, (lx, ly), (lx+lw, ly+lh), (0, 255, 255), 1)
        fill_h = int(lh * l_info['density'])
        # 填充车道密度指示条（实心）
        cv2.rectangle(vis, (lx, ly + lh - fill_h), (lx+lw, ly+lh), (0, 255, 0), -1)
        
        # 3. 绘制动态目标线和信标
        # 先画Gamma曲线
        for color_name, strategy in self.profile.strategies.items():
            line_color = (0, 255, 0) if color_name == 'GREEN' else (0, 0, 255)
            points = []
            for y_px in range(0, base_h, 5):  # 每5个像素采样一次点
                y_ratio = y_px / base_h
                gamma_ratio = np.power(y_ratio, strategy.target_gamma)
                target_x = strategy.target_x_far + (strategy.target_x_near - strategy.target_x_far) * gamma_ratio
                x_px = int(target_x * base_w)
                points.append((x_px, y_px))
            
            # 绘制平滑曲线
            for i in range(len(points) - 1):
                cv2.line(vis, points[i], points[i+1], line_color, 1, cv2.LINE_AA)

        # 再画信标和它的瞬时目标点
        signals = debug['signals']
        nearest = signals.get('nearest_beacon')
        
        for t in debug['targets']:
            color = (0, 255, 0) if t['color'] == 'GREEN' else (0, 0, 255)
            x, y, w, h = t['bbox']
            
            # 如果beacon超出阈值，使用红色边框警告
            if t.get('in_roi', False) and t.get('h_dist', 0) > self.profile.beacon_avoid_h_dist_thresh:
                box_color = (0, 0, 255)  # 红色警告
                thickness = 3
            else:
                # 高亮最近信标
                thickness = 3 if (nearest and t['center_x'] == nearest['center_x'] and t['center_y'] == nearest['center_y']) else 1
                box_color = color
            
            cv2.rectangle(vis, (x, y), (x+w, y+h), box_color, thickness)
            
            # 显示转向力和状态
            status_line = f"F:{t['steer_force']:.2f}"
            if t.get('in_roi', False):
                status_line += f" D:{t.get('h_dist', 0):.2f}"
            cv2.putText(vis, status_line, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, box_color, 1)
            
            # 绘制从信标中心到其动态目标点的连线
            target_px = int(t['target_x'] * base_w)
            cv2.line(vis, (t['center_x'], t['center_y']), (target_px, t['center_y']), color, 1)
            cv2.circle(vis, (target_px, t['center_y']), 4, color, -1)

        # --- 4. 底部 Steering Monitor (独立信号叠加可视化) ---
        panel_h = 80
        panel = np.zeros((panel_h, base_w, 3), dtype=np.uint8)
        
        cx = base_w // 2
        bar_max_w = int(base_w * 0.45)
        
        # 辅助函数：绘制条形图
        def draw_bar(y_off, val, label, color, gain=None):
            cv2.line(panel, (cx, y_off), (cx, y_off+14), (100, 100, 100), 1)
            bar_len = int(val * bar_max_w)
            pt1 = (cx, y_off + 2)
            pt2 = (cx + bar_len, y_off + 12)
            cv2.rectangle(panel, pt1, pt2, color, -1)
            
            gain_txt = f"x{gain:.1f}" if gain else ""
            txt = f"{label}: {val:.2f} {gain_txt}"
            t_x = 5 if val >= 0 else base_w - 120
            cv2.putText(panel, txt, (t_x, y_off + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)

        # A. 信标信号 (青色) - 独立清晰
        draw_bar(5, signals['beacon_val'], "BEAC", (255, 255, 0), signals['beacon_gain'])
        
        # B. 车道信号 (黄色) - 独立清晰
        draw_bar(25, signals['lane_val'], "LANE", (0, 255, 255), signals['lane_gain'])
        
        # C. 叠加结果 (紫色)
        draw_bar(45, signals['final_val'], "SUMM", (255, 0, 255))
        
        # 信号说明
        mode_txt = f"Mode: {self.profile.name} | Strategy: Direct Superposition"
        cv2.putText(panel, mode_txt, (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)

        # 拼接画布
        final_vis = np.vstack([vis, panel])
        
        # 状态叠加
        status = f"[{self.profile.name}] State:{self.drive_state.name} Speed:{self.io.current_speed}"
        cv2.putText(final_vis, status, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return final_vis

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--video-in", type=str, help="Video file path or camera index")
    p.add_argument("--mode", default="cw", choices=["cw", "ccw"])
    args = p.parse_args()
    
    initial_profile = PROFILE_CCW if args.mode == "ccw" else PROFILE_CW
    Autopilot(args.video_in, initial_profile).run()
