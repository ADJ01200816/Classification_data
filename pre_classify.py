
from setting import *
import tools
import read_information

#被使用而不依赖其它的方法

def preprocess_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


#输入分类列表和目标，计算余弦相似度
def prior_classify(classify_embedding:list[np.ndarray], material_embedding:np.ndarray)->list[float]:
    ret_level = []
    for embedding in classify_embedding:
       value_similarity = cosine_similarity(embedding, material_embedding)[0][0]
       ret_level.append(value_similarity)
    return ret_level

#输入关键词得到问题缩小范围
def get_range(keyword:str)->list[int]:

    attribute_size = read_information.get_size()
    #embedding/embedding_list -sum/embedding_list -max
    #关键词句子和attribute句计算
    if(E == "embedding"):
        attribute_embedding = read_information.get_attribute_embedding()
        keyword_embedding = tools.get_sentence_embedding(keyword)
        return prior_classify(attribute_embedding, keyword_embedding)
    #关键词词语与attribute词语计算
    else:
        keyword = re.split(delimiters, keyword)
        attribute_list_embedding = read_information.get_attribute_list_embedding()
        keyword_embedding = []
        question_range = []
        for i in range(attribute_size):
           question_range.append(0)
        for k in keyword:
            keyword_embedding.append(tools.get_sentence_embedding(k))
        #（keyword的每一个关键词与一个attribute中的[每一个attri_embedding算余弦相似度]，）求和作为一个attribute的结果
        #key 【0】【1】【2】 attri 0[0][1][2] 1[0][1][2] 3[0][1][2] 
        # 【0】【1】【2】与0[0][1][2] 计算求和作为一个结果
        if E == "embedding_list -sum":
            for i in range(len(attribute_list_embedding)):
                for k_embedding in keyword_embedding:
                    question_range[i] += sum(prior_classify(attribute_list_embedding[i], k_embedding))
            return question_range
        #一个keyword与所有行所有列的embedding计算余弦相似度，对每一行求sum，取最大的【10】个attribute，为他们的权值+1
        #key 【0】【1】【2】 attri 0[0][1][2] 1[0][1][2] 3[0][1][2] 
        # 【0】与 0[0][1][2] 1[0][1][2] 3[0][1][2] 分别计算分别求和得到0的res,1的res,2的res,对question_range[maxres的index]+1
        elif E == "embedding_list -max":

            for k_embedding in keyword_embedding:
                result = []
                for index, attribute_embedding in enumerate(attribute_list_embedding):
                    result.append(sum(prior_classify(attribute_embedding, k_embedding)))
                for rangei in range(0.1*len(attribute_list_embedding)):
                    max_value = max(result)
                    max_index = result.index(max_value)
                    result[max_index] = 0
                    question_range[max_index] += 1
            return question_range

def narrow_question_range(file:str, file_index = -1, true_range = -1)->list[int]:
    
    kw = []
    y1_class = []
    y2_class = []

    size = read_information.get_size()
    #stime = time.time()
    #基于关键词提取缩小提问范围
    keyword = keyword_extraction_by_llm(file)

    kw.append(keyword)
    #keyword = re.split(delimiters, keyword)
    question_range = get_range(keyword)
    keyword_narrow_question_num = (int)(keyword_narrow_question*size)
    #y_class 缩小范围后的问题索引
    y_class = []
    for i in range(keyword_narrow_question_num):
        max_value = max(question_range)
        max_index = question_range.index(max_value)
        question_range[max_index] = 0
        y_class.append(max_index)
        y1_class.append(max_index)
    #基于词频统计缩小提问范围
    keyword = keyword_extraction_by_TF_IDF(file)
    tmpkeyword = keyword[0:int(len(keyword)*0.1)]
    keyword = ""
    for word in tmpkeyword:
        keyword += "," + word
    keyword = keyword[1:]
    kw.append(keyword)
    extract_narrow_question_num = (int)(extract_narrow_question*size)

    question_range = get_range(keyword)
    for i in range(extract_narrow_question_num):
        max_value = max(question_range)
        max_index = question_range.index(max_value)
        question_range[max_index] = 0
        y_class.append(max_index)
        y2_class.append(max_index)

    #储存信息

    max_index = file_index
    if max_index != -1 and true_range != -1:
        file_path = language+'/info/narrow_result/%d.txt'%max_index
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(true_range)+'\n')
            if true_range in y_class:
                file.write("成功\n")
            else:
                file.write("失败\n")
            for yclass in y1_class:
                file.write((str)(yclass))
                file.write(" ")
            file.write("\n")
            file.write(kw[0])
            file.write("\n")
            for yclass in y2_class:
                file.write((str)(yclass))
                file.write(" ")
            file.write("\n")
            file.write(kw[1])
            file.write("\n")
        y_calss = list(set(y_class))
        file.close()
    #etime = time.time()
    #print("%f %d"%(etime-stime, len(y_class)))

    return y_class



#词频统计
def keyword_extraction_by_TF_IDF(text:str)->list[str]:
    # 使用jieba进行分词
    words = ' '.join(jieba.cut(text))
    # 创建TF-IDF向量化器，并设置参数只提取单个词
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 1))
    # 将文本转化为TF-IDF矩阵
    tfidf_matrix = vectorizer.fit_transform([words])
    # 获取所有词汇
    words = vectorizer.get_feature_names_out()
    # 提取每个词汇的TF-IDF值
    scores = tfidf_matrix.toarray()[0]
    # 将词汇和对应的TF-IDF值组合起来并按得分降序排列
    word_scores = list(zip(words, scores))
    word_scores = sorted(word_scores, key=lambda x: x[1], reverse=True)
    # 打印关键词及其对应的得分
    #for word, score in word_scores:
    #    print(f"{word}: {score}")
    keyword = []
    for word_score in word_scores:
        keyword.append(word_score[0])
    return keyword

def keyword_extraction_by_llm(text:str)->str:
    ps_info = "请不要输出除关键词以外的任何输出.\n"
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": "%s请提取如下文件的关键词：\n%s"%(ps_info, text)
            }
        ],
    )
    message_content = response.choices[0].message.content
    #print(message_content)

    return message_content
