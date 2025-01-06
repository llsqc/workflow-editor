"""

case2-Python自动化教学工具

在教学过程中，教师需要根据学生的知识掌握情况为学生筛
选定制学生需要的题目以供学生巩固薄弱知识点。使用该工作流能根据学生提供的题目，给出正确的解答，然后分析出涉及的知识点并举一反三给出类似的题目用于巩固知识

整个流程分为三个主要步骤：

1. 题目解答：按照Python老师的口味解答题目，分析解题过程并给出注释
2. 知识点分析：分析给出题目的知识点
3. 题目生成：根据分析得到的知识点，为学生生成新的题目，提供输入输出样例，解题提示和参考答案

主要步骤：

1. Analyser - Answer：分析题目，给出该题的正确答案
2. Analyser - Teacher：分析该题中涉及到的各个知识点
3. Analyser - Questioner：根据涉及到的知识点，给出类似的题目，用于巩固

"""

from case.agents import A  # 从agents模块导入A（分析者）类
from biz.infra.util.LLM import call_chat  # 导入与大语言模型交互的函数
from case.consts import python_problem  # 导入Python问题常量

# 定义analyser1，负责提供问题的正确解法
analyser1 = A(name="Python教学-Analyser-Answer",
              identity_setting="资深的Python开发者",
              task="提供这个题目的正确解法，要求注释详细")

# 定义analyser2，负责根据分析该题所涉及的知识点
analyser2 = A(name="Python教学-Analyser-Teacher",
              identity_setting="Python编程老师",
              task="分析这道题目的知识点，只输出知识点，不用分析题目，不涉及任何和题目相关的内容，知识点后不需要带解释，只需要给出名词")

# 定义analyser3，负责根据该问题举一反三
analyser3 = A(name="Python教学-Analyser-Questioner",
              identity_setting="Python编程老师",
              task="根据所给出的知识点提供一道新的编程题")

# agent 1 分析问题解法
prompt1 = analyser1.generate_prompts(text=python_problem.python_problem)
output1 = call_chat(analyser1.identity_setting, prompt1, True)  # 调用大语言模型，获取问题的解法
pre = ""  # 用于存储输出内容
print(analyser1.name + "输出如下")
for content in output1:
    pre += content
    print(content, end="")

print()

# agent 2 分析知识点，从上一步的输出中提取知识点
prompt2 = analyser2.generate_prompts(text=python_problem.python_problem)
output2 = call_chat(analyser2.identity_setting, prompt2, True)
pre = ""  # 重置存储变量
print(analyser2.name + "输出如下")
for content in output2:
    pre += content
    print(content, end="")

print()

# agent 3 提取代码，根据提供的知识点举一反三再出一道题
prompt3 = analyser3.generate_prompts(pre)
output3 = call_chat(analyser3.identity_setting, prompt3, True)
pre = ""  # 重置存储变量
print(analyser3.name + "输出如下")
for content in output3:
    pre += content
    print(content, end="")

print()