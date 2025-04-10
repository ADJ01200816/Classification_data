
import tools 
import classify_model
from setting import *
import read_information
import pre_classify

# Input files and issues, output named entities
def use_llm_get_attribute(file:str)->list[str]:
    stime = time.time()
    question_range = pre_classify.narrow_question_range(file)
    etime = time.time()
    print("%fPre-classification time：%f"%((keyword_narrow_question+extract_narrow_question),(etime-stime)))
    #print(question_range)
    question_list = read_information.get_question(question_range=question_range)
    #print("qlen:%d"%len(question_list))
    attribute = []
    #attribute = invert_index.get_attribute_by_str_matching(question_range, file)
    
    text_list = tools.long_text_split(file)

    for text in text_list:
# llm input max number of characters is 2048, so need to batch input issues
        for qi in range(len(question_list)//max_question):
            q = question_list[qi*max_question:(qi+1)*max_question]
            answer = tools.small_file_to_llm(file,q)
            for attri in answer:
                attri = tools.llm_text_handle2(attri)
                attribute.append(attri)
        if(len(question_list)//max_question == 0):
            q = question_list[:]
            answer = tools.small_file_to_llm(file,q)
            for attri in answer:
                attri = tools.llm_text_handle2(attri)
                attribute.append(attri)

    attribute = list(set(attribute))
    return attribute

def use_invert_index(attribute:list[str])->tuple[int, list[int]]:
    invert_index = classify_model.build_invert_index()
    name = read_information.get_name()
    level = read_information.get_level()
    size = read_information.get_size()
    weight = []
    for i in range(size):
        weight.append(0)
    # Increase the weight of the corresponding information using a backward-rowed index
    for attri in attribute:
        if attri in invert_index:
            name_list = invert_index[attri]
            for info in name_list:
                index = name.index(info)
                weight[index] += 1
    # Filtering eligible information
    return_name = []    
    return_level = 0 
    attribute_num = read_information.get_attribute_num()
    for i in range(size):
        if 1.0 * weight[i] >= min_approval_rate * attribute_num[i]:
            return_name.append(name[i])
            if level[i] > return_level:
                return_level = level[i]
    if(len(return_name) == 0):
        max_index = max(weight)
        for i in range(size):
            if weight[i] == max_index:
                return_name.append(name[i])
                return_level = max(return_level, level[i])
    return return_level, return_name

def use_trie_tree(attribute:list[str])->tuple[int, list[int]]:
    trie_tree = classify_model.build_trie_tree()

    name = read_information.get_name()
    level = read_information.get_level()
    size = read_information.get_size()
    weight = []
    for i in range(size):
        weight.append(0)
    # Use trietree to increase the weight of the corresponding information
    for attri in attribute:
        name_list = trie_tree.search(attri)
        if name_list != None:
            for info in name_list:
                index = name.index(info)
                weight[index] += 1
    # Filtering eligible information
    return_name = []    
    return_level = 0 
    attribute_num = read_information.get_attribute_num()
    for i in range(size):
        if 1.0 * weight[i] >= min_approval_rate * attribute_num[i]:
            return_name.append(name[i])
            if level[i] > return_level:
                return_level = level[i]
    if(len(return_name) == 0):
        max_index = max(weight)
        for i in range(size):
            if weight[i] == max_index:
                return_name.append(name[i])
                return_level = max(return_level, level[i])
    return return_level, return_name

def use_sklearn_model(attribute_list:list[list[str]], number = skmodel_number)->list[int]:
    sklearn_model = classify_model.build_model(number=number)
    level = []
    for attribute in attribute_list:
        tmpattribute = ""
        for attri in attribute:
            tmpattribute += ',' + attri
        tmpattribute = tmpattribute[1:]
        level.append(sklearn_model.predict(vectorizer.transform([tmpattribute]))[0])
    return level
    
