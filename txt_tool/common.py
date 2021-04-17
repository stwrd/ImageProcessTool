import os



#匹配文本中符合搜索字符串的目标行，并提取出来
def searchTxtFile(target_file,target_str):
    dst_str = ''
    with open(target_file,'rt') as f:
        data = f.readlines()
        for str in data:
            if target_str in str:
               dst_str += str
    print(dst_str)
    return dst_str