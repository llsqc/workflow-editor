import json

import requests

agent_create_url = "http://localhost:5000/agent/create"
scene_create_url = "http://localhost:5000/scene/create"

header = {
    "Content-Type": "application/json",
}

payload = json.dumps({
    "name": "简历筛选-HR",
    "description": "通过简历分析出各个求职者的优缺点和基本信息",
    "avatar": "",
    "kind": 0,
    "identity_setting": "招聘前端开发者的互联网公司HR",
    "task": "分析这些人的简历，输出格式为：姓名，邮箱，优点，缺点"
})
response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_1 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "简历筛选-Filter",
    "description": "根据求职者的信息，判断是否符合招聘需求",
    "avatar": "",
    "kind": 1,
    "identity_setting": "招聘前端开发者的互联网公司HR",
    "task": "判断这些求职者是否能胜任前端开发,每行输出求职者姓名和结果，输出格式为求职者姓名，邮箱，结果",
    "output": {
        "符合条件": "一面通过",
        "不符合条件": "一面不通过"
    }
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_2 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "简历筛选-Extractor",
    "description": "提取出通过筛选的求职者的联系方式",
    "avatar": "",
    "kind": 0,
    "identity_setting": "招聘前端开发者的互联网公司HR",
    "task": "输出一面通过的应聘者的名单，格式为[{\"name\":姓名,\"email\":邮箱}]的json数组，不要在markdown的包裹中，不要用```json开头"
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_3 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "简历筛选-Communicant",
    "description": "向通过简历筛选的求职者发送邮件",
    "avatar": "",
    "kind": 2,
    "deal": """
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
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_4 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "case1-简历筛选",
    "agents": [
        id_1,
        id_2,
        id_3,
        id_4
    ]
})
response = requests.request("POST", scene_create_url, headers=header, data=payload)
response.json()

print("成功创建scene", json.loads(payload)["name"])

payload = json.dumps({
    "name": "Python教学-Answer",
    "description": "给出该题的正确答案",
    "avatar": "",
    "kind": 0,
    "identity_setting": "资深的Python开发者",
    "task": "提供这个题目的正确解法，提供解题思路，要求注释详细，markdown的代码块需要给出语言"
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_1 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

# analyser2
payload = json.dumps({
    "name": "Python教学-Teacher",
    "description": "分析该题中涉及到的各个知识点",
    "avatar": "",
    "kind": 0,
    "identity_setting": "Python编程老师",
    "task": "提供这个题目的正确解法，要分析这道题目的知识点，给出最关键最重要的一个知识点，只输出知识点，不用分析题目，不涉及任何和题目相关的内容，知识点后不需要带解释，只需要给出名词求注释详细"
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_2 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

# analyser3
payload = json.dumps({
    "name": "Python教学-Questioner",
    "description": "根据涉及到的知识点给出类似的题目",
    "avatar": "",
    "kind": 0,
    "identity_setting": "Python编程老师",
    "task": "根据所给出的知识点提供一道新的编程题，要求题目与样例，markdown的代码块需要注明语言"
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_3 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "case2-Python教学",
    "agents": [
        id_1,
        id_2,
        id_3
    ]
})

response = requests.request("POST", scene_create_url, headers=header, data=payload)
response.json()

print("成功创建scene", json.loads(payload)["name"])

payload = json.dumps({
    "name": "绘本绘画-Teacher",
    "description": "修改作文并提供修改意见",
    "avatar": "",
    "kind": 0,
    "identity_setting": "小学语文老师",
    "task": "找出作文中的好词好句，给予表扬，找出病句错词，给予指正，给出总体评价与修改建议，要求输出的开头是原文，后续接修改建议"
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_1 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "绘本绘画-Story",
    "description": "分析故事，梳理主要的人物情节",
    "avatar": "",
    "kind": 0,
    "identity_setting": "善于总结的作家",
    "task": "提取这个故事的主要人物与情节，描述故事中最突出的一个画面"
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_2 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "绘本绘画-Illustrator",
    "description": "根据人物、情节、风格绘制对应的图片",
    "avatar": "",
    "kind": 3,
    "identity_setting": "插画画师",
    "style": "绘本"
})

response = requests.request("POST", agent_create_url, headers=header, data=payload)
id_3 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "case3-绘本绘画",
    "agents": [
        id_1,
        id_2,
        id_3
    ]
})

response = requests.request("POST", scene_create_url, headers=header, data=payload)

print("成功创建scene", json.loads(payload)["name"])
