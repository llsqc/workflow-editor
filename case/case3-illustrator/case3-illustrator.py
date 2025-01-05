"""
文件名称: 绘画创作自动化流程

情景描述:
该文件实现了一个自动化流程，用于处理绘画创作中的灵感激发、风格分析和创作指导。整个流程分为三个主要步骤：
1. 灵感激发：分析给定的主题或关键词，生成绘画灵感和创意构思，要求详细描述画面内容和情感表达。
2. 风格分析：根据灵感内容，提取相关的艺术风格和技法，输出风格列表，风格后不带解释。
3. 创作指导生成：根据提取的艺术风格，生成具体的创作指导，包括构图建议、色彩搭配和技法应用。

原理:
该脚本通过定义多个Agent（灵感激发者、风格分析者、创作指导生成者），每个Agent负责不同的任务。每个Agent通过调用LLM生成相应的提示词（prompt），并将结果传递给下一个Agent。最终，由创作指导生成者根据提取的艺术风格生成具体的创作指导。

主要步骤：
1. analyser1：调用LLM分析绘画主题，输出详细的灵感构思。
2. analyser2：调用LLM提取灵感相关的艺术风格，输出风格列表。
3. painter：调用LLM根据艺术风格生成创作指导。
"""

# 导入代理类，用于不同任务的处理
from case.agents import A, P  # 导入代理类，用于不同任务的处理
# 导入与大语言模型交互的函数
from biz.infra.util.LLM import call_chat, call_image  # 导入与大语言模型交互的函数
# 导入Python问题常量
from case.consts import story

# 定义第一个分析器，用于总结故事内容
analyser1 = A(name="analyser code-1 故事总结",
              identity_setting="善于总结的作家",
              task="提取这个故事的主要内容，字数为30字")

# 定义第二个分析器，用于分析故事的绘画风格
analyser2 = A(name="analyser code-2 风格分析",
              identity_setting="善于分析故事的插画家",
              task="分析这个故事的画面，给出适合这个故事的绘画风格，并生成提示词，用于作画，只能输出一个词")

prompt1 = analyser1.generate_prompts(text=story.story)
output1 = call_chat(analyser1.identity_setting, prompt1, True)
pre = ""  # 用于存储输出内容
print(analyser1.name + "输出如下")
for content in output1:
    pre += content
    print(content, end="")

print()

# 将分析器1的输出保存为故事的总结
summary = pre

prompt2 = analyser2.generate_prompts(summary)
output2 = call_chat(analyser2.identity_setting, prompt2, True)
pre = ""  # 重置存储变量
print(analyser2.name + "输出如下")
for content in output2:
    pre += content
    print(content, end="")

print()

# 将分析器2的输出保存为绘画风格提示词
style = pre

# 定义绘画师，用于生成图像
painter1 = P(name="analyser code-3 绘画",
              identity_setting="儿童画画师",
              style=style)

prompt3 = painter1.generate_prompts(summary)
output3 = call_image(prompt3)

# 输出生成的图像的url
print(output3)