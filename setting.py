from outdependence import *

# Hide bert log information
logging.set_verbosity_error()
# Configure the logging module to turn off jieba's log output
logging.get_logger('jieba').setLevel(logging.ERROR)

# Some fixed parameter settings
language = 'cn'
# Choose Chinese/English 'cn'/'en'

# re.split parameters for splitting strings
delimiters = r'[,，、]'

# Narrow down question-related parameters
embedding_number = 0
keyword_narrow_question = 0.15
extract_narrow_question = 0.05

# Machine learning related parameters
vectorizer = TfidfVectorizer()
knn_number = 3
skmodel_number = 1

# Inverted index minimum support rate, inclusion in the classification result set if greater than this percentage
min_approval_rate = 0.8

# Maximum number of questions per transmission to LLM, maximum file length
max_question = 20
small_file_len = 5120

# Personal API required for model calls
api = "831ac485fe42e3d431436d1df649898e.zP0fizGqqW6tENOD"
client = ZhipuAI(api_key=api)
llm_model = "glm-4-0520"

# BERT model parameters
model_name = "bert-base-cased"
if language == "cn":
    model_name = "bert-base-chinese"
#### Compare different models ####
# English: bert-base-cased/bert-large-cased   roberta-base/roberta-large
# Chinese: bert-base-chinese
# Universal: bert-base-multilingual-cased
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

E = "embedding"

