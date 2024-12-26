email_deal = """
import json
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SUBJECT = '[面试通知] 一面通过'
SENDER = '1449610641@qq.com'
AUTHORIZATION_CODE = 'godhxkrehrewhdjf'

SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 465

# 创建邮件
candidates = json.loads(text)
result = ''
for candidate in candidates:
    message = MIMEMultipart()
    message['From'] = SENDER
    message['To'] = candidate['email']
    message['Subject'] = SUBJECT

    # 邮件正文
    body = candidate['name'] + "同学，你好！恭喜通过我司第一轮面试，请耐心等待后续面试通知"
    message.attach(MIMEText(body, 'plain'))

    # 连接到SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # 链接SMTP服务器
        server.login(SENDER, AUTHORIZATION_CODE)  # 登录SMTP服务器
        content = message.as_string()
        server.sendmail(SENDER, candidate['email'], content)
        server.quit()
        result += candidate['name'] + ':' + candidate['email'] + '通知邮件发送成功'

    except Exception as e:
        result += candidate['name'] + ':' + candidate['email'] + '通知邮件发送失败'
"""