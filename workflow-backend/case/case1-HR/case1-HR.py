"""

case1-简历筛选与自动通知

在常规招聘流程中，HR需要逐个浏览简历，判断求职者与招聘需求是否匹配，如果匹配则还需要找出邮箱并发送面试通知。这个过程通常重复且枯燥，可以通过工作流来自动化。

整个流程分为四个主要步骤：

1. 简历分析：分析应聘者的简历，提取关键信息，如姓名、邮箱、优点和缺点。
2. 条件判断：根据分析结果，判断应聘者是否符合前端开发职位的要求，输出是否通过一面。
3. 通过者名单生成：输出通过一面筛选的应聘者名单，格式为JSON数组。
4. 邮件通知：根据通过者名单，自动发送邮件通知给通过一面筛选的应聘者。

主要步骤：

1. Analyser - HR：从简历中提取出各个求职者的优势与缺陷
2. Judge - Filter：根据求职者的优缺点，判断是否通过
3. Analyser - Extractor：提取出通过一面的求职者信息
4. Handler - Communicant：邮件通知各个通过面试的求职者。

"""

from biz.infra.util.LLM import call_chat  # 导入大语言模型调用函数
from case.agents import A, H, J  # 从agents模块导入A（分析者）、H（处理者）、J（判断者）类
from case.consts import applicants, email_deal  # 从consts模块导入applicants（应聘者列表）和email_deal（邮件处理函数）

# 创建analyser1，用于分析应聘者的简历
analyser1 = A(name="简历筛选-Analyser-HR",  # agent名称
              identity_setting="招聘前端开发者的互联网公司HR",  # agent身份设定
              task="分析这些人的简历，输出格式为：姓名，邮箱，优点，缺点")  # agent任务

# 创建judge1，用于判断应聘者是否符合前端开发职位要求
judge1 = J(name="简历筛选-Judge-Filter",
           identity_setting="互联网公司HR",
           task="判断这些求职者是否能胜任前端开发,每行输出求职者姓名和结果，输出格式为求职者姓名，邮箱，结果",
           output={"符合条件": "一面通过", "不符合条件": "一面不通过"})  # 输出结果的映射

# 创建analyser2，用于输出一面通过的应聘者名单
analyser2 = A(name="简历筛选-Analyser-Extractor",
              identity_setting="招聘前端开发者的互联网公司HR",
              task="""输出一面通过的应聘者的名单，格式为[{"name":姓名,"email":邮箱}]的json数组，不要在markdown的包裹中，不要用```json开头""")

# 创建handler1，用于处理邮件通知
handler1 = H(name="简历筛选-Handler-Communicant",
             deal=email_deal.email_deal)  # 邮件处理函数

# analyser1
prompt1 = analyser1.generate_prompts(text=applicants.applicants)  # 生成分析简历的提示词
output1 = call_chat(analyser1.identity_setting, prompt1, True)  # 调用LLM进行分析
pre = ""  # 用于存储输出结果
print(analyser1.name + "输出如下")
for content in output1:  # 遍历输出结果
    pre += content  # 将结果拼接到pre中
    print(content, end="")  # 打印结果

print()

# judge1
prompt2 = judge1.generate_prompts(pre)
output2 = call_chat(judge1.identity_setting, prompt2, True)
pre = ""  # 清空pre，用于存储新的输出结果
print(judge1.name, "输出如下")
for content in output2:
    pre += content
    print(content, end="")

print()

# analyser2
prompt3 = analyser2.generate_prompts(pre)
output3 = call_chat(analyser2.identity_setting, prompt3, True)
pre = ""  # 清空pre，用于存储新的输出结果
print(analyser2.name, "输出如下")
for content in output3:
    pre += content
    print(content, end="")

print()

# handler1
output4 = handler1.handle(pre)  # 调用处理函数处理邮件通知
print(output4)  # 打印处理结果
