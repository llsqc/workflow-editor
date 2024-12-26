class A:
    def __init__(self, name, identity_setting, task):
        self.name = name
        self.identity_setting = identity_setting
        self.task = task

    def generate_prompts(self, text):
        role = f"请记住你的身份是{self.identity_setting}"
        assign = f"你需要根据如上身份对 {text} 做出详细的分析，完成如下任务: {self.task}"
        return f"{role}\n{assign}"


class J:
    def __init__(self, name, identity_setting, task, output):
        self.name = name
        self.identity_setting = identity_setting
        self.task = task
        self.output = output

    def generate_prompts(self, text):
        role = f"请记住你的身份是{self.identity_setting}"
        assign = f"你需要根据如上身份对情况{text},完成判断任务:{self.task}"
        out = "你的回答需要根据如下要求:\n"
        for k, v in self.output.items():
            out += f"当情况: {k}发生时，你需要输出{v}\n"
        out += "记住按照要求输出，不要有其他多余的内容"
        return f"{role}\n{assign}\n{out}"


class H:
    def __init__(self, name, deal):
        self.name = name
        self.deal = deal

    def handle(self, text):
        try:
            local_vars = {'text': text}
            exec(self.deal, {}, local_vars)
            result = local_vars.get('result', None)
        except Exception as e:
            return f"Handler: {self.name} 执行失败，错误信息: {e}"
        return f"Handler: {self.name} 执行成功, 输出如下: {result}" if result is not None else f"Handler: {self.name} 执行成功"


class P:
    def __init__(self, identity_setting, style):
        self.identity_setting = identity_setting
        self.style = style

    def generate_prompts(self, text):
        role = f"请记住你的身份是{self.identity_setting}，你需要基于这个身份提供用于AI生图的提示词"
        assign = f"你需要根据如上身份对 {text} 做出艺术和设计上的分析，并根据风格 {self.style}，丰富并完善后给出用于AI生图的提示词。要求符合提示词的格式，对画面影响大的权重在前，影响小的在后，不需要完整的语句，只需要提示词，保证生成的画面精美"
        return f"{role}\n{assign}\n"