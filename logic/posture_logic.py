"""Posture analysis logic for PoseGuard.

The current app flow is:
1. Save a baseline pose.
2. Start measurement and press q to return the last pose_data.
3. Compare the last pose_data with the saved baseline immediately.

This module does not perform real-time 5-second detection in the current UI.
"""

import math

_baseline: dict | None = None

TURTLE_EAR_THR = 1.05
TURTLE_Y_THR = 0.95
ROUND_SH_THR = 0.95


def _dist(p1: tuple, p2: tuple) -> float:
    """Return Euclidean distance between two (x, y) points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def _avg_y(*points: tuple) -> float:
    """Return average y coordinate."""
    return sum(p[1] for p in points) / len(points)


def _avg_x(*points: tuple) -> float:
    """Return average x coordinate."""
    return sum(p[0] for p in points) / len(points)


def compute_neck_angle(pose_data: dict) -> float:
    """Compute the angle between ear center and shoulder center."""
    le = pose_data["left_ear"]
    re = pose_data["right_ear"]
    ls = pose_data["left_shoulder"]
    rs = pose_data["right_shoulder"]

    ear_mid_x = _avg_x(le, re)
    ear_mid_y = _avg_y(le, re)
    sh_mid_x = _avg_x(ls, rs)
    sh_mid_y = _avg_y(ls, rs)

    dx = ear_mid_x - sh_mid_x
    dy = sh_mid_y - ear_mid_y

    angle_rad = math.atan2(abs(dx), dy) if dy != 0 else math.pi / 2
    return round(math.degrees(angle_rad), 2)


def _compute_metrics(pose_data: dict) -> dict:
    """Convert pose_data landmarks into posture metrics."""
    le = pose_data["left_ear"]
    re = pose_data["right_ear"]
    ls = pose_data["left_shoulder"]
    rs = pose_data["right_shoulder"]

    ear_dist = _dist(le, re)
    shoulder_dist = _dist(ls, rs)
    ear_to_sh_y = _avg_y(ls, rs) - _avg_y(le, re)
    sh_ratio = shoulder_dist / ear_dist if ear_dist > 0 else 0.0

    return {
        "ear_distance": ear_dist,
        "shoulder_distance": shoulder_dist,
        "ear_to_shoulder_y": ear_to_sh_y,
        "shoulder_ratio": sh_ratio,
    }


def save_baseline(pose_data: dict) -> dict:
    """Save current pose metrics as the baseline posture."""
    global _baseline
    _baseline = _compute_metrics(pose_data)
    return _baseline


def has_baseline() -> bool:
    """Return whether baseline posture has been saved."""
    return _baseline is not None


def detect_forward_head(pose_data: dict) -> bool:
    """Detect forward head posture by comparing current metrics to baseline."""
    if not has_baseline():
        return False

    current = _compute_metrics(pose_data)
    baseline = _baseline

    ear_increased = (
        current["ear_distance"] >= baseline["ear_distance"] * TURTLE_EAR_THR
    )
    vertical_gap_decreased = (
        current["ear_to_shoulder_y"]
        <= baseline["ear_to_shoulder_y"] * TURTLE_Y_THR
    )

    return ear_increased or vertical_gap_decreased


def detect_round_shoulder(pose_data: dict) -> bool:
    """Detect rounded shoulders by comparing current metrics to baseline."""
    if not has_baseline():
        return False

    current = _compute_metrics(pose_data)
    baseline = _baseline

    shoulder_decreased = (
        current["shoulder_distance"]
        <= baseline["shoulder_distance"] * ROUND_SH_THR
    )
    ratio_decreased = (
        current["shoulder_ratio"] <= baseline["shoulder_ratio"] * ROUND_SH_THR
    )

    return shoulder_decreased or ratio_decreased


def analyze_posture(pose_data: dict) -> dict:
    """Return combined posture analysis result for UI and Gemini."""
    turtle = detect_forward_head(pose_data)
    rounded = detect_round_shoulder(pose_data)
    bad = turtle or rounded
    angle = compute_neck_angle(pose_data)

    messages = []
    if turtle:
        messages.append("거북목 감지")
    if rounded:
        messages.append("라운드숄더 감지")
    if not messages:
        messages.append("자세 양호")

    return {
        "turtle_neck": turtle,
        "round_shoulder": rounded,
        "is_bad_posture": bad,
        "neck_angle": angle,
        "message": " | ".join(messages),
    }


def get_debug_info(pose_data: dict) -> dict:
    """Return current metrics and baseline metrics for debugging."""
    if not has_baseline():
        return {"error": "기준 자세 없음"}

    current = _compute_metrics(pose_data)
    baseline = _baseline

    return {
        "ear_distance": {
            "current": round(current["ear_distance"], 2),
            "baseline": round(baseline["ear_distance"], 2),
        },
        "shoulder_distance": {
            "current": round(current["shoulder_distance"], 2),
            "baseline": round(baseline["shoulder_distance"], 2),
        },
        "ear_to_shoulder_y": {
            "current": round(current["ear_to_shoulder_y"], 2),
            "baseline": round(baseline["ear_to_shoulder_y"], 2),
        },
        "shoulder_ratio": {
            "current": round(current["shoulder_ratio"], 4),
            "baseline": round(baseline["shoulder_ratio"], 4),
        },
    }


if __name__ == "__main__":
    baseline_pose = {
        "left_ear": (40, 20),
        "right_ear": (60, 20),
        "left_shoulder": (35, 50),
        "right_shoulder": (65, 50),
        "neck_angle": 0.0,
        "is_bad_posture": False,
    }
    print("baseline:", save_baseline(baseline_pose))

    turtle_pose = {
        "left_ear": (35, 27),
        "right_ear": (65, 27),
        "left_shoulder": (35, 50),
        "right_shoulder": (65, 50),
        "neck_angle": 0.0,
        "is_bad_posture": False,
    }
    print("analyze_posture:", analyze_posture(turtle_pose))
    print("debug_info:", get_debug_info(turtle_pose))
