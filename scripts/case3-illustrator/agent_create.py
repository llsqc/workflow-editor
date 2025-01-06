import requests
import json

url = "http://localhost:5000/agent/create"

# analyser1
payload = json.dumps({
   "name": "analyser code-1 故事总结",
   "description": "case 3 - illustrator",
   "avatar": "",
   "kind": 0,
   "identity_setting": "善于总结的作家",
   "task": "提取这个故事的主要内容，字数为30字"
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
id_1 = response.json()["id"]


# analyser2
payload = json.dumps({
   "name": "analyser code-2 风格分析",
   "description": "case 3 - illustrator",
   "avatar": "",
   "kind": 0,
   "identity_setting": "善于分析故事的插画家",
   "task": "分析这个故事的画面，给出适合这个故事的绘画风格，并生成提示词，用于作画，只能输出一个词"
})

response = requests.request("POST", url, headers=headers, data=payload)
id_2 = response.json()["id"]

# painter
payload = json.dumps({
   "name": "analyser code-3 绘画",
   "description": "case 3 - illustrator",
   "avatar": "",
   "kind": 3,
   "identity_setting": "插画画师",
   "task": "卡通"
})

response = requests.request("POST", url, headers=headers, data=payload)
id_3 = response.json()["id"]