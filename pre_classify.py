
from setting import *
import tools
import read_information


def preprocess_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


# Input list of categories and targets, calculate cosine similarity
def prior_classify(classify_embedding:list[np.ndarray], material_embedding:np.ndarray)->list[float]:
    ret_level = []
    for embedding in classify_embedding:
       value_similarity = cosine_similarity(embedding, material_embedding)[0][0]
       ret_level.append(value_similarity)
    return ret_level

#Enter keywords to get questions narrowed down
def get_range(keyword:str)->list[int]:

    attribute_size = read_information.get_size()
    #embedding/embedding_list -sum/embedding_list -max
    # Keyword sentences and attribute sentence calculations
    if(E == "embedding"):
        attribute_embedding = read_information.get_attribute_embedding()
        keyword_embedding = tools.get_sentence_embedding(keyword)
        return prior_classify(attribute_embedding, keyword_embedding)
    #Keyword words and attribute word calculation
    else:
        keyword = re.split(delimiters, keyword)
        attribute_list_embedding = read_information.get_attribute_list_embedding()
        keyword_embedding = []
        question_range = []
        for i in range(attribute_size):
           question_range.append(0)
        for k in keyword:
            keyword_embedding.append(tools.get_sentence_embedding(k))

        if E == "embedding_list -sum":
            for i in range(len(attribute_list_embedding)):
                for k_embedding in keyword_embedding:
                    question_range[i] += sum(prior_classify(attribute_list_embedding[i], k_embedding))
            return question_range
 
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
    # Narrow down questions based on keyword extraction
    keyword = keyword_extraction_by_llm(file)

    kw.append(keyword)
    #keyword = re.split(delimiters, keyword)
    question_range = get_range(keyword)
    keyword_narrow_question_num = math.ceil(keyword_narrow_question*size)
    print(keyword_narrow_question_num)
    #y_class Narrowed down index of issues
    y_class = []
    for i in range(keyword_narrow_question_num):
        max_value = max(question_range)
        max_index = question_range.index(max_value)
        question_range[max_index] = 0
        y_class.append(max_index)
        y1_class.append(max_index)
    # Narrow down questions based on word frequency statistics
    keyword = keyword_extraction_by_TF_IDF(file)
    tmpkeyword = keyword[0:int(len(keyword)*0.1)]
    keyword = ""
    for word in tmpkeyword:
        keyword += "," + word
    keyword = keyword[1:]
    kw.append(keyword)
    extract_narrow_question_num = math.ceil(extract_narrow_question*size)
    print(extract_narrow_question_num)
    question_range = get_range(keyword)
    for i in range(extract_narrow_question_num):
        max_value = max(question_range)
        max_index = question_range.index(max_value)
        question_range[max_index] = 0
        y_class.append(max_index)
        y2_class.append(max_index)

    # Stored information

    # max_index = file_index
    # if max_index != -1 and true_range != -1:
    #     file_path = language+'/info/narrow_result/%d.txt'%max_index
    #     with open(file_path, 'w', encoding='utf-8') as file:
    #         file.write(str(true_range)+'\n')
    #         if true_range in y_class:
    #             file.write("成功\n")
    #         else:
    #             file.write("失败\n")
    #         for yclass in y1_class:
    #             file.write((str)(yclass))
    #             file.write(" ")
    #         file.write("\n")
    #         file.write(kw[0])
    #         file.write("\n")
    #         for yclass in y2_class:
    #             file.write((str)(yclass))
    #             file.write(" ")
    #         file.write("\n")
    #         file.write(kw[1])
    #         file.write("\n")
    #     y_calss = list(set(y_class))
    #     file.close()
    #etime = time.time()
    #print("%f %d"%(etime-stime, len(y_class)))
    y_class = list(set(y_class))
    return y_class



#Word frequency statistics
def keyword_extraction_by_TF_IDF(text:str)->list[str]:
    # Segmentation using jieba
    words = ' '.join(jieba.cut(text))
    # Create TF-IDF vectorizer and set parameters to extract only single words
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 1))
    # Convert text into TF-IDF matrices
    tfidf_matrix = vectorizer.fit_transform([words])
    # Get all the words
    words = vectorizer.get_feature_names_out()
    # Extract TF-IDF values for each word
    scores = tfidf_matrix.toarray()[0]
    # Combine words and corresponding TF-IDF values and rank them in descending order of score
    word_scores = list(zip(words, scores))
    word_scores = sorted(word_scores, key=lambda x: x[1], reverse=True)
    # Print keywords and their corresponding scores
    #for word, score in word_scores:
    #    print(f"{word}: {score}")
    keyword = []
    for word_score in word_scores:
        keyword.append(word_score[0])
    return keyword

def keyword_extraction_by_llm(text:str)->str:
    ps_info = "Please do not output anything other than keywords.\n"
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": "%sPlease extract the keywords from the following file:\n%s"%(ps_info, text)
            }
        ],
    )
    message_content = response.choices[0].message.content
    #print(message_content)

    return message_content
