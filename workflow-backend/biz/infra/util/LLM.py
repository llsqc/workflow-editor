import json
import logging

import requests

from biz.infra.consts.LLM import MODEL, CHAT_URL, IMAGE_MODEL, IMAGE_URL, HEADERS
from biz.infra.exception.biz_exception import BizException as BE
from biz.infra.exception.error_code import ErrorCode

"""
LLM 大模型调用工具类
提供对话调用，图片生成等工具
支持使用同步生成器实现流式输出
"""


def call_chat(identity_setting, prompts, stream=False):
    """
    调用LLM实现对话
    :param identity_setting: 身份设定 system prompts
    :param prompts: 提示词
    :param stream: 是否启用流式输出
    :return: LLM响应 or 同步生成器
    """
    messages = generate_messages(identity_setting, prompts)
    # 请求构建
    req = {
        "messages": messages,
        "stream": stream,
        "model": MODEL,
    }
    response = requests.post(CHAT_URL, json=req, headers=HEADERS, stream=stream)

    # 非流式输出
    if not stream:
        return response.json()["choices"][0]["message"]["content"]

    # 流式输出的同步生成器
    def generate_response():
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:  # 确保不是空行
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[len('data: '):]
                        if data == '[DONE]':  # 结束标志
                            break
                        json_data = json.loads(data)
                        content = json_data["choices"][0]["delta"]["content"]
                        yield content
        else:
            logging.error(response.status_code)
            raise BE.error(ErrorCode.CALL_CHAT_FAILED)

    return generate_response()


def call_image(prompts):
    """
    调用LLM实现图片生成
    :param prompts: 提示词
    :return: url and revised_prompts
    """
    req = {
        "prompt": prompts,
        "model": IMAGE_MODEL
    }
    response = requests.post(IMAGE_URL, json=req, headers=HEADERS)
    result = response.json()
    return result["data"][0]["url"], result["data"][0]["revised_prompt"]


def generate_messages(identity_setting, prompts):
    """
    生成消息体
    :param identity_setting: 身份设定
    :param prompts: 提示词
    :return: 本次调用使用的消息体
    """
    messages = [{
        "role": "system",
        "content": "你的身份是" + identity_setting,
    }, {
        "role": "user",
        "content": prompts,
    }]
    return messages
