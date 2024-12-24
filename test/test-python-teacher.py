# 教学场景
from test_ import A, H
from biz.infra.util.LLM import call_chat

analyser1 = A(name="analyser code-1 Python开发者", identity_setting="资深的Python开发者",
              task="提供这个题目的正确解法，要求注释详细")

# analyser2 = A(name="analyser code-2 编程老师", identity_setting="经验丰富的Python编程老师",
#               task="通俗易懂的教会我怎么做这道题，要求详细，首先讲讲整体的思路，然后给出具体步骤和为什么这么思考，最后给出每一个步骤的代码实现和需要注意的点")

analyser3 = A(name="analyser code-3 代码提取", identity_setting="从文本里提取代码",
              task="从这段文本里提取出python代码，代码块外不允许出现任何字符")

# agent 1 分析问题解法
prompt1 = analyser1.generate_prompts(
    text="现有 $N$ 名同学参加了期末考试，并且获得了每名同学的信息：姓名（不超过 $8$ 个字符的仅有英文小写字母的字符串）、语文、数学、英语成绩（均为不超过 $150$ 的自然数）。总分最高的学生就是最厉害的，请输出最厉害的学生各项信息（姓名、各科成绩）。如果有多个总分相同的学生，输出靠前的那位")
output1 = call_chat(analyser1.identity_setting, prompt1)
pre = ""
print(analyser1.name + "输出如下")
for content in output1:
    pre += content
    print(content, end="")

print()
print("-----------------------分割线--------------------")

#
# # agent 2 提供教学方法
# prompt2 = analyser2.generate_prompts(pre)
# output2 = call_chat(analyser2.identity_setting, prompt2)
# print(analyser2.name, "输出如下")
# for content in output2:
#     print(content, end="")

prompt3 = analyser3.generate_prompts(pre)
output3 = call_chat(analyser3.identity_setting, prompt3)
output3 = output3[10:-3]
pre = ""
for content in output3:
    pre += content
    print(content, end="")


print()
print("-----------------------分割线--------------------")

python_deal = pre

handler1 = H(name="handler code-1 邮件通知", deal=python_deal)
output4 = handler1.handle("")