"""
logic/gemini_advisor.py - 원준혁 담당 (logic 브랜치)

역할:
  - analyze_posture() 결과를 받아 Gemini API로 맞춤 건강 코멘트 생성
  - 세션 종료 시 전체 자세 요약 코멘트 생성

주요 공개 함수:
  get_posture_comment(posture_result) -> str   # 실시간 경고 시 호출
  get_session_summary(session_data)   -> str   # 세션 종료 시 호출
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env 파일에서 API 키 로드
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


# ──────────────────────────────────────────
# 실시간 자세 경고 코멘트
# ──────────────────────────────────────────

def get_posture_comment(posture_result: dict) -> str:
    """
    analyze_posture() 반환값을 받아 Gemini로 맞춤 코멘트 생성.

    입력:
        posture_result = {
            "turtle_neck":    bool,
            "round_shoulder": bool,
            "is_bad_posture": bool,
            "message":        str
        }

    반환: 사용자에게 보여줄 코멘트 문자열
    """
    if not posture_result.get("is_bad_posture"):
        return "자세가 좋습니다! 계속 유지해주세요 😊"

    issues = []
    if posture_result.get("turtle_neck"):
        issues.append("거북목")
    if posture_result.get("round_shoulder"):
        issues.append("라운드숄더")

    issue_str = "와 ".join(issues)

    prompt = f"""
당신은 자세 교정 전문가입니다.
사용자에게 현재 {issue_str} 자세가 감지되었습니다.
다음 조건에 맞게 짧고 친근한 한국어 코멘트를 작성해주세요:
- 2~3문장 이내
- 구체적인 교정 방법 1가지 포함
- 딱딱하지 않고 친근한 말투
- 이모지 1~2개 사용
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini 오류] {e}"


# ──────────────────────────────────────────
# 세션 종료 시 전체 요약 코멘트
# ──────────────────────────────────────────

def get_session_summary(session_data: dict) -> str:
    """
    세션 종료 후 전체 자세 데이터를 받아 요약 코멘트 생성.

    입력 (workflow.md / firebase_structure.md 기준):
        session_data = {
            "duration_minutes":   int,    # 세션 시간 (분)
            "good_posture_rate":  float,  # 양호 자세 비율 (0.0 ~ 1.0)
            "turtle_neck_count":  int,    # 거북목 알림 횟수
            "round_shoulder_count": int,  # 라운드숄더 알림 횟수
        }

    반환: 세션 결과 화면에 표시할 요약 코멘트 문자열
    """
    good_rate_pct = round(session_data.get("good_posture_rate", 0) * 100)
    duration      = session_data.get("duration_minutes", 0)
    turtle_count  = session_data.get("turtle_neck_count", 0)
    round_count   = session_data.get("round_shoulder_count", 0)

    prompt = f"""
당신은 자세 교정 전문가입니다.
사용자의 오늘 자세 세션 결과입니다:
- 세션 시간: {duration}분
- 올바른 자세 유지율: {good_rate_pct}%
- 거북목 감지 횟수: {turtle_count}회
- 라운드숄더 감지 횟수: {round_count}회

다음 조건에 맞게 한국어로 전체 요약 코멘트를 작성해주세요:
- 3~4문장 이내
- 결과에 대한 칭찬 또는 격려 포함
- 내일을 위한 구체적인 개선 팁 1가지 포함
- 친근하고 따뜻한 말투
- 이모지 2~3개 사용
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini 오류] {e}"


# ──────────────────────────────────────────
# 동작 확인 (직접 실행 시)
# ──────────────────────────────────────────

if __name__ == "__main__":
    # 실시간 경고 테스트
    test_result = {
        "turtle_neck":    True,
        "round_shoulder": False,
        "is_bad_posture": True,
        "message":        "⚠️ 거북목 감지됨",
    }
    print("=== 실시간 코멘트 ===")
    print(get_posture_comment(test_result))

    # 세션 요약 테스트
    test_session = {
        "duration_minutes":     30,
        "good_posture_rate":    0.65,
        "turtle_neck_count":    4,
        "round_shoulder_count": 1,
    }
    print("\n=== 세션 요약 ===")
    print(get_session_summary(test_session))
