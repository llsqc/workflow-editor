from case.consts import applicants, email_deal
from case.agents import A, H, J

from biz.infra.util.LLM import call_chat

analyser1 = A(name="analyser code-1 互联网公司HR", identity_setting="招聘前端开发者的互联网公司HR",
              task="分析这些人的简历，输出格式为：姓名，邮箱，优点，缺点")

judge1 = J(name="judge code-1 互联网公司HR", identity_setting="互联网公司HR",
           task="判断这些求职者是否能胜任前端开发,每行输出求职者姓名和结果，输出格式为求职者姓名，邮箱，结果",
           output={"符合条件": "一面通过", "不符合条件": "一面不通过"})

analyser2 = A(name="analyser code-2 互联网公司HR", identity_setting="招聘前端开发者的互联网公司HR",
              task=
              """输出一面通过的应聘者的名单，格式为[{"name":姓名,"email":邮箱}]的json数组，不要在markdown的包裹中，不要用```json开头""")

handler1 = H(name="handler code-1 邮件通知", deal=email_deal)
# agent 1 分析问题解法
prompt1 = analyser1.generate_prompts(text=applicants)
output1 = call_chat(analyser1.identity_setting, prompt1, True)
pre = ""
print(analyser1.name + "输出如下")
for content in output1:
    pre += content
    print(content, end="")

prompt2 = judge1.generate_prompts(pre)
output2 = call_chat(judge1.identity_setting, prompt2, True)
pre = ""
print(judge1.name, "输出如下")
for content in output2:
    pre += content
    print(content, end="")

prompt3 = analyser2.generate_prompts(pre)
output3 = call_chat(analyser2.identity_setting, prompt3, True)
pre = ""
print(analyser2.name, "输出如下")
for content in output3:
    pre += content
    print(content, end="")

output4 = handler1.handle(pre)
print(output4)
