from agent_create import *

url = "http://localhost:5000/scene/create"

payload = json.dumps({
    "name": "case1-HR",
    "agents": [
        id_1,
        id_2,
        id_3,
        id_4
    ]
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)