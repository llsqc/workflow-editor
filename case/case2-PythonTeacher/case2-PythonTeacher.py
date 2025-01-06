"""
文件名称: 基于Agent的Python自动化教学工具

情景描述:
该文件实现了一个自动化流程，用于处理Python编程教学中的题目分析、知识点提取和巩固训练。整个流程分为三个主要步骤：
1. 问题解法分析：分析Python编程题目，提取并输出正确的解法，要求解法详细并带有注释。
2. 知识点提取：根据题目内容，提取相关的编程知识点，输出知识点列表，知识点后不带解释。
3. 巩固训练生成：根据提取的知识点，生成一道新的编程题目，用于巩固训练。

原理:
该脚本通过定义多个Agent（分析者、知识点提取者、巩固训练生成者），每个Agent负责不同的任务。每个Agent通过调用LLM生成相应的提示词（prompt），并将结果传递给下一个Agent。最终，由巩固训练生成者根据提取的知识点生成新的编程题目。

主要步骤：
1. analyser1：调用LLM分析Python题目，输出详细的解法。
2. analyser2：调用LLM提取题目相关的知识点，输出知识点列表。
3. analyser3：调用LLM根据知识点生成新的编程题目。

"""

# 导入代理类，用于不同任务的处理
from case.agents import A  # 导入代理类，用于不同任务的处理
# 导入与大语言模型交互的函数
from biz.infra.util.LLM import call_chat  # 导入与大语言模型交互的函数
# 导入Python问题常量
from case.consts import python_problem

# 定义第一个代理，负责提供问题的正确解法
analyser1 = A(name="Python教学-Analyser-Answer",
              identity_setting="资深的Python开发者",
              task="提供这个题目的正确解法，要求注释详细")

# 定义第二个代理，负责根据分析该题所涉及的知识点
analyser2 = A(name="Python教学-Analyser-Teacher",
              identity_setting="Python编程老师",
              task="分析这道题目的知识点，只输出知识点，不用分析题目，不涉及任何和题目相关的内容，知识点后不需要带解释，只需要给出名词")

# 定义第三个代理，负责根据该问题举一反三
analyser3 = A(name="Python教学-Analyser-Questioner",
              identity_setting="Python编程老师",
              task="根据所给出的知识点提供一道新的编程题")

# agent 1 分析问题解法
# 生成提示词，描述问题：找出总分最高的学生并输出其信息
prompt1 = analyser1.generate_prompts(text=python_problem.python_problem)

# 调用大语言模型，获取问题的解法
output1 = call_chat(analyser1.identity_setting, prompt1, True)
pre = ""  # 用于存储输出内容
print(analyser1.name + "输出如下")
for content in output1:
    pre += content
    print(content, end="")

print()

# agent 2 分析知识点
# 从上一步的输出中提取知识点
prompt2 = analyser2.generate_prompts(text=python_problem.python_problem)
output2 = call_chat(analyser2.identity_setting, prompt2, True)
pre = ""  # 重置存储变量
print(analyser2.name + "输出如下")
for content in output2:
    pre += content
    print(content, end="")

print()

# agent 3 提取代码
# 根据提供的知识点举一反三再出一道题
prompt3 = analyser3.generate_prompts(pre)
output3 = call_chat(analyser3.identity_setting, prompt3, True)
pre = ""  # 重置存储变量
print(analyser3.name + "输出如下")
for content in output3:
    pre += content
    print(content, end="")

print()