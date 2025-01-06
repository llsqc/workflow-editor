from agent_create import *

url = "http://localhost:5000/scene/create"

payload = json.dumps({
    "name": "case2-PythonTeacher",
    "agents": [
        id_1,
        id_2,
        id_3
    ]
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

