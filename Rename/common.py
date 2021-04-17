import os
def isvalid_symbol(code):
    if ord(code) >=32 and ord(code) <=122:
        return True
    else:
        return False

def strip_chinese_character(base_name):
    new_basename = ''
    for c in base_name:
        if isvalid_symbol(c):
            new_basename += c
    return new_basename