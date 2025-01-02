
from setting import *


"""
#########
以下为预分类
#########
"""

#输入字符串得到词嵌入向量
def get_sentence_embedding(sentence:str)->np.ndarray:
    
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    #input必须小于512字/词
    outputs = model(**inputs,output_hidden_states=True) 
    #0:获取BERT最后一层（即词汇维度）的输出，并取平均
    if embedding_number == 0:
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    """
    #1:取最后一层的 [CLS] token
    if embedding_number == 1:
        embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
    #2
    if embedding_number == 2:
        # 聚合最后四层的输出
        mean_hidden_states = [outputs.hidden_states[i].mean(dim=1) for i in [-1, -2, -3, -4]]
        # 然后将每个均值从计算图中分离，并转换为NumPy数组
        embeddings = [state.detach().numpy() for state in mean_hidden_states]
        embeddings = np.concatenate(embeddings, axis=-1)
    #3
    if embedding_number == 3:
        # 使用一个简单的自注意力机制
        attention_scores = torch.matmul(outputs.last_hidden_state, outputs.last_hidden_state.transpose(-1, -2))
        attention_weights = torch.nn.functional.softmax(attention_scores, dim=-1)
        embeddings = torch.matmul(attention_weights, outputs.last_hidden_state).mean(dim=1).detach().numpy()
    """
    return embeddings

import read_information




"""
#########
以下为大模型提问
#########
"""

#将短文本输入llm
def small_file_to_llm(file_str:str, question_str_list:list[str])->list[str]:

    stime = time.time()
    language = ""
    if(language == 'cn'):
        language = "中文"
    elif (language == 'en'):
        language = "全小写的英语"
    question_str = ""
    for index, question in enumerate(question_str_list):
        question_str = question_str + "q%d:" % (index+1)
        question_str = question_str + question + '\n'

    ps_info = "你的回复语言请使用%s.由于你的回答将被用于成批数据处理，以下是规定回答，你回答的信息中命名实体一定要完整且与问题提及的命名实体一模一样，每个句子的回答只能占一行，如果不存在该命名实体，输出:|+命名实体名+0，如果存在该命名实体，输出:|+命名实体名+1，单个句子的每个命名实体输出间需用|分隔而不是,分割，处理完当前一个问题立即换行"%(language)
    #使用智谱清言官方接口
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": "%s.文件C:\n%s.文件如上。 请对以下问题集分别回答问题。问题集：\n%s" % (ps_info, file_str, question_str)
            }
        ],
    )
    #print("\n\n\n\n")
    #print("%s.文件C:\n%s.文件如上。 请对以下问题集分别回答问题。问题集：\n%s" % (ps_info, file_str, question_str))
    message_content = response.choices[0].message.content
    #print("end")
    #print(message_content)
    etime = time.time()
    #print(etime-stime)
    return llm_text_handle(message_content)

#将llm返回内容处理为命名实体列表
def llm_text_handle(text:str)->list[str]:
    attribute = []
    str_list = text.split('\n')
    #对llm的回答分割出每一命名实体
    for str in str_list:
        if '|' in str:
            tmp = str.split('|')
            for tmpp in tmp:
                if '1' in tmpp and 'q' not in tmpp.split('1')[0]:
                    attribute.append(tmpp.split('1')[0].strip())
    #统一命名实体格式
    if(language == 'en'):
        for i, attri in enumerate(attribute):
            attribute[i] = attri.strip().lower()
    return attribute

#llm返回内容处理去除特殊字符
def llm_text_handle2(attribute:str)->str:
    attribute = re.split(delimiters, attribute)
    attri_str = ''
    for attri in attribute:
        if attri == '' or attri == '+':
            continue
        if attri[0] == '+':
            attri = attri[1:]
        if attri[-1] == '+':
            attri = attri[0:len(attri)-1]
        attri_str = attri_str + ',' + attri
    attri_str = attri_str[1:]
    return attri_str


#待补充
def long_text_split(file):
    file_list = []
    file_list.append(file)
    return file_list


#输入文件与问题，输出命名实体
def get_attribute(file:str, question_list:list[str],i00=-1)->list[str]:

    question_range = narrow_question_range(file, i00)
    question_list = read_information.get_question(question_range=question_range)
    #print("qlen:%d"%len(question_list))
    attribute = []
    #attribute = invert_index.get_attribute_by_str_matching(question_range, file)
    
    text_list = long_text_split(file)

    for text in text_list:
#llm输入最大数量为2048字，因此需分批输入问题
        for qi in range(len(question_list)//max_question):
            q = question_list[qi*max_question:(qi+1)*max_question]
            answer = small_file_to_llm(file,q)
            for attri in answer:
                attri = llm_text_handle2(attri)
                attribute.append(i)
    attribute = list(set(attribute))
    return attribute





def count_files_in_directory(directory_path):
    return len([f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))])

def find_highest_numbered_file(folder_path, suffix):
    if(count_files_in_directory(folder_path) == 0):
        return 0
    max_number = 0
    for filename in os.listdir(folder_path):
        filename = filename[0:len(filename)-len(suffix)]
        if filename.isdigit():
            number = int(filename)
            if number > max_number:
                max_number = number
    return max_number+1

def clear_folder(path):
    # 检查路径是否存在
    if os.path.exists(path):
        # 遍历目录中的文件和文件夹
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                # 如果是文件，直接删除
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # 如果是目录，递归删除
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        print('The path %s does not exist' % path)