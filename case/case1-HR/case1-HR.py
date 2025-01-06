"""
文件名称: 简历筛选与通知自动化流程

情景描述:
该文件实现了一个自动化流程，用于处理互联网公司前端开发职位的简历筛选和通知操作。整个流程分为四个主要步骤：
1. 简历分析：分析应聘者的简历，提取关键信息，如姓名、邮箱、优点和缺点。
2. 条件判断：根据分析结果，判断应聘者是否符合前端开发职位的要求，输出是否通过一面。
3. 通过者名单生成：输出通过一面筛选的应聘者名单，格式为JSON数组。
4. 邮件通知：根据通过者名单，自动发送邮件通知给通过一面筛选的应聘者。

原理:
该脚本通过定义多个Agent（分析者、判断者、处理者），每个Agent负责不同的任务。每个Agent通过调用LLM生成相应的提示词（prompt），并将结果传递给下一个Agent。最终，处理者Agent根据通过者的名单，自动发送邮件通知。

主要步骤：
1. analyser1：调用LLM分析简历，输出应聘者的关键信息。
2. judge1：调用LLM判断应聘者是否符合职位要求，输出是否通过一面。
3. analyser2：调用LLM生成通过一面筛选的应聘者名单。
4. handler1：根据通过者名单，调用邮件处理函数发送通知。

"""

# 导入LLM（大语言模型）调用函数
from biz.infra.util.LLM import call_chat
from case.agents import A, H, J  # 从agents模块导入A（分析者）、H（处理者）、J（判断者）类
# 导入所需的模块和类
from case.consts import applicants, email_deal  # 从consts模块导入applicants（应聘者列表）和email_deal（邮件处理函数）

# 创建analyser1，用于分析应聘者的简历
analyser1 = A(name="analyser code-1 互联网公司HR",  # agent名称
              identity_setting="招聘前端开发者的互联网公司HR",  # agent身份设定
              task="分析这些人的简历，输出格式为：姓名，邮箱，优点，缺点")  # agent任务

# 创建judge1，用于判断应聘者是否符合前端开发职位要求
judge1 = J(name="judge code-1 互联网公司HR",  # agent名称
           identity_setting="互联网公司HR",  # agent身份设定
           task="判断这些求职者是否能胜任前端开发,每行输出求职者姓名和结果，输出格式为求职者姓名，邮箱，结果",  # agent任务
           output={"符合条件": "一面通过", "不符合条件": "一面不通过"})  # 输出结果的映射

# 创建analyser2，用于输出一面通过的应聘者名单
analyser2 = A(name="analyser code-2 互联网公司HR",  # agent名称
              identity_setting="招聘前端开发者的互联网公司HR",  # agent身份设定
              task="""输出一面通过的应聘者的名单，格式为[{"name":姓名,"email":邮箱}]的json数组，不要在markdown的包裹中，不要用```json开头""")  # agent任务

# 创建handler1，用于处理邮件通知
handler1 = H(name="handler code-1 邮件通知",
             deal=email_deal.email_deal)  # agent名称和邮件处理函数

# analyser1分析应聘者简历
prompt1 = analyser1.generate_prompts(text=applicants.applicants)  # 生成分析简历的提示词
output1 = call_chat(analyser1.identity_setting, prompt1, True)  # 调用LLM进行分析
pre = ""  # 用于存储输出结果
print(analyser1.name + "输出如下")  # 打印agent1名称
for content in output1:  # 遍历输出结果
    pre += content  # 将结果拼接到pre中
    print(content, end="")  # 打印结果

print()

# judge1判断应聘者是否符合条件
prompt2 = judge1.generate_prompts(pre)  # 生成判断条件的提示词
output2 = call_chat(judge1.identity_setting, prompt2, True)  # 调用LLM进行判断
pre = ""  # 清空pre，用于存储新的输出结果
print(judge1.name, "输出如下")  # 打印agent1名称
for content in output2:  # 遍历输出结果
    pre += content  # 将结果拼接到pre中
    print(content, end="")  # 打印结果

print()

# analyser2输出一面通过的应聘者名单
prompt3 = analyser2.generate_prompts(pre)  # 生成输出名单的提示词
output3 = call_chat(analyser2.identity_setting, prompt3, True)  # 调用LLM生成名单
pre = ""  # 清空pre，用于存储新的输出结果
print(analyser2.name, "输出如下")  # 打印agent2名称
for content in output3:  # 遍历输出结果
    pre += content  # 将结果拼接到pre中
    print(content, end="")  # 打印结果

print()

# handler1处理邮件通知
output4 = handler1.handle(pre)  # 调用处理函数处理邮件通知
print(output4)  # 打印处理结果
