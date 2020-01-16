import os
import random
result_file1=r'/media/hzh/work/workspace/data/1301_delete_result.txt'
result_file2=r'/media/hzh/work/workspace/data/1301_keep_result.txt'

with open(result_file1,encoding='UTF-8') as f:
    results1=f.readlines()

with open(result_file2,encoding='UTF-8') as f:
    results2=f.readlines()

results = results1+results2
random.shuffle(results)

results_file = r'/media/hzh/work/workspace/data/result_1301.txt'
with open(results_file,mode='w',newline='\n',encoding='UTF-8') as f:
    for l in results:
        f.write(l)