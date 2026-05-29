from vision.pose_detector import get_pose_data
from logic.posture_logic import detect_forward_head

def main():

    pose_data = get_pose_data()

    result = detect_forward_head(pose_data)

    print(result)


if __name__ == "__main__":
    main()