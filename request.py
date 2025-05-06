import requests
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일 로드
# ────────────────────────────────
# 1. 예약 확인 함수
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
# 2. 이메일 발송 함수
# ────────────────────────────────
def send_email():
    sender_email = "dlguswp010731@gmail.com"
    receiver_email = "dlguswp010731@gmail.com"
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    subject = "✅ 뮌헨 예약 가능!"
    body = "https://stadt.muenchen.de/buergerservice/terminvereinbarung.html#/services/10339027/locations/10187259 에서 예약이 열렸습니다!"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(message)
        print("✅ 이메일 전송 완료")

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
        already_notified = False  # 다음에 다시 가능해지면 알림 보내기
    time.sleep(20)  # 1분마다 확인