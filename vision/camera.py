from __future__ import annotations

import cv2

from vision.pose_detector import PoseDetector, PoseData


def run_camera(camera_index: int = 0):
    """Runs webcam capture and returns pose_data when q is pressed."""
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        raise RuntimeError("Cannot open webcam. Check camera connection or index.")

    detector = PoseDetector()
    last_pose_data = None

    try:
        while True:
            success, frame = capture.read()
            if not success:
                raise RuntimeError("Cannot read frame from webcam.")

            frame = cv2.flip(frame, 1)
            annotated_frame, pose_data = detector.process_frame(frame)

            if pose_data is not None:
                last_pose_data = pose_data

            _draw_pose_status(annotated_frame, pose_data)

            cv2.imshow("PoseGuard - Vision", annotated_frame)

            key = cv2.waitKey(1) & 0xFF

            # q 누르면 현재까지 감지된 자세 반환
            if key == ord("q"):
                return last_pose_data

    finally:
        detector.close()
        capture.release()
        cv2.destroyAllWindows()


def _draw_pose_status(frame, pose_data: PoseData | None) -> None:
    if pose_data is None:
        cv2.putText(
            frame,
            "No pose detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        return

    _draw_tracked_points(frame, pose_data)

    cv2.putText(
        frame,
        "Pose detected - press q to quit",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"LE:{pose_data['left_ear']} RE:{pose_data['right_ear']}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        f"LS:{pose_data['left_shoulder']} RS:{pose_data['right_shoulder']}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )


def _draw_tracked_points(frame, pose_data: PoseData) -> None:
    point_styles = {
        "left_ear": ((255, 0, 0), "LE"),
        "right_ear": ((255, 0, 0), "RE"),
        "left_shoulder": ((0, 255, 255), "LS"),
        "right_shoulder": ((0, 255, 255), "RS"),
    }

    for key, (color, label) in point_styles.items():
        point = pose_data[key]
        if not isinstance(point, tuple):
            continue

        cv2.circle(frame, point, 9, color, -1)
        cv2.circle(frame, point, 12, (255, 255, 255), 2)
        cv2.putText(
            frame,
            label,
            (point[0] + 10, point[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            cv2.LINE_AA,
        )


if __name__ == "__main__":
    run_camera()
