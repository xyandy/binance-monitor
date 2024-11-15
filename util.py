import smtplib
from email.mime.text import MIMEText
from email.header import Header

from config import EMIAL_CONFIG


def send_email(subject, content):
    sender = EMIAL_CONFIG["sender"]
    receiver = EMIAL_CONFIG["receiver"]
    password = EMIAL_CONFIG["password"]

    message = MIMEText(content, "plain", "utf-8")
    message["From"] = Header(sender)
    message["To"] = Header(receiver)
    message["Subject"] = Header(subject)

    try:
        with smtplib.SMTP(EMIAL_CONFIG["host"], EMIAL_CONFIG["port"]) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
    except Exception as e:
        print(f"fail to send email: {str(e)}")


if __name__ == "__main__":
    subject = "测试邮件"
    content = "这是一封测试邮件的内容"
    send_email(subject, content)
