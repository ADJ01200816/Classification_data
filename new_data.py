
from setting import *
import read_information

from zhipuai import ZhipuAI
import pandas as pd
import re
import requests
import glob

with open(language + '/data/example/example.txt', 'a', encoding='utf-8') as file:
    file.write("")

client = ZhipuAI(api_key="a88353a9dd3d34fff9c685a5289a7805.aOn3va1j7wVpN3hM")  # 填写您自己的APIKey
i = 0
name = read_information.get_name()
attribute = read_information.get_attribute()
level = read_information.get_level()

while i < 1:
    print("生成总数：")
    print(len(name))
    for item1, item2, item3 in zip(attribute, name, level):
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": item1}
            ],
        )
        ai_answer = response.choices[0].message.content
        ai_answer_str = str(ai_answer)  # 显式调用 __str__()

        file_path = language + f"/data/example/{len(glob.glob(language + '/data/example/*.txt'))-1}.txt"  # 指定文件路径
        with open(file_path, 'w', encoding='utf-8') as file:  # 使用open函数以写入模式打开文件
            file.write(ai_answer_str)  # 将数据写入文件
        

        print(f"数据已存入文本文件：{file_path}")
        with open(language + '/data/example/example.txt', 'a', encoding='utf-8') as file:  # 使用追加模式（'a'）打开文件
            file.write(f"{item3}|{item2}\n")  # 文件将保留原有内容，并在末尾添加新内容。

    i += 1