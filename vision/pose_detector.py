from __future__ import annotations

from typing import Optional

import cv2
import mediapipe as mp


Point = tuple[int, int]
PoseData = dict[str, Point | float | bool]


class PoseDetector:
    """Extracts MediaPipe pose landmarks and converts them to pose_data."""

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        min_visibility: float = 0.5,
    ) -> None:
        self.min_visibility = min_visibility
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            model_complexity=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def close(self) -> None:
        self.pose.close()

    def process_frame(self, frame) -> tuple[object, Optional[PoseData]]:
        """Returns an annotated frame and pose_data for the current frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        result = self.pose.process(rgb_frame)
        rgb_frame.flags.writeable = True

        annotated_frame = frame.copy()
        if not result.pose_landmarks:
            return annotated_frame, None

        self.mp_drawing.draw_landmarks(
            annotated_frame,
            result.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
        )

        pose_data = self._build_pose_data(
            result.pose_landmarks.landmark,
            frame_width=frame.shape[1],
            frame_height=frame.shape[0],
        )
        return annotated_frame, pose_data

    def _build_pose_data(
        self,
        landmarks,
        frame_width: int,
        frame_height: int,
    ) -> Optional[PoseData]:
        left_ear = self._landmark_to_point(
            landmarks[self.mp_pose.PoseLandmark.LEFT_EAR],
            frame_width,
            frame_height,
        )
        right_ear = self._landmark_to_point(
            landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR],
            frame_width,
            frame_height,
        )
        left_shoulder = self._landmark_to_point(
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER],
            frame_width,
            frame_height,
        )
        right_shoulder = self._landmark_to_point(
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER],
            frame_width,
            frame_height,
        )

        if None in (left_ear, right_ear, left_shoulder, right_shoulder):
            return None

        return {
            "left_ear": left_ear,
            "right_ear": right_ear,
            "left_shoulder": left_shoulder,
            "right_shoulder": right_shoulder,
            "neck_angle": 0.0,
            "is_bad_posture": False,
        }

    def _landmark_to_point(
        self,
        landmark,
        frame_width: int,
        frame_height: int,
    ) -> Optional[Point]:
        if landmark.visibility < self.min_visibility:
            return None

        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        return x, y


def extract_pose_data(frame) -> Optional[PoseData]:
    """Convenience function for one-off pose_data extraction."""
    detector = PoseDetector()
    try:
        _, pose_data = detector.process_frame(frame)
        return pose_data
    finally:
        detector.close()

