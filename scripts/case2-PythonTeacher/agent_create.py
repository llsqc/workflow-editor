import requests
import json

url = "http://localhost:5000/agent/create"

# analyser1
payload = json.dumps({
    "name": "analyser code-1 Python开发者",
    "description": "case 2 - HR",
    "avatar": "",
    "kind": 0,
    "identity_setting": "资深的Python开发者",
    "task": "提供这个题目的正确解法，要求注释详细"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
id_1 = response.json()["id"]

# analyser2
payload = json.dumps({
    "name": "analyser code-2 知识点分析",
    "description": "case 2 - HR",
    "avatar": "",
    "kind": 0,
    "identity_setting": "Python编程老师",
    "task": "提供这个题目的正确解法，要分析这道题目的知识点，只输出知识点，不用分析题目，不涉及任何和题目相关的内容，知识点后不需要带解释，只需要给出名词求注释详细"
})

response = requests.request("POST", url, headers=headers, data=payload)
id_2 = response.json()["id"]

# analyser3
payload = json.dumps({
   "name": "analyser code-3 巩固训练",
   "description": "case 2 - HR",
   "avatar": "",
   "kind": 0,
   "identity_setting": "Python编程老师",
   "task": "根据所给出的知识点提供一道新的编程题"
})

response = requests.request("POST", url, headers=headers, data=payload)
id_3 = response.json()["id"]