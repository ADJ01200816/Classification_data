
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

Main("1234567")

