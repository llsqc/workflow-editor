"""

case3-绘画创作自动化

该工作流能批改小朋友写的作文，并根据小朋友写的作文，分析故事的主要人物、情节，分许需要的风格，生成对应的绘本图片，能完成装订校刊等方便小朋友教学的功能

整个流程分为四个主要步骤：

1. 作文批改：批改作文并提供修改意见
2. 作文概述：提炼小朋友写的作文的内容要点
3. 画风分析：根据所提炼的作文概述，分析这篇作文的文字风格和内容适合用什么样的画风来展现
4. 绘画：根据分析的画风与内容梗概，绘制符合的绘本图片

主要步骤：

1. Analyser - Teacher：批改作文并提供修改意见
2. Analyser - Story：分析故事，梳理主要的人物、情节
3. Analyser - Style：分析这个故事需要的风格
4. Painter - Illustrator：根据人物、情节、风格绘制对应的图片

"""

from case.agents import A, P  # 从agents模块导入A（分析者）、P（画家）类
from biz.infra.util.LLM import call_chat, call_image  # 导入与大语言模型交互的函数
from case.consts import story  # 导入小学生作文常量story

# 定义analyser1，用于批改作文
analyser1 = A(name="绘本绘画-Analyser-Teacher",
              identity_setting="小学语文老师",
              task="用教导小学生的口吻提出给出的这篇作文的修改意见")

# 定义analyser2，用于总结故事内容
analyser2 = A(name="绘本绘画-Analyser-Story",
              identity_setting="善于总结的作家",
              task="提取这个故事的主要内容，字数为30字")

# 定义analyser3，用于分析故事的绘画风格
analyser3 = A(name="绘本绘画-Analyser-Style",
              identity_setting="善于分析故事的插画家",
              task="给出适合这个故事的绘画风格，只能输出一个词语")

prompt1 = analyser1.generate_prompts(text=story.story)
output1 = call_chat(analyser1.identity_setting, prompt1, True)
pre = ""  # 用于存储输出内容
print(analyser1.name + "输出如下")
for content in output1:
    pre += content
    print(content, end="")

print()

prompt2 = analyser2.generate_prompts(text=story.story)
output2 = call_chat(analyser2.identity_setting, prompt2, True)
pre = ""  # 用于存储输出内容
print(analyser2.name + "输出如下")
for content in output2:
    pre += content
    print(content, end="")

print()

# 将analyser2的输出保存
summary = pre

prompt3 = analyser3.generate_prompts(summary)
output3 = call_chat(analyser3.identity_setting, prompt3, True)
pre = ""  # 重置存储变量
print(analyser3.name + "输出如下")
for content in output3:
    pre += content
    print(content, end="")

print()

# 将analyser3的输出保存为绘画风格提示词
style = pre

# 定义painter1，用于生成图像
painter1 = P(name="绘本绘画-Painter-Illustrator",
              identity_setting="插画画师",
              style=style)

prompt4 = painter1.generate_prompts(summary)
output4 = call_image(prompt4)

# 输出生成的图像的url
print(output4)