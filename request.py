import requests # <- 이거 설치 안되어있으면 pip install requests 해야함. 이거는 내장 함수아님
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


load_dotenv()  # .env 파일 로드 << 이거 다운로드 너거 노트북 윈도우였나? 윈도우면 걍 pip install python-dotenv 하고 mac이면 가상환경 만들고 pip install python-dotenv 해라
# ────────────────────────────────
# API로 예약 가능한지 확인해서 받아오는거
# ────────────────────────────────
def is_appointment_available():
    url = "https://terminvereinbarung.muenchen.de/termin/rest/locations/10187259/availableDays?serviceId=10339027"
    try:
        response = requests.get(url)
        data = response.json()
        return len(data["availableDays"]) > 0
    except Exception as e:
        print("예약 확인 실패:", e)
        return False

# ────────────────────────────────
# 2. 예약 뜨면 너 이메일로 보내짐
# ────────────────────────────────
def send_email():
    sender_email = os.getenv("EMAIL_SENDER") # 너거 이메일 <- .env에 넣어야함
    receiver_email = os.getenv("EMAIL_RECEIVER") # 이것도 너거 이메일 <- 요놈도 .env
    app_password = os.getenv("EMAIL_APP_PASSWORD") # 패스워드 <- 진짜진짜진짜 env에 넣어서 불러오려무나

    # ────────────────────────────────
    # EMAIL_APP_PASSWORD=너 이메일 비밀번호 // 어차피 위에 ""로 묶여있어서 따로 할 필요 X
    # EMAIL_SENDER = 님 이메일.
    # EMAIL_RECEIVER = 님 이메일
    # ────────────────────────────────  
    subject = "뮌헨 예약 ㄱㄱㄱㄱㄱㄱㄱㄱㄱ"
    body = "https://stadt.muenchen.de/buergerservice/terminvereinbarung.html#/services/10339027/locations/10187259 빨리 ㄱㄱㄱㄱㄱㄱㄱㄱ"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(message)
        print("예약떠서 이메일 보냄요")

# ────────────────────────────────
# 3. 메인 루프
# ────────────────────────────────
already_notified = False

while True:
    if is_appointment_available():
        if not already_notified:
            send_email()
            already_notified = True
    else:
        already_notified = False  # 누가 재빨리 먹어버린 경우
    time.sleep(20)  # 20초마다 확인하게는 해뒀는디 이건 너 맘
