"""
logic/posture_logic.py - 원준혁 담당 (logic 브랜치)

역할:
  - 기준 자세 저장
  - 거북목 / 라운드숄더 판단 로직
  - 5초 지속 감지 구현
  - Gemini 연동 준비 (detect_forward_head 반환값으로 UI/backend에 전달)

pose_data 형식 (data_format.md 기준):
  {
      "left_ear":       (x, y),
      "right_ear":      (x, y),
      "left_shoulder":  (x, y),
      "right_shoulder": (x, y),
      "neck_angle":     float,
      "is_bad_posture": bool      ← 이 모듈에서 채워서 반환
  }

주요 공개 함수:
  detect_forward_head(pose_data) -> bool   # main.py / api_structure.md 기준
  save_baseline(pose_data)                 # UI에서 기준 자세 저장 버튼 클릭 시 호출
  analyze_posture(pose_data)  -> dict      # 거북목 + 라운드숄더 + 메시지 통합 반환
"""

import math
import time

# ──────────────────────────────────────────
# 전역 상태 (기준 자세 & 타이머)
# ──────────────────────────────────────────

_baseline: dict | None = None          # 기준 자세 측정값
_turtle_start: float | None = None     # 거북목 이상 감지 시작 시각
_round_start:  float | None = None     # 라운드숄더 이상 감지 시작 시각

ALERT_DURATION   = 5.0   # 이상 자세 지속 판단 시간 (초)
TURTLE_EAR_THR   = 1.10  # ear_distance 기준 대비 증가 비율 임계값 (10% 이상)
TURTLE_Y_THR     = 0.90  # ear_to_shoulder_y 기준 대비 감소 비율 임계값 (10% 이하)
ROUND_SH_THR     = 0.90  # shoulder_distance 기준 대비 감소 비율 임계값 (10% 이하)


# ──────────────────────────────────────────
# 내부 유틸
# ──────────────────────────────────────────

def _dist(p1: tuple, p2: tuple) -> float:
    """두 (x, y) 튜플 사이의 유클리드 거리"""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def _avg_y(*points: tuple) -> float:
    """여러 (x, y) 튜플의 y 좌표 평균"""
    return sum(p[1] for p in points) / len(points)

def _avg_x(*points: tuple) -> float:
    """여러 (x, y) 튜플의 x 좌표 평균"""
    return sum(p[0] for p in points) / len(points)

def compute_neck_angle(pose_data: dict) -> float:
    """
    귀와 어깨 기준으로 목 각도 계산 (data_format.md 기준).

    - 귀 중점 → 어깨 중점을 잇는 벡터와 수직선(위쪽) 사이의 각도
    - 정자세일수록 0°에 가깝고, 거북목일수록 각도가 커짐
    - 반환값: 도(degree), 0.0 ~ 90.0
    """
    le = pose_data["left_ear"]
    re = pose_data["right_ear"]
    ls = pose_data["left_shoulder"]
    rs = pose_data["right_shoulder"]

    ear_mid_x = _avg_x(le, re)
    ear_mid_y = _avg_y(le, re)
    sh_mid_x  = _avg_x(ls, rs)
    sh_mid_y  = _avg_y(ls, rs)

    # 어깨 → 귀 방향 벡터
    dx = ear_mid_x - sh_mid_x
    dy = sh_mid_y  - ear_mid_y   # y축 반전 (화면 좌표계: 아래가 +)

    # 수직선(위 방향)과의 각도
    angle_rad = math.atan2(abs(dx), dy) if dy != 0 else math.pi / 2
    return round(math.degrees(angle_rad), 2)

def _compute_metrics(pose_data: dict) -> dict:
    """
    pose_data에서 측정값 계산.

    반환:
        ear_distance        : 왼쪽 귀 ↔ 오른쪽 귀 거리
        shoulder_distance   : 왼쪽 어깨 ↔ 오른쪽 어깨 거리
        ear_to_shoulder_y   : 어깨 평균 y - 귀 평균 y  (클수록 귀가 어깨에서 멀다)
        shoulder_ratio      : shoulder_distance / ear_distance
    """
    le = pose_data["left_ear"]
    re = pose_data["right_ear"]
    ls = pose_data["left_shoulder"]
    rs = pose_data["right_shoulder"]

    ear_dist      = _dist(le, re)
    shoulder_dist = _dist(ls, rs)
    ear_to_sh_y   = _avg_y(ls, rs) - _avg_y(le, re)
    sh_ratio      = shoulder_dist / ear_dist if ear_dist > 0 else 0.0

    return {
        "ear_distance":      ear_dist,
        "shoulder_distance": shoulder_dist,
        "ear_to_shoulder_y": ear_to_sh_y,
        "shoulder_ratio":    sh_ratio,
    }


# ──────────────────────────────────────────
# 공개 API
# ──────────────────────────────────────────

def save_baseline(pose_data: dict) -> dict:
    """
    현재 pose_data를 기준 자세로 저장.
    UI에서 '기준 자세 저장' 버튼 클릭 시 호출.

    반환: 저장된 baseline 측정값 딕셔너리 (로깅/디버그용)
    """
    global _baseline, _turtle_start, _round_start
    _baseline      = _compute_metrics(pose_data)
    _turtle_start  = None
    _round_start   = None
    return _baseline

def has_baseline() -> bool:
    """기준 자세가 저장되어 있으면 True"""
    return _baseline is not None


def detect_forward_head(pose_data: dict) -> bool:
    """
    거북목 여부 판단 (main.py / api_structure.md 기준 함수).

    기준 자세 미저장 시 False 반환.
    거북목 조건이 ALERT_DURATION 초 이상 지속되면 True 반환.

    거북목 판단 기준 (최준수 제안):
      1. ear_distance >= baseline * TURTLE_EAR_THR  (귀 간격 증가)
      2. ear_to_shoulder_y <= baseline * TURTLE_Y_THR  (귀-어깨 y 거리 감소)
    """
    global _turtle_start

    if not has_baseline():
        return False

    m   = _compute_metrics(pose_data)
    b   = _baseline
    now = time.time()

    cond1 = m["ear_distance"]      >= b["ear_distance"]      * TURTLE_EAR_THR
    cond2 = m["ear_to_shoulder_y"] <= b["ear_to_shoulder_y"] * TURTLE_Y_THR

    if cond1 and cond2:
        if _turtle_start is None:
            _turtle_start = now
        elif now - _turtle_start >= ALERT_DURATION:
            return True
    else:
        _turtle_start = None

    return False


def detect_round_shoulder(pose_data: dict) -> bool:
    """
    라운드숄더 여부 판단.

    기준 자세 미저장 시 False 반환.
    라운드숄더 조건이 ALERT_DURATION 초 이상 지속되면 True 반환.

    라운드숄더 판단 기준 (최준수 제안):
      1. shoulder_distance <= baseline * ROUND_SH_THR  (어깨 간격 감소)
      2. shoulder_ratio    <= baseline shoulder_ratio * ROUND_SH_THR  (어깨/귀 비율 감소)
    """
    global _round_start

    if not has_baseline():
        return False

    m   = _compute_metrics(pose_data)
    b   = _baseline
    now = time.time()

    cond1 = m["shoulder_distance"] <= b["shoulder_distance"] * ROUND_SH_THR
    cond2 = m["shoulder_ratio"]    <= b["shoulder_ratio"]    * ROUND_SH_THR

    if cond1 and cond2:
        if _round_start is None:
            _round_start = now
        elif now - _round_start >= ALERT_DURATION:
            return True
    else:
        _round_start = None

    return False


def analyze_posture(pose_data: dict) -> dict:
    """
    거북목 + 라운드숄더 통합 분석. UI / Gemini 연동에 활용.

    반환:
        {
            "turtle_neck":    bool,
            "round_shoulder": bool,
            "is_bad_posture": bool,   # 둘 중 하나라도 True면 True
            "neck_angle":     float,  # 목 각도 (도)
            "message":        str     # UI 표시용 메시지
        }
    """
    turtle  = detect_forward_head(pose_data)
    rounded = detect_round_shoulder(pose_data)
    bad     = turtle or rounded
    angle   = compute_neck_angle(pose_data)

    messages = []
    if turtle:
        messages.append("⚠️ 거북목 감지됨")
    if rounded:
        messages.append("⚠️ 라운드숄더 감지됨")
    if not messages:
        messages.append("✅ 자세 양호")

    return {
        "turtle_neck":    turtle,
        "round_shoulder": rounded,
        "is_bad_posture": bad,
        "neck_angle":     angle,
        "message":        " | ".join(messages),
    }


def get_debug_info(pose_data: dict) -> dict:
    """현재 측정값 vs 기준값 비교 (개발/디버그용)"""
    if not has_baseline():
        return {"error": "기준 자세 없음"}

    m = _compute_metrics(pose_data)
    b = _baseline
    now = time.time()

    return {
        "ear_distance":         {"current": round(m["ear_distance"], 2),      "baseline": round(b["ear_distance"], 2)},
        "shoulder_distance":    {"current": round(m["shoulder_distance"], 2), "baseline": round(b["shoulder_distance"], 2)},
        "ear_to_shoulder_y":    {"current": round(m["ear_to_shoulder_y"], 2), "baseline": round(b["ear_to_shoulder_y"], 2)},
        "shoulder_ratio":       {"current": round(m["shoulder_ratio"], 4),    "baseline": round(b["shoulder_ratio"], 4)},
        "turtle_neck_timer":    round(now - _turtle_start, 1) if _turtle_start else 0,
        "round_shoulder_timer": round(now - _round_start, 1)  if _round_start  else 0,
    }


# ──────────────────────────────────────────
# 빠른 동작 확인 (직접 실행 시)
# ──────────────────────────────────────────

if __name__ == "__main__":
    # 기준 자세 (튜플 형식)
    baseline_pose = {
        "left_ear":       (0.40, 0.20),
        "right_ear":      (0.60, 0.20),
        "left_shoulder":  (0.35, 0.50),
        "right_shoulder": (0.65, 0.50),
        "neck_angle":     0.0,
        "is_bad_posture": False,
    }
    print("기준 자세 저장:", save_baseline(baseline_pose))

    # 거북목 시뮬레이션 (귀 간격 증가, 어깨-귀 y 감소)
    turtle_pose = {
        "left_ear":       (0.35, 0.27),
        "right_ear":      (0.65, 0.27),
        "left_shoulder":  (0.35, 0.50),
        "right_shoulder": (0.65, 0.50),
        "neck_angle":     0.0,
        "is_bad_posture": False,
    }
    print("neck_angle:     ", compute_neck_angle(turtle_pose))
    print("analyze_posture:", analyze_posture(turtle_pose))
    print("debug info:     ", get_debug_info(turtle_pose))
