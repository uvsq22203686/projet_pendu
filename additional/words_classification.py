import pickle

def sort_words_by_len():
    path = './liste_francais.txt'
    f = {}
    i = 0
    with open(path, 'r') as t:
        lines = t.readlines()

    print(len(lines))

    for line in lines:
        line = line[:-1]
        if line != '':
            l = len(line)
            if l in f.keys():
                f[l].append(line)
            else:
                f[l]=[line]

    with open('../utils/french_dict.pkl', 'wb') as d:
        pickle.dump(f, d)
