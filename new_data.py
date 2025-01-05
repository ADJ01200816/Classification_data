
from setting import *
import read_information

from zhipuai import ZhipuAI
import pandas as pd
import re
import requests
import glob

with open(language + '/data/example/example.txt', 'a', encoding='utf-8') as file:
    file.write("")

client = ZhipuAI(api_key="a88353a9dd3d34fff9c685a5289a7805.aOn3va1j7wVpN3hM")  # Fill in your own APIKey
i = 0
name = read_information.get_name()
attribute = read_information.get_attribute()
level = read_information.get_level()

while i < 1:
    print("Total generated：")
    print(len(name))
    for item1, item2, item3 in zip(attribute, name, level):
        response = client.chat.completions.create(
            model="glm-4",  # Fill in the name of the model to be called
            messages=[
                {"role": "user", "content": item1}
            ],
        )
        ai_answer = response.choices[0].message.content
        ai_answer_str = str(ai_answer)  # Explicitly call __str__()

        file_path = language + f"/data/example/{len(glob.glob(language + '/data/example/*.txt'))-1}.txt"  # Specify the file path
        with open(file_path, 'w', encoding='utf-8') as file:  
            file.write(ai_answer_str)  # Write data to file
        

        print(f"数据已存入文本文件：{file_path}")
        with open(language + '/data/example/example.txt', 'a', encoding='utf-8') as file:  # Open the file using append mode (‘a’)
            file.write(f"{item3}|{item2}\n")  # The file will keep the original content and add new content at the end.

    i += 1