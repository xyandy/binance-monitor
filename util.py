import smtplib
from email.mime.text import MIMEText
from email.header import Header
from typing import Dict, List
import json
import re

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


def extract_announcements(data: Dict[str, List[Dict]]):
    # 正则表达式匹配日期格式 YYYY-MM-DD
    date_pattern = r"\d{4}-\d{2}-\d{2}$"

    announcements = []
    for item in data["internal"]:
        href = item["href"]
        text = item["text"]
        if "/en/support/announcement/" in href and re.search(date_pattern, text):
            # 提取日期并添加到结果中
            date_match = re.search(date_pattern, text)
            time_str = date_match.group(0) if date_match else None
            announcements.append({
                "href": href, 
                "text": text,
                "time": time_str
            })
    return announcements


if __name__ == "__main__":
    subject = "测试邮件"
    content = "这是一封测试邮件的内容"
    send_email(subject, content)

    # 读取JSON数据
    with open("tmp/tmp.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 提取公告
    announcements = extract_announcements(data)

    # 打印结果
    for announcement in announcements:
        print(f"标题: {announcement['text']}")
        print(f"链接: {announcement['href']}")
        print("-" * 80)
