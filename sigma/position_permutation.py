import pandas as pd
s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
# (1)->(4)->(3)->(1)
# (2)->(5)->(2)
sigma = [3, 5, 4, 1, 2]
# sigma[i] is index of character moved to i


def remove_accents(input_str):
    s = ''

    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def remove_accents_of_plaintext(filepath: str):
    df = pd.read_csv(filepath)
    list = df['Name']
    list = [remove_accents(name) for name in list]
    df['Name'] = list
    df.pop('Unnamed: 0')
    df.to_csv(filepath, index=False)


def encrypt_name_by_permutation_sigma(name: str, sigma: list):
    words = name.split(" ")
    sequence = "".join(words)
    n_sigma = len(sigma)

    if len(sequence) % n_sigma != 0:
        sequence += " "*(n_sigma-len(sequence) % (n_sigma))

    print(sequence)
    ciphertext = [sequence[i//len(sigma)*len(sigma)+sigma[i % len(sigma)]-1]
                  for i in range(len(sequence))]
    ciphertext = "".join(ciphertext)

    return ciphertext.replace(" ", "")


def analysis_data(data_path, analysis_path):
    df = pd.read_csv(data_path)
    namelist: list[str] = df["Name"]
    dictionary: dict = {}
    amount_word = 0
    for name in namelist:
        words = name.split(" ")
        amount_word += 1

        word = words[0]
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary.update({word: 1})
    key_list: list = list(dictionary.keys())
    key_list.sort(key=lambda x: -dictionary[x])
    newdf = pd.DataFrame({"word": key_list, "portion": [
                         dictionary[key]*100/amount_word for key in key_list]})
    newdf.to_csv(analysis_path, index=False)


def analysis_cipher(data_path, analysis_path, n):
    df = pd.read_csv(data_path)
    namelist: list[str] = df["Name"]
    dictionary: dict = {}
    amount_word = 0
    for name in namelist:
        name = name.replace(" ", "")
        words = [name[i:i+n] for i in range(0, len(name), n)]
        amount_word += 1
        word = words[0]
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary.update({word: 1})
    key_list: list = list(dictionary.keys())
    key_list.sort(key=lambda x: -dictionary[x])
    newdf = pd.DataFrame({"word": key_list, "portion": [
                         dictionary[key]*100/amount_word for key in key_list]})
    newdf.to_csv(analysis_path, index=False)


analysis_data("data.csv", "analysis.csv")
encrypt_file("plaindata.csv", 'cipherdata.csv', sigma)
analysis_cipher("cipherdata.csv", "analysis_cipher1.csv", 1)
analysis_cipher("cipherdata.csv", "analysis_cipher2.csv", 2)
analysis_cipher("cipherdata.csv", "analysis_cipher3.csv", 3)
analysis_cipher("cipherdata.csv", "analysis_cipher4.csv", 4)
analysis_cipher("cipherdata.csv", "analysis_cipher5.csv", 5)
analysis_cipher("cipherdata.csv", "analysis_cipher6.csv", 6)
