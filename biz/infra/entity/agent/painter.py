import json

from mongoengine import StringField

from biz.infra.entity.agent.agent import Agent
from biz.infra.util import LLM


class Painter(Agent):
    identity_setting = StringField()
    style = StringField()

    def call(self, text, stream=False):
        prompts = self.generate_prompts(text)
        r = LLM.call_chat(self.identity_setting, prompts, False)

        def generator():
            i = 0
            for chunk in r:
                yield json.dumps({
                    "number": i,
                    "id": str(self.id),
                    "content": chunk
                }, ensure_ascii=False) + '\n'
                i += 1

            url, revised_prompt = LLM.call_image(r)
            yield json.dumps({
                'number': -1,
                'id': str(self.id),
                'url': url,
                'revised_prompt': revised_prompt,
            }, ensure_ascii=False) + '\n'

        return generator()

    def generate_prompts(self, text):
        role = f"请记住你的身份是{self.identity_setting}，你需要基于这个身份提供用于AI生图的提示词"
        assign = f"你需要根据如上身份对 {text} 做出艺术和设计上的分析，并根据风格 {self.style}，丰富并完善后给出用于AI生图的提示词。要求符合提示词的格式，对画面影响大的权重在前，影响小的在后，不需要完整的语句，只需要提示词，保证生成的画面精美"
        return f"{role}\n{assign}\n"

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "avatar": self.avatar,
            "kind": self.kind,
            "identity_setting": self.identity_setting,
            "style": self.style
        }
