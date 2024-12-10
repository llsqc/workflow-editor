CHAT_URL = "https://chat.ecnu.edu.cn/open/api/v1/chat/completions"
KEY = "sk-13d4a8937ef9448fa4bddde1a5cd5e01"
MODEL = "ecnu-max"
STREAM = True
UN_STREAM_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + KEY
}
