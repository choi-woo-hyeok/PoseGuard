from vision.pose_detector import get_pose_data

try:
    from logic.posture_logic import detect_forward_head
except ModuleNotFoundError:
    detect_forward_head = None


def main():
    print("PoseGuard Start")

    # 1. 웹캠 실행

    # 2. pose_data 생성

    # 3. 자세 분석

    # 4. UI 출력

    # 5. 결과 저장

    # 6. 그래프 및 AI 코멘트 출력
    pose_data = get_pose_data()
    if pose_data is None:
        print("Pose not detected")
        return

    if detect_forward_head is None:
        print(pose_data)
        return

    result = detect_forward_head(pose_data)
    print(result)


if __name__ == "__main__":
    main()
