import pickle
import os
from random import randint
from googletrans import Translator
#pip install googletrans==3.1.0a0


word_len_first_time = True
word_cat_first_time = True
dict_len_word = None
dict_cat_word = None

def load_words_sorted_by_len():
    '''loads a dictionnary containing french words sorted by len'''

    p = os.path.abspath('./dict/french_dict1.pkl')
    with open(p, 'rb') as d:
        mots = pickle.load(d)
    
    return mots

def get_words_sorted_by_len(word_len):

    """trouve un mot de longeur donnee"""

    global word_len_first_time
    global dict_len_word

    try:
        word_len = int(word_len)
    except: return ["La longeur doit etre un nombre", True]

    if word_len_first_time:
        dict_len_word = load_words_sorted_by_len()
        word_len_first_time = False
    
    if word_len in list( dict_len_word):
        word = dict_len_word[word_len][randint(0, len(dict_len_word[word_len])-1)]
        # indique s'il y a une erreur
        # erreur = False
        return [word, False]
    else:
        return ['On ne sait pas de mot de cette longeur. Veuillez choisir une autre longueur', True]
    
def get_words_sorted_by_cat(categorie, dict_cat_word, nlp):
    """trouve un mot de categorie donnee"""

    global word_cat_first_time

    try:
        int(categorie)
        return ["La categorie doit etre un mot", True]
    except: pass

    translator = Translator()
    categorie1 = translator.translate(categorie, src = 'fr', dest='en').text
    try:
        for i in range(5):
            word = dict_cat_word.most_similar(categorie1, topn = 3)[randint(0,4)][0]
            word = translator.translate(word, src = 'en', dest='fr').text
            if (nlp(word)[0].lemma_) != (nlp(categorie)[0].lemma_):
                break
        
        return [word, False]
    
    except:
        return ["Cette categorie n'existe pas, veillez choisir un autre mot", True]
    