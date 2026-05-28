# PoseGuard Data Format

## pose_data 형식

```python
pose_data = {
    "left_ear": (x, y),
    "right_ear": (x, y),

    "left_shoulder": (x, y),
    "right_shoulder": (x, y),

    "neck_angle": float,

    "is_bad_posture": bool
}
```

## 데이터 설명

* left_ear / right_ear:
  사용자의 귀 좌표

* left_shoulder / right_shoulder:
  사용자의 어깨 좌표

* neck_angle:
  귀와 어깨 기준으로 계산된 목 각도

* is_bad_posture:
  거북목 여부 판단 결과
