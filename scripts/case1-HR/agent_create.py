import requests
import json

url = "http://localhost:5000/agent/create"

# analyser1
payload = json.dumps({
    "name": "analyser code-1 互联网公司HR",
    "description": "case 1 - HR",
    "avatar": "",
    "kind": 0,
    "identity_setting": "招聘前端开发者的互联网公司HR",
    "task": "分析这些人的简历，输出格式为：姓名，邮箱，优点，缺点"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
id_1 = response.json()["id"]

# Judge1
payload = json.dumps({
    "name": "judge code-1 互联网公司HR",
    "description": "互联网公司HR",
    "avatar": "",
    "kind": 1,
    "identity_setting": "互联网公司HR",
    "task": "判断这些求职者是否能胜任前端开发,每行输出求职者姓名和结果，输出格式为求职者姓名，邮箱，结果",
    "output": {
        "符合条件": "一面通过",
        "不符合条件": "一面不通过"
    }
})

response = requests.request("POST", url, headers=headers, data=payload)
id_2 = response.json()["id"]

# analyser2
payload = json.dumps({
   "name": "analyser code-1 互联网公司HR",
   "description": "case 1 - HR",
   "avatar": "",
   "kind": 0,
   "identity_setting": "招聘前端开发者的互联网公司HR",
   "task": "输出一面通过的应聘者的名单，格式为[{\"name\":姓名,\"email\":邮箱}]的json数组，不要在markdown的包裹中，不要用```json开头"
})

response = requests.request("POST", url, headers=headers, data=payload)
id_3 = response.json()["id"]

# handler1
payload = json.dumps({
   "name": "handler code-1 邮件通知",
   "description": "case 1 - HR",
   "avatar": "",
   "kind": 2,
   "deal": "import json\nimport smtplib\nimport string\nfrom email.mime.multipart import MIMEMultipart\nfrom email.mime.text import MIMEText\n\nSUBJECT = '[面试通知] 一面通过'\nSENDER = '1449610641@qq.com'\nAUTHORIZATION_CODE = 'godhxkrehrewhdjf'\n\nSMTP_SERVER = 'smtp.qq.com'\nSMTP_PORT = 465\n\n# 创建邮件\ncandidates = json.loads(text)\nresult = ''\nfor candidate in candidates:\n    message = MIMEMultipart()\n    message['From'] = SENDER\n    message['To'] = candidate['email']\n    message['Subject'] = SUBJECT\n\n    # 邮件正文\n    body = candidate['name'] + \"同学，你好！恭喜通过我司第一轮面试，请耐心等待后续面试通知\"\n    message.attach(MIMEText(body, 'plain'))\n\n    # 连接到SMTP服务器并发送邮件\n    try:\n        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # 链接SMTP服务器\n        server.login(SENDER, AUTHORIZATION_CODE)  # 登录SMTP服务器\n        content = message.as_string()\n        server.sendmail(SENDER, candidate['email'], content)\n        server.quit()\n        result += candidate['name'] + ':' + candidate['email'] + '通知邮件发送成功'\n\n    except Exception as e:\n        result += candidate['name'] + ':' + candidate['email'] + '通知邮件发送失败'"
})

response = requests.request("POST", url, headers=headers, data=payload)
id_4 = response.json()["id"]
