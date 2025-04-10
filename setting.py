

from outdependence import *

#bert log message hiding
logging.set_verbosity_error()
# Configure the logging module to disable logging from jieba.
logging.get_logger('jieba').setLevel(logging.ERROR)

# Some fixed parameter settings
language = 'en'
#Choose Chinese/English    'cn'/'en'

#re.split parameter, split string
delimiters = r'[,，、]'

# Parameters related to narrowing the problem
embedding_number = 0
keyword_narrow_question = 0.15
extract_narrow_question = 0.05

#Machine learning related parameters
vectorizer = TfidfVectorizer()
knn_number = 3
skmodel_number = 1

# Minimum support for inverted indexing, greater than this percentage added to the set of categorized results
min_approval_rate = 0.8

# Single pass to llm max issues, max number of files
max_question = 20
small_file_len = 5120

# personal api needed to call the model
api = "f2ca63ccab3f49d1bea0b79642aa0fd5.It6zGnIIyMYFc0kW"
client = ZhipuAI(api_key=api)
llm_model = "glm-4-plus"

#bert model parameters
model_name = "bert-base-cased"
if language == "cn":
    model_name = "bert-base-chinese"
####Compare and contrast different models####
#en：bert-base-cased/bert-large-cased   roberta-base/roberta-large
#cn：bert-base-chinese
#common (use)：bert-base-multilingual-cased
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

E = "embedding"

dataset_path = 'Finance'
#dataset_path = 'Medical'
#dataset_path = 'NewEnergyVehicles'