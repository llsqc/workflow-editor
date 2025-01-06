from agent_create import *

url = "http://localhost:5000/scene/create"

payload = json.dumps({
    "name": "case3-illustrator",
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

