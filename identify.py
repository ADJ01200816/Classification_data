

import classify
import pre_classify
from setting import *
import read_information
import tools
        
#把文件批量处理为attribute
def file_handle_to_attribute():
    path = language + '/data/example'
    size = tools.count_files_in_directory(path)-1
    for i in range(size):
        s_time = time.time()
        file_path = language + '/data/attribute/%d.txt'%i
        if(os.path.exists(file_path)):
            continue

        print("%dstart"%i)

        file_path = language + '/data/example/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.read()
        file.close()
        attribute = classify.use_llm_get_attribute(file_info)
        
        file_path = language + '/data/attribute/%d.txt'%i
        attri_str = ''
        for attri in attribute:
            attri_str += ',' + attri
        attri_str = attri_str[1:]
        with open(file_path, 'w', encoding='utf-8') as file:  # 使用open函数以写入模式打开文件
            file.write(attri_str)  # 将数据写入文件
        file.close()

        e_time = time.time()
        print(e_time-s_time)


#检验分类结果
def identify_classify():
    level_accuracy = 0
    name_accuracy = 0
    example_level, example_name = read_information.get_example_info()

    path = language + '/data/example'
    size = tools.count_files_in_directory(path)-1
    attribute_list = []
    for i in range(size):
        file_path = language + '/data/attribute/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.read()
        file.close()
        attribute_list.append(file_info.split(','))
    print("invert_index/trie_tree:")
    input("enter")

    tools.clear_folder(language + '/info/classify_result/invert_index_result')
    for index, attribute in enumerate(attribute_list):
        if language == 'cn':
            level, name_list = classify.use_invert_index(attribute)
        else:
            level, name_list = classify.use_trie_tree(attribute)
        if example_level[index] <= level:
            level_accuracy += 1
        if example_name[index] in name_list:
            name_accuracy += 1

        file_path = ''
        if language == 'cn':
            file_path = language + '/info/classify_result/invert_index_result/%d.txt'%index
        elif language == 'en':
                file_path = language + '/info/classify_result/trie_tree_result/%d.txt'%index

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(level)+'\n')
            for name in name_list:
                file.write(name+',')


    print("level_accuracy:%.4f"%(level_accuracy/size))
    print("name_accuracy:%.4f"%(name_accuracy/size))
    
    print("sklearn_model:")
    input("enter")

    for i in range(1, 8, 1):
        level_accuracy = 0
        level = classify.use_sklearn_model(attribute_list, number=i)
        for i in range(size):
            if(level[i] == example_level[i]):
                level_accuracy += 1
        print("level_accuracy:%.4f"%(level_accuracy/size))
    
#检验预分类结果
def identify_pre_classify():
    if input("是否清空预分类信息文件夹\n1:是\n0:否\n") == '1':
        tools.clear_folder(language+'/info/narrow_result')
        print("清空完成")

    pre_classify_accuracy = 0
    example_level, example_name = read_information.get_example_info()
    size = len(example_name)
    name = read_information.get_name()
    for i in range(size):
        index = name.index(example_name[i])

        file_path = language + '/data/example/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.read()
        file.close()
        pre_classify_result = pre_classify.narrow_question_range(file_info, file_index = i, true_range = i)

        if index in pre_classify_result:
            pre_classify_accuracy += 1
    print("pre_classify_accurancy%.4f"%(pre_classify_accuracy/size))
        

def info_collect():
    tools.clear_folder(language + '/info/info_collected')
    example_level, example_name = read_information.get_example_info()
    size = len(example_level)
    name = read_information.get_name()
    for i in range(size):
        print(i)
        need_write = 0
        file_path = language + '/info/narrow_result/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.readlines()
        file.close()
        collected_info = str(i) + '预分类'

        if file_info[1] == '成功\n':
            collected_info += '成功,分类'
        else:
            collected_info += '失败,分类'
            need_write = 1
        if language == 'cn':
            file_path = language + '/info/classify_result/invert_index_result/%d.txt'%i
        elif language == 'en':
                file_path = language + '/info/classify_result/trie_tree_result/%d.txt'%i
        with open(file_path, 'r', encoding='utf-8') as file:
            file_info = file.readlines()
        file.close()
        if file_info[0][0] == '0':
            collected_info += '失败'
            need_write = 1
        else:
            c_level = int(file_info[0][0:len(file_info[0])-1])
            c_name = file_info[1].split(',')
            if example_name[i] in c_name:
                collected_info += '成功'
            else:
                collected_info += '失败'
                need_write = 1
        file_path = language + '/info/info_collected/' + collected_info + '.txt'
        if need_write != 0:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(' ')
            file.close()

info_collect()