
from setting import *
import read_information

#Modelling
def build_model(number = skmodel_number):
    
    text = read_information.get_attribute()

    label = read_information.get_level()
    data = {'text': text, 'label': label}
    df = pd.DataFrame(data)
    
    # All data used for training set
    X_train = df['text']
    y_train = df['label']
    X_train = vectorizer.fit_transform(X_train)

    """
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
    X_train = setting.sklearn_setting.vectorizer.fit_transform(X_train)
    X_test = setting.sklearn_setting.vectorizer.fit_transform(X_test)
    """
    # Training models
    if number == 1:
        model =  KNeighborsClassifier(n_neighbors=knn_number)
        print("KNN")
    elif number == 2:
        model = DecisionTreeClassifier()
        print("DECISION TREE")
    elif number == 3:
        model = SVC(kernel='linear')  # You can choose other kernel functions, e.g. ‘rbf’, ‘poly’ etc.
        print("SVM")
    elif number == 4:
        model = LogisticRegression()
        print("logistic regression")
    elif number == 5:
        model = RandomForestClassifier()
        print("random forest")
    elif number == 6:
        model = MultinomialNB()
        print("Naive Bayes")
    elif number == 7:
        model = GradientBoostingClassifier()
        print("GBM")
    else:
        print("Invalid number")
        exit()

    model.fit(X_train, y_train)
    
    # Prediction and Evaluation (there is no test set here, so predictions are made using the training set, which is used for example purposes only and is not recommended for actual model evaluation)
    #y_pred = model.predict(X_train)
    """
    for i in range(len(y_pred)):
        print(y_pred[i])
        print(y_train[i])
        print("\n")
    """
    # Calculate and display accuracy
    #accuracy = accuracy_score(y_train, y_pred)
    #print("Accuracy:", accuracy)
    return model

# Building of inverted indexes (dictionaries)
def build_invert_index():
    dictionary = {}
    names = read_information.get_name()
    attribute_lists = read_information.get_attribute_list()
# Uniform format
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

# trie tree data structure
class node:
    def __init__(self):
        self.children = {}
        self.end = False
    
    # Recursively insert each letter in turn
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
    
    # Recursively find each letter
    def search(self, word, num = 0):
        if num == len(word) and self.end == True:
            return self.children[10]
        if num == len(word) and self.end == False:
            
            return None
        if word[num] in self.children:
            return self.children[word[num]].search(word, num+1)
            return self.children[word[num]].search(word, num+1)
        return None

    # Traverse the trie tree
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
            
# Build a trie tree
def build_trie_tree():
    name = read_information.get_name(language='en')
    attribute = read_information.get_attribute(language='en')
    trie_tree = node()
    for i in range(len(name)):
        # Split named entities and insert them in sequence
        attri_list = re.split(setting.delimiters,attribute[i])
        for attri in attri_list:
            attri = attri.strip()
            trie_tree.insert(attri, name[i])
    return trie_tree



    
