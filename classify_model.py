
from setting import *
import read_information

#建立模型
def build_model(number = skmodel_number):
    
    text = read_information.get_attribute()

    label = read_information.get_level()
    data = {'text': text, 'label': label}
    df = pd.DataFrame(data)
    
    # 所有数据都用于训练集
    X_train = df['text']
    y_train = df['label']
    X_train = vectorizer.fit_transform(X_train)

    """
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
    X_train = setting.sklearn_setting.vectorizer.fit_transform(X_train)
    X_test = setting.sklearn_setting.vectorizer.fit_transform(X_test)
    """
    # 训练模型
    if number == 1:
        model =  KNeighborsClassifier(n_neighbors=knn_number)
        print("KNN")
    elif number == 2:
        model = DecisionTreeClassifier()
        print("DECISION TREE")
    elif number == 3:
        model = SVC(kernel='linear')  # 你可以选择其他核函数，例如 'rbf'，'poly' 等
        print("SVM")
    elif number == 4:
        model = LogisticRegression()
        print("逻辑回归")
    elif number == 5:
        model = RandomForestClassifier()
        print("随机森林")
    elif number == 6:
        model = MultinomialNB()
        print("朴素贝叶斯")
    elif number == 7:
        model = GradientBoostingClassifier()
        print("梯度提升机")
    else:
        print("无效number")
        exit()

    model.fit(X_train, y_train)
    
    # 预测与评估（这里没有测试集，所以使用训练集进行预测，这仅用于示例，不推荐用于实际模型评估）
    #y_pred = model.predict(X_train)
    """
    for i in range(len(y_pred)):
        print(y_pred[i])
        print(y_train[i])
        print("\n")
    """
    # 计算并显示准确率
    #accuracy = accuracy_score(y_train, y_pred)
    #print("Accuracy:", accuracy)
    return model

#倒排索引（字典）的建立
def build_invert_index():
    dictionary = {}
    names = read_information.get_name()
    attribute_lists = read_information.get_attribute_list()
#统一格式
    if(language == 'en'):
        for i, attribute_list in enumerate(attribute_lists):
            for j, attribute in attribute_list:
                attribute_lists[i][j] = attribute.strip().lower()
        for i, name in enumerate(names):
            names[i] = name.strip().lower()

    for i in range(len(names)):
        for attribute in attribute_lists[i]:
            if attribute not in dictionary:
                dictionary[attribute] = []
            dictionary[attribute].append(names[i])
    return dictionary

#trie树的数据结构
class node:
    def __init__(self):
        self.children = {}
        self.end = False
    
    #递归依次插入每个字母
    def insert(self, word, information, num = 0):
        if num == len(word):
            self.end = True
            if 10 not in self.children:
                self.children[10] = []
            self.children[10].append(information)
            return True
        if word[num] not in self.children:
            self.children[word[num]] = node()
        return self.children[word[num]].insert(word, information, num+1)
    
    #递归查找每一字母
    def search(self, word, num = 0):
        if num == len(word) and self.end == True:
            return self.children[10]
        if num == len(word) and self.end == False:
            #print("%s不在trie树中"%word)
            return None
        if word[num] in self.children:
            return self.children[word[num]].search(word, num+1)
            return self.children[word[num]].search(word, num+1)
        return None

    #遍历trie树
    def order(self, str = ""):
        if self.end == True:
            print(str)
            for i in self.children[10]:
                print(i)
            print('\n')
        for key, value in self.children.items():
            if key == 10:
                continue
            else:
                value.order(str+key)
        return
            
#建立trie树
def build_trie_tree():
    name = read_information.get_name(language='en')
    attribute = read_information.get_attribute(language='en')
    trie_tree = node()
    for i in range(len(name)):
        #分割命名实体并依次插入
        attri_list = re.split(setting.delimiters,attribute[i])
        for attri in attri_list:
            attri = attri.strip()
            trie_tree.insert(attri, name[i])
    return trie_tree



    
