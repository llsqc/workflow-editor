import requests

from const.LLM import STREAM, MODEL, CHAT_URL, UN_STREAM_HEADERS


def call_chat(identity_setting, prompts):
    messages = generate_messages(identity_setting, prompts)
    req = {
        "messages": messages,
        "stream": STREAM,
        "model": MODEL
    }
    response = requests.post(CHAT_URL, json=req, headers=UN_STREAM_HEADERS)
    print(response.json())
    return response.json()["choices"][0]["message"]["content"]


def generate_messages(identity_setting, prompts):
    messages = [{
        "role": "system",
        "content": "你的身份是" + identity_setting,
    }, {
        "role": "user",
        "content": prompts,
    }]
    return messages


if __name__ == '__main__':
    # call_chat("数学专家", """请记住你的身份是数学专家
    # 你需要根据如上身份对情况1 + 1 = 3, 完成判断任务:判断是否计算正确
    # 你的回答需要根据如下要求:
    # 当情况: 计算正确发生时，你需要输出123
    # 当情况: 计算错误发生时，你需要输出456
    # 记住按照要求输出，不要有其他多余的内容
    # """)
    out = call_chat("数学专家", """请记住你的身份是数学专家
你需要根据如上身份对 9+9等于几 做出详细的分析，完成如下任务: 提供这道题目的详细解题思路记住不能使用markdown的形式输出，要求就是正常文本
    """)
    print(out)
