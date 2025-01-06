import json

import requests

agent_create_url = "http://localhost:5000/agent/create"
scene_create_url = "http://localhost:5000/scene/create"

header = {
    "Content-Type": "application/json",
}

payload = json.dumps({
    "name": "简历筛选-Analyser-HR",
    "description": "通过简历分析出各个求职者的优缺点和基本信息",
    "avatar": "",
    "kind": 0,
    "identity_setting": "招聘前端开发者的互联网公司HR",
    "task": "分析这些人的简历，输出格式为：姓名，邮箱，优点，缺点"
})
response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_1 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "简历筛选-Judge-Filter",
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

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_2 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "简历筛选-Analyser-Extractor",
    "description": "提取出通过筛选的求职者的联系方式",
    "avatar": "",
    "kind": 0,
    "identity_setting": "招聘前端开发者的互联网公司HR",
    "task": "输出一面通过的应聘者的名单，格式为[{\"name\":姓名,\"email\":邮箱}]的json数组，不要在markdown的包裹中，不要用```json开头"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_3 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "简历筛选-Handler-Communicant",
    "description": "向通过简历筛选的求职者发送邮件",
    "avatar": "",
    "kind": 2,
    "deal": "import json\nimport smtplib\nimport string\nfrom email.mime.multipart import MIMEMultipart\nfrom email.mime.text import MIMEText\n\nSUBJECT = '[面试通知] 一面通过'\nSENDER = '1449610641@qq.com'\nAUTHORIZATION_CODE = 'godhxkrehrewhdjf'\n\nSMTP_SERVER = 'smtp.qq.com'\nSMTP_PORT = 465\n\n# 创建邮件\ncandidates = json.loads(text)\nresult = ''\nfor candidate in candidates:\n    message = MIMEMultipart()\n    message['From'] = SENDER\n    message['To'] = candidate['email']\n    message['Subject'] = SUBJECT\n\n    # 邮件正文\n    body = candidate['name'] + \"同学，你好！恭喜通过我司第一轮面试，请耐心等待后续面试通知\"\n    message.attach(MIMEText(body, 'plain'))\n\n    # 连接到SMTP服务器并发送邮件\n    try:\n        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # 链接SMTP服务器\n        server.login(SENDER, AUTHORIZATION_CODE)  # 登录SMTP服务器\n        content = message.as_string()\n        server.sendmail(SENDER, candidate['email'], content)\n        server.quit()\n        result += candidate['name'] + ':' + candidate['email'] + '通知邮件发送成功'\n\n    except Exception as e:\n        result += candidate['name'] + ':' + candidate['email'] + '通知邮件发送失败'"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_4 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "case1-HR",
    "agents": [
        id_1,
        id_2,
        id_3,
        id_4
    ]
})
response = requests.request("POST", scene_create_url, headers=header,data=payload)
response.json()

print("成功创建scene", json.loads(payload)["name"])

payload = json.dumps({
    "name": "analyser code-1 Python开发者",
    "description": "case 2 - HR",
    "avatar": "",
    "kind": 0,
    "identity_setting": "资深的Python开发者",
    "task": "提供这个题目的正确解法，要求注释详细"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_1 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

# analyser2
payload = json.dumps({
    "name": "analyser code-2 知识点分析",
    "description": "case 2 - HR",
    "avatar": "",
    "kind": 0,
    "identity_setting": "Python编程老师",
    "task": "提供这个题目的正确解法，要分析这道题目的知识点，只输出知识点，不用分析题目，不涉及任何和题目相关的内容，知识点后不需要带解释，只需要给出名词求注释详细"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_2 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

# analyser3
payload = json.dumps({
    "name": "analyser code-3 巩固训练",
    "description": "case 2 - HR",
    "avatar": "",
    "kind": 0,
    "identity_setting": "Python编程老师",
    "task": "根据所给出的知识点提供一道新的编程题"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_3 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "case2-PythonTeacher",
    "agents": [
        id_1,
        id_2,
        id_3
    ]
})

response = requests.request("POST", scene_create_url, headers=header,data=payload)
response.json()

print("成功创建scene", json.loads(payload)["name"])

payload = json.dumps({
    "name": "analyser code-1 故事总结",
    "description": "case 3 - illustrator",
    "avatar": "",
    "kind": 0,
    "identity_setting": "善于总结的作家",
    "task": "提取这个故事的主要内容，字数为30字"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_1 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "analyser code-2 风格分析",
    "description": "case 3 - illustrator",
    "avatar": "",
    "kind": 0,
    "identity_setting": "善于分析故事的插画家",
    "task": "分析这个故事的画面，给出适合这个故事的绘画风格，并生成提示词，用于作画，只能输出一个词"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_2 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "analyser code-3 绘画",
    "description": "case 3 - illustrator",
    "avatar": "",
    "kind": 3,
    "identity_setting": "插画画师",
    "task": "卡通"
})

response = requests.request("POST", agent_create_url, headers=header,data=payload)
id_3 = response.json()["payload"]

print("成功创建agent", json.loads(payload)["name"])

payload = json.dumps({
    "name": "case3-illustrator",
    "agents": [
        id_1,
        id_2,
        id_3
    ]
})

response = requests.request("POST", scene_create_url, headers=header,data=payload)

print("成功创建scene", json.loads(payload)["name"])
