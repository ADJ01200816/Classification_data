
from setting import *
import read_information
import classify

f_model = classify.use_invert_index

def Main(file):
    s_time = time.time()
    file_attribute = classify.use_llm_get_attribute(file)
    print(f_model(file_attribute))
    e_time = time.time()
    print(e_time-s_time)

Main("在这片繁华的城市中，有一位名叫张伟的男士，他的国籍是中国。根据《海外账户纳税法案》（FATCA）的相关规定，他提供了自己的身份信息，以证明其合规性。张伟，性别男，汉族，已婚，他持有的是中华人民共和国居民身份证。证件号码为110105197001012345，证件生效日期为2005年1月1日，有效期至2025年12月31日。他的家庭住址位于北京市朝阳区幸福路88号院2号楼3单元402室。在这里，他与妻子共同守护着他们温馨的小家，度过了一个又一个美好时光。")

