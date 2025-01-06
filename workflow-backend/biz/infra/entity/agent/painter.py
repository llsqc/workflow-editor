import json

from mongoengine import StringField

from biz.infra.entity.agent.agent import Agent
from biz.infra.util import LLM


class Painter(Agent):
    """
    Painter类，继承自Agent类。
    表示一个绘画agent，具有身份设定和风格属性。
    该类主要用于生成绘画提示词，并通过LLM调用生成图像。
    """

    # 身份设定，描述绘画agent的身份
    identity_setting = StringField()
    # 绘画风格，描述绘画agent的风格
    style = StringField()

    def call(self, text, stream=False):
        """
        调用Painter Agent生成图像。

        Args:
            text (str): 输入的文本，用于生成提示词。
            stream (bool): 是否以流式方式返回结果，默认为False。

        Returns:
            generator: 生成器对象，用于流式返回生成的图像数据。
        """
        # 生成提示词
        prompts = self.generate_prompts(text)
        # 调用LLM进行对话，生成初始结果
        r = LLM.call_chat(self.identity_setting, prompts, True)

        # 定义生成器函数
        def generator():
            p = ""
            i = 0
            # 逐块处理生成的结果
            for chunk in r:
                # 生成JSON格式的数据块
                yield json.dumps({
                    "number": i,
                    "id": str(self.id),
                    "content": chunk
                }, ensure_ascii=False) + '\n'
                i += 1
                p += chunk

            # 调用LLM生成图像，并获取图像URL和修订后的提示词
            url, revised_prompt = LLM.call_image(p)
            # 生成最终的JSON数据块
            yield json.dumps({
                'number': -1,
                'id': str(self.id),
                'content': url,
                'revised_prompt': revised_prompt,
            }, ensure_ascii=False) + '\n'

        # 返回生成器对象
        return generator()

    def generate_prompts(self, text):
        """
        生成用于AI生图的提示词。

        Args:
            text (str): 输入的文本，用于生成提示词。

        Returns:
            str: 生成的提示词字符串。
        """
        # 定义角色设定
        role = f"请记住你的身份是{self.identity_setting}，你需要基于这个身份提供用于AI生图的提示词"
        # 定义任务分配
        assign = f"你需要根据如上身份对 {text} 做出艺术和设计上的分析，并根据风格 {self.style}，丰富并完善后给出用于AI生图的提示词。要求符合提示词的格式，对画面影响大的权重在前，影响小的在后，不需要完整的语句，只需要提示词，保证生成的画面精美"
        # 返回组合后的提示词
        return f"{role}\n{assign}\n"

    def to_dict(self):
        """
        将Painter对象转换为字典格式，以便于序列化和传输。

        Returns:
            dict: 包含Painter对象详细信息的字典，包括id、name、description、avatar、kind、identity_setting和style。
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind,
            "identity_setting": self.identity_setting,
            "style": self.style
        }
