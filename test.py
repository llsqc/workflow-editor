from util.LLM import call_chat


class A:
    def __init__(self, name, identity_setting, task):
        self.name = name
        self.identity_setting = identity_setting
        self.task = task

    def generate_prompts(self, text):
        role = f"请记住你的身份是{self.identity_setting}"
        assign = f"你需要根据如上身份对 {text} 做出详细的分析，完成如下任务: {self.task}"
        return f"{role}\n{assign}\n记住不能使用markdown或latex的特殊形式输出，要求只能是正常文本"


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


if __name__ == '__main__':
    # 教学场景
    analyser1 = A(name="analyser code-1 Java开发者", identity_setting="资深的Java开发者", task="提供这个题目的解法")
    analyser2 = A(name="analyser code-2 编程老师", identity_setting="经验丰富的编程老师",
                  task="通俗易懂的教会我怎么做这道题，要求详细")

    # agent 1 分析问题解法
    prompt1 = analyser1.generate_prompts(
        text="现有 $N$ 名同学参加了期末考试，并且获得了每名同学的信息：姓名（不超过 $8$ 个字符的仅有英文小写字母的字符串）、语文、数学、英语成绩（均为不超过 $150$ 的自然数）。总分最高的学生就是最厉害的，请输出最厉害的学生各项信息（姓名、各科成绩）。如果有多个总分相同的学生，输出靠前的那位")
    output1 = call_chat(analyser1.identity_setting, prompt1)
    print(analyser1.name, "输出为", output1)

    # agent 2 提供教学方法
    prompt2 = analyser2.generate_prompts(output1)
    output2 = call_chat(analyser2.identity_setting, prompt2)
    print(analyser2.name, "输出为", output2)

#     # 日志分析场景
#     analyser3 = A(name="analyser code-3 资深运维工程师", identity_setting="资深的k8s管理和分布式运维工程师",
#                   task="深入分析日志记录的内容")
#     judge = J(name="judge code-1 运维工程师", identity_setting="资深的运维工程师",
#               task="判断是否出现需要告知工程师的异常",
#               output={"出现了异常": "异常", "没有异常": "正常"})
#     handler = H(name="handler code-1 邮件发送", deal="""
# if text == "异常":
#     result = "出现了异常，以邮件通知相关工程师!"
# elif text == "正常":
#     result = "没有异常，系统正常运行"
# """)
#
#     prompt3 = analyser3.generate_prompts(text="""{"@timestamp":"2024-12-03T21:44:00.899+08:00","caller":"middleware/middleware.go:19","content":"[meowchat.user RPC Request] req={\"Req\":{\"targetId\":\"67374d712447bc1ba07239c3\",\"type\":4,\"paginationOptions\":{\"limit\":0}}}, resp={\"Success\":{}}, err=\u003cnil\u003e","level":"info","span":"a8b957628f424ae1","trace":"57edd571708063fd2ebeabc32de7c97c"}
# {"@timestamp":"2024-12-03T21:44:00.899+08:00","caller":"middleware/middleware.go:19","content":"[platform.comment RPC Request] req={\"Req\":{\"type\":3,\"parentId\":\"6727671de3063facab7cb575\"}}, resp={\"Success\":{}}, err=\u003cnil\u003e","level":"info","span":"cdd6f74167101506","trace":"57edd571708063fd2ebeabc32de7c97c"}
# {"@timestamp":"2024-12-03T21:44:00.900+08:00","caller":"middleware/middleware.go:19","content":"[meowchat.user RPC Request] req={\"Req\":{\"targetId\":\"670f52348b14cccb1dfc89d2\",\"type\":4,\"paginationOptions\":{\"limit\":0}}}, resp={\"Success\":{\"total\":1}}, err=\u003cnil\u003e","level":"info","span":"d0fc47ee6aade3e7","trace":"57edd571708063fd2ebeabc32de7c97c"}
# {"@timestamp":"2024-12-03T21:44:00.900+08:00","caller":"adaptor/common.go:48","content":"[/moment/get_moment_p""")
#     output3 = call_chat(analyser3.identity_setting, prompt3)
#     print(analyser3.name, "输出为", output3)
#
#     prompt4 = judge.generate_prompts(output3)
#     output4 = call_chat(analyser3.identity_setting, prompt4)
#     print(judge.name, "输出为", output4)
#
#     result = handler.handle(output4)
#     print(handler.name, "输出为", result)
