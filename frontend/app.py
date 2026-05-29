import tkinter as tk
from tkinter import messagebox

from vision.pose_detector import get_pose_data
from logic.posture_logic import analyze_posture
from logic.gemini_advisor import get_posture_comment

def show_warning(message):
    messagebox.showwarning("자세 경고", message)

def start_monitoring():
    guide_msg = "정확한 측정을 위해 측정 중에는 어깨와 상체 위치를 고정하고, 카메라와의 거리를 유지해주세요. 앞뒤로 움직이지 마세요."
    messagebox.showinfo("안내", guide_msg)

    try:
        # 테스트용 가짜 데이터
        pose_data = {
            "left_ear": (100, 100),
            "right_ear": (150, 100),
            "left_shoulder": (100, 200),
            "right_shoulder": (150, 200)
        }

        result = analyze_posture(pose_data)

        comment = get_posture_comment(result)

        if result["is_bad_posture"]:
            show_warning(comment)
        else:
            messagebox.showinfo("AI 코멘트", comment)

    except Exception as e:
        messagebox.showerror("오류", str(e))

def stop_monitoring():
    messagebox.showinfo("종료", "프로그램을 종료하고 결과를 저장합니다.")
    print("Firebase에 세션 데이터 저장 요청...")

root = tk.Tk()
root.title("PoseGuard")
root.geometry("450x450")

BG_COLOR = "#1E1E24"       
CARD_COLOR = "#2A2A35"     
TEXT_COLOR = "#F5F5FA"     
POINT_COLOR = "#6C5CE7"    
GREEN_COLOR = "#00B894"    
RED_COLOR = "#D63031"      

root.configure(bg=BG_COLOR)

title_frame = tk.Frame(root, bg=CARD_COLOR, pady=20)
title_frame.pack(fill="x")

title_label = tk.Label(
    title_frame, 
    text="PoseGuard", 
    font=("Helvetica", 24, "bold"), 
    fg=POINT_COLOR, 
    bg=CARD_COLOR
)
title_label.pack()

sub_title = tk.Label(
    title_frame, 
    text="AI 실시간 자세 교정 시스템", 
    font=("NanumGothic", 10), 
    fg="#A0A0B0", 
    bg=CARD_COLOR
)
sub_title.pack(pady=5)

info_frame = tk.Frame(root, bg=BG_COLOR)
info_frame.pack(pady=30)

info_label = tk.Label(
    info_frame, 
    text="상태: 측정 대기 중", 
    font=("NanumGothic", 12, "bold"), 
    fg=TEXT_COLOR, 
    bg=BG_COLOR
)
info_label.pack()

btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

start_button = tk.Button(
    btn_frame, 
    text="▶  측정 시작", 
    command=start_monitoring, 
    font=("NanumGothic", 11, "bold"),
    width=18, 
    height=2, 
    bg=GREEN_COLOR, 
    fg="white",
    relief="flat",          
    cursor="hand2"          
)
start_button.pack(pady=8)

stop_button = tk.Button(
    btn_frame, 
    text="■  측정 종료", 
    command=stop_monitoring, 
    font=("NanumGothic", 11, "bold"),
    width=18, 
    height=2, 
    bg=RED_COLOR, 
    fg="white",
    relief="flat",
    cursor="hand2"
)
stop_button.pack(pady=8)

test_button = tk.Button(
    root, 
    text="⚠️ 시스템 경고창 미리보기 테스트", 
    command=lambda: show_warning("거북목이 감지되었습니다! 자세를 고쳐주세요."),
    font=("NanumGothic", 9, "underline"),
    fg="#808090", 
    bg=BG_COLOR,
    relief="flat",
    activebackground=BG_COLOR,
    activeforeground=POINT_COLOR,
    cursor="hand2"
)
test_button.pack(side="bottom", pady=20)

root.mainloop()