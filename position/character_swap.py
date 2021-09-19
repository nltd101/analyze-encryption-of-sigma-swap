from os import replace
from typing import Any
import pandas as pd
s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
# (1)->(4)->(3)->(1)
# (2)->(5)->(2)
sigma = [3, 5, 4, 1, 2]
# sigma[i] is index of character moved to i
key = {"a": "k", "b": "s", "c": "l", "d": "m", "e": "b", "f": "d", "g": "a", "h": "r", "i": "p", "j": "e", "k": "f", "l": "u", "m": "x",
       "n": "z", "o": "i", "p": "g", "q": "j", "r": "t", "s": "y", "t": "c", "u": "n", "v": "o", "w": "q", "x": "h", "y": "v", "z": "w", }


def remove_accents(input_str):
    s = ''

    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def preprocess_data(filepath: str):
    f = open(filepath, 'r')
    data = f.read()
    f = open(filepath, 'w')

    f.write("".join([c.lower() for c in data if c in key or c.lower() in key]))


def remove_accents_of_file(filepath: str):
    f = open(filepath, 'r')
    data = f.read()
    f = open(filepath, 'w')
    data = remove_accents(data)

    print(data)
    f.write(data)


def encrypt_file(filepath: str, newpath: str, key: dict):
    f = open(filepath, 'r')
    data = f.read()
    result = []
    for i in range(len(data)):
        c = data[i]
        if c in key:
            result.append(key[c])
        elif c.lower() in key:
            result.append(key[c.lower()])
        # else:
        #     result.append(c)

    f = open(newpath, 'w')
    f.write("".join(result))


def analysis(data_path, analysis_path, n):
    f = open(data_path, 'r')
    data = f.read()
    dictionary: dict = {}
    amount_word = 0
    words = [data[i:i+n] for i in range(0, len(data), n)]
    print(words)

    for word in words:
        amount_word += 1
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary.update({word: 1})
        key_list: list = list(dictionary.keys())
        key_list.sort(key=lambda x: -dictionary[x])
    newdf = pd.DataFrame({"word": key_list, "portion": [
        round(dictionary[key]*100/amount_word, 2) for key in key_list]})
    newdf.to_csv(analysis_path, index=False)


# remove_accents_of_file("data.txt")
# encrypt_file("plaintext.txt", "ciphertext.txt", key)
preprocess_data("data.txt")
analysis("data.txt", 'data_analysis_1.csv', 1)
analysis("data.txt", 'data_analysis_2.csv', 2)
analysis("data.txt", 'data_analysis_3.csv', 3)
