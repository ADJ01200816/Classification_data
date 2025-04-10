
from setting import *

#Read the name of the message
def get_name():
    file_path = 'Datasets/' + dataset_path + '/'+language+'/rules/category_data.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        name = file.readlines()
    file.close()
    for i,str in enumerate(name):
        name[i] = str.strip().lower()
    return name

def get_size():
    name = get_name()
    return len(name)
# Named entities that read information
def get_attribute():
    file_path = 'Datasets/' + dataset_path + '/'+language+'/rules/feature_data.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        attribute = file.readlines()
    file.close()
    for i,str in enumerate(attribute):
        attribute[i] = str.strip().lower()
    return attribute

# Read information levels
def get_level():
    file_path = 'Datasets/' + dataset_path + '/'+language+'/rules/level_data.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        level = file.readlines()
    
    # Convert strings to integers and handle possible conversion errors
    int_level = []
    for str in level:
        str = str.strip() 
        try:
            int_level.append(int(str))
        except ValueError:
            print(f"Cannot convert '{str}' to integer, please check the file content.")
            # Here you can choose to skip invalid entries or perform other error handling
            continue
    
    return int_level

#Constructing questions for llm to ask
def get_question(question_range = []):

    attribute = get_attribute()
    num = len(attribute)
    question = []
    for i in range(num):
        question.append("Please extract the following named entity from Material C:"+attribute[i])
    if question_range != []:
        narrow_question = []
        for index in question_range:
            narrow_question.append(question[index])

        return narrow_question
    return question
# Get the number of named entities per name
def get_attribute_num():
    name = get_name()
    attribute = get_attribute()
    if(language == 'en'):
        for i, attri in enumerate(attribute):
            attribute[i] = attri.strip().lower()
        for i, n in enumerate(name):
            name[i] = n.strip().lower()
    num = []
    for i, attri in enumerate(attribute):
        attri_list = re.split(delimiters,attribute[i])
        num.append(len(attri_list))
    return num

def attribute_handle():
    a = get_attribute()
    for attribute in a:
        attribute = re.split(delimiters, attribute)
        attribute = list(filter(lambda x: x.strip(), attribute))
        for i2 in range(len(attribute)):
            attribute[i2] = attribute[i2].strip().lower()
        attribute = list(set(attribute))
        attribute.sort()
        text = ""
        for attri in attribute:
            text = text + attri + ','
        text = text[0:len(text)-1]
        return text

def get_attribute_list():

    tmp_attri = get_attribute()
    
    attribute_list = []
    for attri in tmp_attri:
        tmp = re.split(delimiters, attri)
        tmp = list(filter(lambda x: x.strip(), tmp)) 
        for i2 in range(len(tmp)):
            tmp[i2] = tmp[i2].strip().lower()

        tmp.sort()
        attribute_list.append(tmp)
    return attribute_list

from tools import get_sentence_embedding
def store_attribute_embedding():
    attribute = get_attribute()
    name = get_name()
    attribute_embedding = []
    for i in range(len(name)):
        attribute_embedding.append(get_sentence_embedding(name[i] + " " + attribute[i]))

    np.savez('middle_data/' + dataset_path + '/' + language + '/embedding/' + (str)(embedding_number) + '.npz', *attribute_embedding)
    return attribute_embedding
    
store_attribute_embedding()
def get_attribute_embedding():
    loaded_data = np.load('middle_data/' + dataset_path + '/' + language + '/embedding/' + (str)(embedding_number) + '.npz')
    attribute_embedding = [loaded_data[f'arr_{i}'] for i in range(len(loaded_data.files))]
    return attribute_embedding




def store_attribute_list_embedding():
    attribute_list = get_attribute_list()
    attribute_list_embedding = []
    for index, attribute in enumerate(attribute_list):
        file_path = 'middle_data/' + dataset_path + '/' + language + '/embedding/attribute_list/' + (str)(index) + '.npz'
        if os.path.exists(file_path):
            continue
        for attri in attribute:
            attribute_list_embedding.append(get_sentence_embedding(attri))
        np.savez(file_path, *attribute_list_embedding)
        attribute_list_embedding = []


def get_attribute_list_embedding():

    attribute = get_attribute()
    attribute_list_embedding = []
    for i in range(len(attribute)):
        file_path = 'middle_data/' + dataset_path + '/' + language + '/embedding/attribute_list/' + (str)(index) + '.npz'
        loaded_data = np.load(file_path)
        attribute_list_embedding.append([loaded_data[f'arr_{i}'] for i in range(len(loaded_data.files))])
    return attribute_list_embedding

def get_example_info()->tuple[list[int], list[str]]:
    file_path = 'Datasets/' + dataset_path + '/' + language + '/Text_files/Data_labels.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        file_info = file.readlines()
    file.close()
    name = []
    level = []
    for info in file_info:
        info = info.split('|')
        level.append(int(info[0]))
        name.append(info[1][0:len(info[1])-1])
    return level, name


if __name__ == '__main__':
    name = get_name()
    attribute = get_attribute()
    level = get_level()
    for i in range(len(name)):
        print(name[i])
        print(attribute[i])
        print(level[i])
        print(' ')
    embedding = get_attribute_embedding()


