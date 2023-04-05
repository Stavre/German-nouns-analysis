import re

import pandas as pd


def process_field(fields):
    if isinstance(fields, str):
        return re.findall("\[.*?\]", fields)[0].replace('[', '').replace(']', '')
    else:
        # print(type(fields), fields)
        return 'no field'

def get_ending(word: str, terminations: dict):
    for key,val in terminations.items():
        if word.endswith(key) is True:
            return key
    return "no special ending"

def predicted_gender(word: str, terminations: dict):
    for key,val in terminations.items():
        if word.endswith(key) is True:
            return val
    return "could not predict gender"


def eval_word(word: str, actual_gender: str, terminations: dict):
    for key,val in terminations.items():
        if word.endswith(key) is True:
            if actual_gender == val:
                return 0
            else:
                return 1
    return 2

def process_tags(path):
    tags = pd.read_csv(path, sep='\t')
    res = list(zip(*tags.index))
    # print(res)
    t = dict(zip(res[0], list(map(lambda x: x.split(" / ")[0], res[1]))))
    #print(t.keys())


    return t


def assign_to_dict(row, dictionary):
    dictionary[row['field']] = row['word']




if __name__ == '__main__':
    process_tags("resources/tags.txt")