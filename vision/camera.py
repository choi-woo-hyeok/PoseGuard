from __future__ import annotations

import cv2

from vision.pose_detector import PoseDetector, PoseData


def run_camera(camera_index: int = 0):
    """Runs webcam capture and returns pose_data when q is pressed."""
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        raise RuntimeError("Cannot open webcam. Check camera connection or index.")

    # mediapipe로 사람몸 landmark 찾는역할
    detector = PoseDetector()
    # 마지막으로 감지된 자세 데이터 저장 변수  
    last_pose_data = None

    try:
        while True:
            success, frame = capture.read()  #프레임 읽기 성공여부(success), 실제 이미지(frame)
            if not success:  # 못읽으면 에러
                raise RuntimeError("Cannot read frame from webcam.")

            frame = cv2.flip(frame, 1)  # 화면 좌우 반전
            annotated_frame, pose_data = detector.process_frame(frame)  # 프레임1장받아서 mediapipe로 사람 landmark 찾기 -> 연결해 이미지 만들기 -> 귀/어깨 좌표 pose_data만들기
            # annotated_frame: landmark 그려진 화면 이미지, pose_data: 자세 분석에 사용할 좌표 데이터
          
            if pose_data is not None: # 자세 감지시 그데이터가 last_pose_data -> q누르면 마지막으로 감지된 자세 반환(계속 최신값으로 바뀜)
                last_pose_data = pose_data
                
                
            # 화면에 글자와 점 그리기
            _draw_pose_status(annotated_frame, pose_data)  

            # 창제목이 Poseguard - Vision 인 annotated_frame이 보임
            cv2.imshow("PoseGuard - Vision", annotated_frame)

            # 1ms 동안 키 입력 확인
            key = cv2.waitKey(1) & 0xFF

            # q 누르면 마지막 자세 반환
            if key == ord("q"):
                return last_pose_data

    # mediapipe pose 자원 정리, 웹캠 해재, OpenCV창 전부 닫기
    finally:
        detector.close()
        capture.release()
        cv2.destroyAllWindows()

# 화면에 자세 감지 상태 표시 함수(frame: 화면이미지, pose_data: 있을수도있고 없을수도 있다), 반환값이 없다(->None)
def _draw_pose_status(frame, pose_data: PoseData | None) -> None:
    if pose_data is None:  # 자세감지 X 시
        cv2.putText(
            frame,  # 글자 쓸 이미지
            "No pose detected",  # 표시할 글자
            (20, 40),  # 글자 위치 
            cv2.FONT_HERSHEY_SIMPLEX,  # 글꼴
            1.0,  # 글자 크기
            (0, 0, 255),  # 색상
            2,  # 두깨 
            cv2.LINE_AA,  # 부드러운 선
        )
        return

    _draw_tracked_points(frame, pose_data)  # 자세 감지 시: 귀와 어깨점 따로 표시하는 함수 호출

    cv2.putText(  
        frame,
        "Pose detected - press q to quit",  #라고
        (20, 40),  # 에
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

# 귀와 어깨 점을 따로 표시하는 함수 호출 
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
