
from setting import *
import read_information

from zhipuai import ZhipuAI
import pandas as pd
import re
import requests
import glob

with open('Datasets/' + dataset_path + '/' + language + '/Text_files/Data_labels.txt', 'a', encoding='utf-8') as file:
    file.write("")

client = ZhipuAI(api_key=api)  # Fill in your own APIKey
i = 0
name = read_information.get_name()
attribute = read_information.get_attribute()
level = read_information.get_level()

while i < 100:
    print("Generate totals:")
    print(len(name))
    lang = '中文'
    if language == 'en':
        lang = 'English'
    for item1, item2, item3 in zip(attribute, name, level):
        response = client.chat.completions.create(
            model=llm_model,  # Fill in the name of the model to be called
            messages=[
                {"role": "user", "content": "Please use"+lang+" to answer the question, please generate an unemotional descriptive long text for privacy data recognition, real and specific data is required to appear, it is forbidden to output the pre-text descriptive statements and end-of-text summarizing statements, it is required to contain the following named entity's specific implementations, and the named entity itself is not permitted to appear, for example: Named Entity: Name, Gender, Nationality, Income, Tax Payment, Phone Number Text: Zhang San is a male and a Chinese citizen with a monthly salary of 50,000 RMB and a tax payment of 8,000 RMB"+item1}
            ],
        )
        ai_answer = response.choices[0].message.content
        ai_answer_str = str(ai_answer)  
        file_path = 'Datasets/' + dataset_path + '/' + language + f"/Text_files/{len(glob.glob('Datasets/' + dataset_path + '/' + language + '/Text_files/*.txt'))-1}.txt"  # 指定文件路径
        with open(file_path, 'w', encoding='utf-8') as file: 
            file.write(ai_answer_str) 
        

        print(f"The data has been stored in a text file:{file_path}")
        with open('Datasets/' + dataset_path + '/' + language + '/Text_files/Data_labels.txt', 'a', encoding='utf-8') as file:  # 使用追加模式（'a'）打开文件
            file.write(f"{item3}|{item2}\n")  # The file will keep the original content and add new content at the end.

    i += 1