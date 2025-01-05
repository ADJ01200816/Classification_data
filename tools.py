
from setting import *


"""
#########
The following are pre-categorised
#########
"""

# Input string to get word embedding vector
def get_sentence_embedding(sentence:str)->np.ndarray:
    
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    # input must be less than 512 characters/word
    outputs = model(**inputs,output_hidden_states=True) 
    # 0: Get the output of the last layer of BERT (i.e., the vocabulary dimension) and take the average
    if embedding_number == 0:
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    """
    #1: Take the [CLS] token of the last layer.
    if embedding_number == 1:
        embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
    #2
    if embedding_number == 2:
        # Aggregate the output of the last four layers
        mean_hidden_states = [outputs.hidden_states[i].mean(dim=1) for i in [-1, -2, -3, -4]]
        # Each mean is then separated from the computed graph and converted to a NumPy array
        embeddings = [state.detach().numpy() for state in mean_hidden_states]
        embeddings = np.concatenate(embeddings, axis=-1)
    #3
    if embedding_number == 3:
        # Use a simple self-attention mechanism
        attention_scores = torch.matmul(outputs.last_hidden_state, outputs.last_hidden_state.transpose(-1, -2))
        attention_weights = torch.nn.functional.softmax(attention_scores, dim=-1)
        embeddings = torch.matmul(attention_weights, outputs.last_hidden_state).mean(dim=1).detach().numpy()
    """
    return embeddings

import read_information




"""
#########
Here are the big model questions
#########
"""

# Enter short text into llm
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

    ps_info = "Your reply language please use %s. As your answer will be used for batch data processing, the following is the required answer, the named entity in your answer must be complete and exactly the same as the named entity mentioned in the question, the answer to each sentence can only take up one line, if the named entity does not exist, the output:|+Named Entity Name +0, if the named entity exists, the output:|+Named Entity Name +1, the output between each named entity of a single sentence should be separated by | instead of ,split, after processing the current one, immediately change the line. Each named entity output of a single sentence should be separated by | instead of ,, and line break immediately after processing the current question."%(language)
    # Use the official Wisdom Spectrum Clear Speech interface
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
    message_content = response.choices[0].message.content
    #print("end")
    #print(message_content)
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
    # Harmonise the format of named entities
    if(language == 'en'):
        for i, attri in enumerate(attribute):
            attribute[i] = attri.strip().lower()
    return attribute

# Remove special characters from llm returns
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


# Input files and issues, output named entities
def get_attribute(file:str, question_list:list[str],i00=-1)->list[str]:

    question_range = narrow_question_range(file, i00)
    question_list = read_information.get_question(question_range=question_range)
    #print("qlen:%d"%len(question_list))
    attribute = []
    #attribute = invert_index.get_attribute_by_str_matching(question_range, file)
    
    text_list = long_text_split(file)

    for text in text_list:
# llm input max 2048 characters, so need to batch input issues
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