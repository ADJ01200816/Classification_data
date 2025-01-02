

from outdependence import *

#bert日志信息隐藏
logging.set_verbosity_error()
# 配置 logging 模块，关闭 jieba 的日志输出
logging.get_logger('jieba').setLevel(logging.ERROR)

#一些固定参数的设置
language = 'cn'
#选择中/英文    'cn'/'en'

#re.split参数，分割字符串
delimiters = r'[,，、]'

#缩小问题相关参数
embedding_number = 0
keyword_narrow_question = 0.15
extract_narrow_question = 0.05

#机器学习相关参数
vectorizer = TfidfVectorizer()
knn_number = 3
skmodel_number = 1

#倒排索引最小支持率，大于大于这个百分比加入分类结果集合
min_approval_rate = 0.8

#单次传递给llm最大问题,最长文件数量
max_question = 20
small_file_len = 5120

#调用模型所需的个人api
api = "831ac485fe42e3d431436d1df649898e.zP0fizGqqW6tENOD"
client = ZhipuAI(api_key=api)
llm_model = "glm-4-0520"

#bert模型参数
model_name = "bert-base-cased"
if language == "cn":
    model_name = "bert-base-chinese"
####对比不同模型####
#英：bert-base-cased/bert-large-cased   roberta-base/roberta-large
#中：bert-base-chinese
#通用：bert-base-multilingual-cased
model = BertModel.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

E = "embedding"

