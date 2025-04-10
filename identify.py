

import classify
import pre_classify
from setting import *
import read_information
import tools
        

# Test classification results
def identify_classify():
    levels = []
    true_levels = []
    false_levels = []
    for i in range(10):
        levels.append(0)
        true_levels.append(0)
        false_levels.append(0)
    level_accuracy = 0
    name_accuracy = 0
    two_accuracy = 0

    example_level, example_name = read_information.get_example_info()

    for tmplevel in example_level:
        levels[tmplevel] += 1

    path = 'Datasets/' + dataset_path + '/' + language + '/Text_files'
    size = tools.count_files_in_directory(path)-1
    print(size)
    attribute_list = []
    for i in range(size):
        file_path = 'middle_data/' + dataset_path + '/' + language + '/attribute/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.read()
        file.close()
        attribute_list.append(file_info.split(','))
    print("invert_index/trie_tree:")

    #tools.clear_folder(language + '/info/classify_result/invert_index_result')
    for index, attribute in enumerate(attribute_list):
        if language == 'cn':
            level, name_list = classify.use_invert_index(attribute)
        else:
            level, name_list = classify.use_trie_tree(attribute)
        if level < 3:
            if example_level[index] < 3:
                two_accuracy += 1
        else:
            if example_level[index] >= 3:
                two_accuracy += 1
        if example_level[index] <= level:
            level_accuracy += 1

        if example_level[index] == level:
            true_levels[example_level[index]] += 1
        else:
            false_levels[example_level[index]] += 1

        if example_name[index] in name_list:
            name_accuracy += 1
            if example_level[index] != level:
                print(name_list)
        
        # file_path = ''
        # if language == 'cn':
        #     file_path = language + '/info/classify_result/invert_index_result/%d.txt'%index
        # elif language == 'en':
        #         file_path = language + '/info/classify_result/trie_tree_result/%d.txt'%index

        # with open(file_path, 'w', encoding='utf-8') as file:
        #     file.write(str(level)+'\n')
        #     for name in name_list:
        #         file.write(name+',')

    print("two_accuracy:%.4f"%(two_accuracy/size))
    print("level_accuracy:%.4f"%(level_accuracy/size))
    print("name_accuracy:%.4f"%(name_accuracy/size))

    print(levels)
    print(true_levels)
    print(false_levels)

    print(tools.get_4_args(levels, true_levels, false_levels))

    print("sklearn_model:")

    for i0 in range(1, 8, 1):
        true_levels = []
        false_levels = []
        for j in range(10):
            true_levels.append(0)
            false_levels.append(0)
        level_accuracy = 0
        print(i0)
        level = classify.use_sklearn_model(attribute_list, number=i0)
        for i in range(size):
            if(level[i] == example_level[i]):
                level_accuracy += 1
                true_levels[example_level[i]] += 1
            else:
                false_levels[example_level[i]] += 1
        print("level_accuracy:%.4f"%(level_accuracy/size))
        print(tools.get_4_args(levels, true_levels, false_levels))

    

    
# Test pre-categorization results
def identify_pre_classify():
    if input("Whether to empty the pre-categorized information folder \n1:Yes \n0:No \n") == '1':
        #tools.clear_folder(language+'/info/narrow_result')
        print("Emptying complete.")

    pre_classify_accuracy = 0
    example_level, example_name = read_information.get_example_info()
    size = len(example_name)
    name = read_information.get_name()
    for i in range(size):
        index = name.index(example_name[i])

        file_path = 'Datasets/' + dataset_path + '/' + language + '/data/Text_files/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.read()
        file.close()
        pre_classify_result = pre_classify.narrow_question_range(file_info, file_index = i, true_range = i)

        if index in pre_classify_result:
            pre_classify_accuracy += 1
    print("pre_classify_accurancy%.4f"%(pre_classify_accuracy/size))
        


#Batch processing of files into attributes
def file_handle_to_attribute():
    s_time = time.time()
    path = language + '/data/Text_files'
    size = tools.count_files_in_directory(path)-1
    for i in range(size):
        file_path = language + '/data/attribute/%d.txt'%i
        if(os.path.exists(file_path)):
            continue

        print("%dstart"%i)

        file_path = 'Datasets/' + dataset_path + '/' + language + '/Text_files/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.read()
        file.close()
        attribute = classify.use_llm_get_attribute(file_info)
        
        file_path = 'middle_data/' + dataset_path + '/' + language + '/attribute/%d.txt'%i
        attri_str = ''
        for attri in attribute:
            attri_str += ',' + attri
        attri_str = attri_str[1:]
        with open(file_path, 'w', encoding='utf-8') as file:  
            file.write(attri_str)  # Write data to file
        file.close()
    identify_classify()
    e_time = time.time()
    print((e_time-s_time)/size)

identify_classify()