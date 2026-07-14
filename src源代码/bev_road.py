import argparse
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np


NORMALIZED_FRAME_SIZE: Tuple[int, int] = (320, 240)
BEV_CANVAS_SIZE: Tuple[int, int] = (512, 512)

FAR_MASK_RATIO = 0.5
NEAR_MASK_RATIO = 0.90
BORDER_THICKNESS_PX = 15

DEFAULT_VIDEO = Path("obstacles.m4v")

COLOR_DILATE_KERNEL_SIZE = (5, 1)

LUMA_LOW_PERCENTILE = 5.0
LUMA_HIGH_PERCENTILE = 95.0

SAT_DILATE_KERNEL_SIZE = (11, 1)

SOBEL_SPACING = 5
SOBEL_MAG_SCALE = 4.0
EDGE_HIGH_PERCENTILE =80.0
SAT_SUPPRESSION_WEIGHT = 1.0

COMPONENT_FONT_SCALE = 0.5
COMPONENT_FONT_THICKNESS = 1

COMPONENT_COLORS = [
    (255, 64, 64),
    (64, 255, 64),
    (64, 128, 255),
    (255, 192, 64),
    (192, 64, 255),
    (64, 255, 192),
]


class BevRoad:
    def __init__(self, video_in: Path, far_mask_ratio: float):
        self.cap = cv2.VideoCapture(str(video_in))
        if not self.cap.isOpened():
            raise RuntimeError(f"无法打开视频 {video_in}")

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.far_mask_ratio = float(np.clip(far_mask_ratio, 0.0, 1.0))
        self.src_points = np.float32([
            [0.0, 0.0],
            [0.0, NORMALIZED_FRAME_SIZE[1] - 1.0],
            [NORMALIZED_FRAME_SIZE[0] - 1.0, NORMALIZED_FRAME_SIZE[1] - 1.0],
            [NORMALIZED_FRAME_SIZE[0] - 1.0, 0.0]
        ])
        self.dst_points = np.float32([
            [0.0, 0.0],
            [0.0, BEV_CANVAS_SIZE[1] - 1.0],
            [BEV_CANVAS_SIZE[0] - 1.0, BEV_CANVAS_SIZE[1] - 1.0],
            [BEV_CANVAS_SIZE[0] - 1.0, 0.0]
        ])
        self.bev_matrix = cv2.getPerspectiveTransform(self.src_points, self.dst_points)

        self.dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, COLOR_DILATE_KERNEL_SIZE)
        sobel33x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        sobel33y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        dilation = SOBEL_SPACING
        kernel_size = 3 + (3 - 1) * (dilation - 1)
        self.sobel_x_kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
        self.sobel_y_kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
        for i in range(3):
            for j in range(3):
                self.sobel_x_kernel[i * dilation, j * dilation] = sobel33x[i, j]
                self.sobel_y_kernel[i * dilation, j * dilation] = sobel33y[i, j]
        self.sobel_anchor = (kernel_size // 2, kernel_size // 2)

    def run(self) -> None:
        frame_idx = 0
        while True:
            ret, frame_orig = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame_orig, NORMALIZED_FRAME_SIZE, interpolation=cv2.INTER_AREA)
            frame = cv2.dilate(frame, self.dilate_kernel, iterations=1)

            hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
            lightness = hls[:, :, 1].astype(np.float32)
            low = np.percentile(lightness, LUMA_LOW_PERCENTILE)
            high = np.percentile(lightness, LUMA_HIGH_PERCENTILE)
            if high - low < 1:
                high = low + 1.0
            np.clip(lightness, low, high, out=lightness)
            lightness -= low
            lightness *= 255.0 / (high - low)
            hls[:, :, 1] = lightness.astype(np.uint8)
            frame = cv2.cvtColor(hls, cv2.COLOR_HLS2BGR)

            bev_frame = cv2.warpPerspective(frame, self.bev_matrix, BEV_CANVAS_SIZE, flags=cv2.INTER_LINEAR)

            # bright = np.max(bev_frame, axis=2).astype(np.float32)
            bright = bev_frame[:,:,0].astype(np.float32)
            sobel_x = cv2.filter2D(bright, -1, self.sobel_x_kernel, anchor=self.sobel_anchor, borderType=cv2.BORDER_CONSTANT)
            sobel_y = cv2.filter2D(bright, -1, self.sobel_y_kernel, anchor=self.sobel_anchor, borderType=cv2.BORDER_CONSTANT)
            sobel = cv2.magnitude(sobel_x, sobel_y)
            sobel_norm = sobel / SOBEL_MAG_SCALE

            high = float(np.percentile(sobel_norm, EDGE_HIGH_PERCENTILE))
            # if high <= 1:
            #     high = 1.0
            saturation = cv2.cvtColor(bev_frame, cv2.COLOR_BGR2HSV)[:,:,1].astype(np.float32)
            saturation = cv2.dilate(saturation, np.ones(SAT_DILATE_KERNEL_SIZE), iterations=1)
            sobel_norm -= saturation * SAT_SUPPRESSION_WEIGHT
            road_mask = (sobel_norm <= high).astype(np.uint8) * 255
            road_mask = cv2.rectangle(road_mask, (0, 0), (BEV_CANVAS_SIZE[0], BEV_CANVAS_SIZE[1]), 0, BORDER_THICKNESS_PX)
            road_mask = cv2.rectangle(
                road_mask,
                (0, int(BEV_CANVAS_SIZE[1] * NEAR_MASK_RATIO)),
                (BEV_CANVAS_SIZE[0], BEV_CANVAS_SIZE[1]),
                0,
                -1,
            )



            cutoff = int(BEV_CANVAS_SIZE[1] * self.far_mask_ratio)
            if cutoff > 0:
                road_mask[:cutoff, :] = 0

            component_vis = np.zeros_like(bev_frame)
            overlay = bev_frame.copy()
            num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(road_mask, connectivity=8)
            if num_labels > 1:
                areas = stats[1:, cv2.CC_STAT_AREA]
                order = np.argsort(-areas)
                for idx, label_offset in enumerate(order):
                    label = int(label_offset) + 1
                    color = COMPONENT_COLORS[idx % len(COMPONENT_COLORS)]
                    component_vis[labels == label] = color
                    x, y, w, h, _ = stats[label]
                    cv2.rectangle(overlay, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(
                        overlay,
                        f"{idx + 1}:{stats[label, cv2.CC_STAT_AREA]}",
                        (x, max(0, y - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        COMPONENT_FONT_SCALE,
                        color,
                        COMPONENT_FONT_THICKNESS,
                        cv2.LINE_AA,
                    )
            cv2.imshow("connected_components", component_vis)
            cv2.imshow("bev_components_overlay", overlay)
            cv2.imshow("sobel_dilated", sobel / 1024.0)

            frame_idx += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Road-only BEV preprocessing pipeline.")
    parser.add_argument("--video-in", type=Path, default=DEFAULT_VIDEO, help="输入视频文件路径")
    parser.add_argument(
        "--far-mask-ratio",
        type=float,
        default=FAR_MASK_RATIO,
        help="BEV 远处（上方）需要屏蔽的高度占比，范围[0,1]",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not args.video_in.exists():
        raise FileNotFoundError(f"Input video not found: {args.video_in}")
    BevRoad(args.video_in, args.far_mask_ratio).run()


