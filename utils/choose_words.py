import pickle
import os
from random import randint
import gensim.downloader
from googletrans import Translator
#pip install googletrans==3.1.0a0


word_len_first_time = True
word_cat_first_time = True
dict_len_word = None
dict_cat_word = None

def load_words_sorted_by_len():
    p = os.path.abspath('./dict/french_dict1.pkl')
    with open(p, 'rb') as d:
        mots = pickle.load(d)
    
    return mots

def get_words_sorted_by_len(word_len):
    #+ assert word_len-> int
    global word_len_first_time
    global dict_len_word

    if word_len_first_time:
        dict_len_word = load_words_sorted_by_len()
        word_len_first_time = False
    
    if word_len in list( dict_len_word):
        word = dict_len_word[word_len][randint(0, len(dict_len_word[word_len])-1)]

        # indique s'il y a une erreur erreur = False
        return [word, False]
    else:
        return ['On ne sait pas de mot de cette longeur. Veuillez choisir une autre lonheur', True]
    

def get_words_sorted_by_cat(categorie):
    #^ make async with 'we are proceeding your request'
    #+ assert category -> str
    global word_cat_first_time
    global dict_cat_word
    translator = Translator()

    if word_cat_first_time:
        # faire async telechargement
        #ou faire l'onglet 'ca telecharge'
        dict_cat_word = gensim.downloader.load('glove-wiki-gigaword-50')
        word_cat_first_time = False

    categorie = translator.translate(categorie, src = 'fr', dest='en').text
    word = dict_cat_word.most_similar(categorie , topn = 3)[randint(0,2)]
    word = translator.translate(word, src = 'en', dest='fr').text
    return [word, False]