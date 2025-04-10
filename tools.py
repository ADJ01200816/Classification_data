
from setting import *
from pre_classify import *

"""
#########
The following are pre-categorized
#########
"""

# Input string to get word embedding vector
def get_sentence_embedding(sentence:str)->np.ndarray:
    
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    # input must be less than 512 characters/word
    outputs = model(**inputs,output_hidden_states=True) 
    #0: Get the output of the last layer of BERT (i.e., the lexical dimension) and average it
    if embedding_number == 0:
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
  
    return embeddings

import read_information




"""
#########
Here are the big model questions
#########
"""

#将短文本输入llm
def small_file_to_llm(file_str:str, question_str_list:list[str])->list[str]:

    stime = time.time()
    language = ""
    if(language == 'cn'):
        language = "Chinese"
    elif (language == 'en'):
        language = "All lowercase English"
    question_str = ""
    for index, question in enumerate(question_str_list):
        question_str = question_str + "q%d:" % (index+1)
        question_str = question_str + question + '\n'

    ps_info = "Please use %s for your reply language. Since your reply will be used for batch data processing, the following is the required reply, the named entity in the information in your reply must be complete and exactly the same as the named entity mentioned in the question, the reply can only take up one line for each sentence, if the named entity doesn't exist, the output will be :|+Named Entity Name + 0, if the named entity exists, the output will be :|+Named Entity Name +1, the output will be separated by | instead of ,split, immediately change the line after processing the current one. Each named entity output of a single sentence should be separated by | instead of ,, and the current question should be processed immediately after the new line "%(language)
    #使用智谱清言官方接口
    print("%s.file C:\n%s.file as above. Please answer the questions for each of the following problem sets. Problem Set: \n%s" % (ps_info, file_str, question_str))
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": "%s.file C:\n%s.file as above. Please answer the questions for each of the following problem sets. Problem Set: \n%s" % (ps_info, file_str, question_str)
            }
        ],
    )
    #print("\n\n\n\n")
    message_content = response.choices[0].message.content
    #print("end")
    print(message_content)
    etime = time.time()
    #print(etime-stime)
    return llm_text_handle(message_content)

# Process llm returns into a list of named entities
def llm_text_handle(text:str)->list[str]:
    attribute = []
    str_list = text.split('\n')
    # Split the answer to llm for each named entity
    for str in str_list:
        if '|' in str:
            tmp = str.split('|')
            for tmpp in tmp:
                if '1' in tmpp and 'q' not in tmpp.split('1')[0]:
                    attribute.append(tmpp.split('1')[0].strip())
    # Harmonize named entity formats
    if(language == 'en'):
        for i, attri in enumerate(attribute):
            attribute[i] = attri.strip().lower()
    return attribute

# llm return content processing to remove special characters
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


# To be added
def long_text_split(file):
    file_list = []
    file_list.append(file)
    return file_list


# Input files and issues, output named entities
def get_attribute(file:str, question_list:list[str],i00=-1)->list[str]:

    question_range = narrow_question_range(file, i00)
    question_list = read_information.get_question(question_range=question_range)
    #print("qlen:%d"%len(question_list))
    attribute = []
    #attribute = invert_index.get_attribute_by_str_matching(question_range, file)
    
    text_list = long_text_split(file)

    for text in text_list:
# llm input max number of characters is 2048, so need to batch input issues
        for qi in range(len(question_list)//max_question):
            q = question_list[qi*max_question:(qi+1)*max_question]
            answer = small_file_to_llm(file,q)
            for attri in answer:
                attri = llm_text_handle2(attri)
                attribute.append(attri)
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
    # Check if the path exists
    if os.path.exists(path):
        # Iterate over files and folders in a directory
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                # If it's a file, just delete it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # If it's a directory, recursively delete
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        print('The path %s does not exist' % path)

def get_4_args(levels, true_levels, false_levels):
    index = []
    size = 0
    for j in range(10):
        if levels[j] != 0:
            index.append(j)
            size += levels[j]
    #Calculate accuracy, precision, recall, f1 scores
    accuracy = 0
    precision = 0
    recall = 0
    f1 = 0
    for i in index:
        accuracy += true_levels[i]
        precision += true_levels[i]/(true_levels[i]+false_levels[i])
        recall += true_levels[i]/levels[i]
    
    accuracy = accuracy/size
    precision = precision/len(index)
    recall = recall/len(index)
    if(precision == 0 or recall == 0):
        f1 = 0
    else:
        f1 = 2*precision*recall/(precision+recall)

    return accuracy, precision, recall, f1

    


