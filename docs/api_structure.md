# PoseGuard API Structure

## vision module

### get_pose_data()

설명:
MediaPipe를 이용해 사용자의 관절 좌표를 추출한다.

반환값:
pose_data (dictionary)


예시:
{
    "neck_x": 120,
    "neck_y": 240,
    "shoulder_x": 180,
    "shoulder_y": 300
}


--------------------------------------------------


## logic module

### detect_forward_head(pose_data)

설명:
거북목 여부를 판단한다.

입력값:
pose_data

반환값:
True / False


--------------------------------------------------


## frontend module

### show_warning(message)

설명:
경고 메시지를 UI에 출력한다.


--------------------------------------------------


## backend module

### save_session_data(session_data)

설명:
세션 결과를 Firebase에 저장한다.