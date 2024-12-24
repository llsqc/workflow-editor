from test.HR_text import HR_text
from test_ import J
from test_ import A
from test_ import H

from util.LLM import call_chat

analyser1 = A(name="analyser code-1 互联网公司HR", identity_setting="招聘前端开发者的互联网公司HR",
              task="分析这些人的简历，输出格式为：姓名，邮箱，优点，缺点")

judge1 = J(name="judge code-1 互联网公司HR", identity_setting="互联网公司HR",
           task="判断这些求职者是否能胜任前端开发,每行输出求职者姓名和结果，输出格式为求职者姓名，邮箱，结果",
           output={"符合条件": "一面通过", "不符合条件": "一面不通过"})

analyser2 = A(name="analyser code-2 互联网公司HR", identity_setting="招聘前端开发者的互联网公司HR",
              task=
              """输出一面通过的应聘者的名单，格式为[{"name":姓名,"email":邮箱}]的json数组，不要在markdown的包裹中，不要用```json开头""")

handler1 = H(name="handler code-1 邮件通知", deal=
"""
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
""")
# agent 1 分析问题解法
prompt1 = analyser1.generate_prompts(text=HR_text)
output1 = call_chat(analyser1.identity_setting, prompt1, True)
pre = ""
print(analyser1.name + "输出如下")
for content in output1:
    pre += content
    print(content, end="")

prompt2 = judge1.generate_prompts(pre)
output2 = call_chat(judge1.identity_setting, prompt2, True)
pre = ""
print(judge1.name, "输出如下")
for content in output2:
    pre += content
    print(content, end="")

prompt3 = analyser2.generate_prompts(pre)
output3 = call_chat(analyser2.identity_setting, prompt3, True)
pre = ""
print(analyser2.name, "输出如下")
for content in output3:
    pre += content
    print(content, end="")

output4 = handler1.handle(pre)
print(output4)
