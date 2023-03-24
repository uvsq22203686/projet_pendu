from bs4 import BeautifulSoup
import requests
from random import randint
import tkinter as tk
import pickle
import os
from random import randint
import gensim.downloader
from googletrans import Translator
#pip install googletrans==3.1.0a0

#fenetre debut de jeu 
debutjeu = tk.Tk()
debutjeu.title("Jeu du pendu")
debutjeu.config(bg ="#C0BCB5")
debutjeu.geometry("500x500")

def debut():
    debutjeu.destroy()
    
play = tk.Button(debutjeu, text = "Play", bg = "#383e42", command=debut)
play.grid(column=5, r ow=5)

debutjeu.mainloop()

#fenetre de jeu 

jeu = tk.Tk()
jeu.title("Jeu du pendu")
jeu.config(bg ="#C0BCB5")

def actionEvent(event):     
    lbl.configure(text = "Joueur : "+ entry.get())
    entry.destroy()   
 
#entrer informations du jeu
entry = tk.Entry(jeu)
entry.bind("<Return>", actionEvent) 
lbl = tk.Label(jeu, text = "Joueur :") 
entry.grid(column=1, row=5) 
lbl.grid(column=0, row = 5) 

def homonyme(bs):
        '''Cherche la definition de l'homonyme du mot'''

        res = bs.find('a', 'lienarticle').text
        res = ["La definition de l'homonyme de ce mot est la suivante:",
            make_request(res, 'definition')[2], 'homonyme']
        return res

def locution(bs, mot):
        '''Cherche la locution avec le mot donne'''
        res_valide = False
        index_invalid = True
        max_index = 8

        res = bs.find('ul', 'ListeLocutions').text[:1000].split('.')
        while index_invalid:
            try:
                res1 = res[randint(1,max_index)]
                index_invalid = False
            except IndexError:
                  max_index-=1

        while res_valide == False:
                index_invalid = True
                if len(res1)<20:
                        while index_invalid:
                            try:
                                res1 = res[randint(1,max_index)]
                                index_invalid = False
                            except IndexError:
                                max_index-=1
                else:
                        res_valide = True
                res1 = res1.split(' ')
                res = ''
                for i in res1:
                        if i.lower().__contains__(mot):
                            i = '...'
                        res+=i
                        res+=' '
                res = ['Voici une locution avec ce mot:', res[:-1]+'.', 'locution']
        return res

def citation(bs, mot):
        '''cherche la citation avec le mot donne'''

        res = [bs.find('span', 'AuteurCitation').text]
        res.append(bs.find('span', 'TexteCitation').text)
        res.append(bs.find('span', 'InfoCitation').text)
                    
        res[1] = res[1].split(' ')
        res1 = ''
        for i in res[1]:
                if i.lower().__contains__(mot):
                        i = '...'
                res1+=i
                res1+=' '
        res = ['Voici une citation avec ce mot:', res[0],
                res1[:-1]+'.', res[2], 'citation']
                    
        return res

def enigme(sous_action, bs, mot=None):
        try:
                if sous_action == 'homonymes':
                        return homonyme(bs)

                elif sous_action == 'locutions':
                        return locution(bs, mot)
                        
                else:    
                        return citation(bs, mot)

        
        except AttributeError:
                return None

def make_request(mot, action, sous_action = None):
    '''make a request to the Larous dictionnary to get the definition
    of a word or a complement information'''

    url = 'https://www.larousse.fr/dictionnaires/francais/' + mot
    response = requests.get(url)

    try:
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'html.parser')
            
            if action == 'definition':
                try:
                    mot_f_m = bs.find('p', 'CatgramDefinition')
                    #definitions = bs.find('ul', 'Definitions')
                    definitions = bs.find('li', 'DivisionDefinition')
                    return [mot, mot_f_m.text, definitions.text.split('.\xa0')[1].split('\r')[0]]
                except IndexError:
                    return ["Oh! Ce mot est trop complique! On ne peut pas trouver sa definition.", 'error']

            elif action == 'enigme':
                actions = ['homonymes', 'locutions', 'citation']
                if sous_action == None:
                    ca_marche = False
                    while len(actions)>=1:
                        sous_action = actions.pop(randint(0, len(actions)-1))
                        res = enigme(sous_action, bs, mot)
                        if res!=None:
                            return res

                    if  res == None:
                        return ["Oh! Ce mot est trop complique! "+\
                              "On ne peut pas trouver d'enigme.", 'error']
                
                else:
                    res = enigme(sous_action, bs, mot)
                    if res==None:
                        return ["Cet action est indisponible pour ce mot. "+\
                              "Veillez de choisir une autre action.", 'error']
                    else:
                        return res
                    

        else:
            return ['Verifiez la connection internet.\n Status code:'+ response.status_code, 'error']

    except TimeoutError:
        return ['Verifiez la connection internet.\n Status code:'+ response.status_code, 'error']

def fermer_fenetre_def_eni_root(def_eni_root):
    def_eni_root.destroy()


def create_fenetre_def_eni_root(mot, action, sous_action):
    '''cree une fenetre qui affiche la definition
    ou l'enigme'''
    res = make_request(mot, action, sous_action)

    def_eni_root = tk.Tk()

    if res[-1]=='error':
        def_eni_root.title('error')
        t_text1 = tk.Label(def_eni_root, text = res[0])

    elif action == 'enigme':

        def_eni_root.title('enigme')
        t_title = tk.Label(def_eni_root, text = 'Enigme')

        t_text1 = tk.Label(def_eni_root, text = res[0])
        t_text2 = tk.Label(def_eni_root, text = res[1])
        
        if res[-1] == 'citation':
            t_text3 = tk.Label(def_eni_root, text = res[2])
            t_text4 = tk.Label(def_eni_root, text = res[3])

            t_text3.grid(row=3, column=1)
            t_text4.grid(row=4, column=1)
        
        t_title.grid(row=0, column=0, columnspan = 2)
        t_text2.grid(row=2, column=1)


    else:
        def_eni_root.title('definition')
        t_title = tk.Label(def_eni_root, text = res[0].capitalize())
        t_text1 = tk.Label(def_eni_root, text = res[1])
        t_text2 = tk.Label(def_eni_root, text = res[2])

        t_title.grid(row=0, column=0, columnspan = 2)
        t_text2.grid(row=2, column=1)
        
    t_text1.grid(row=1, column=1)

    b_quitter = tk.Button(def_eni_root, text = 'Quitter', command = lambda: fermer_fenetre_def_eni_root(def_eni_root))
    b_quitter.grid(column = 2, row = 5)


    def_eni_root.mainloop()


sous_action = None

def choisir_sous_action(s_action):
    global sous_action
    sous_action = s_action


'''Affiche le bouton qui affiche des enigmes et un bouton
qui permet de choisir le type d'enigme '''
#global sous_action

ask_eni_bouton = tk.Button(jeu, text='Enigme', command = lambda: create_fenetre_def_eni_root(word, 'enigme', sous_action))
ask_eni_bouton1 =  tk.Menubutton(jeu, text = "Choisir le type d'enigme", relief = 'ridge',fg='white', bg='green' )
ask_eni_bouton1.menu = tk.Menu(ask_eni_bouton1, tearoff = 0 )
ask_eni_bouton1["menu"] =  ask_eni_bouton1.menu

ask_eni_bouton1.menu.add_command(label = 'Homonyme', command = lambda : choisir_sous_action('homonymes'))
ask_eni_bouton1.menu.add_command(label = 'Citation',  command = lambda : choisir_sous_action('citations'))
ask_eni_bouton1.menu.add_command(label = 'Locution', command = lambda : choisir_sous_action('locutions'))
ask_eni_bouton1.menu.add_command(label = 'Tout', command = lambda : choisir_sous_action(None))

ask_eni_bouton.grid(column = 0, row = 0)
ask_eni_bouton1.grid(column = 1, row = 0)



word_len_first_time = True
word_cat_first_time = True
dict_len_word = None
dict_cat_word = None

def load_words_sorted_by_len():
    p = os.path.abspath('./dict/french_dict.pkl')
    with open(p, 'rb') as d:
        mots = pickle.load(d)
    return mots

def get_words_sorted_by_len(word_len):
    #+ assert word_len-> int
    global word_len_first_time, word
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
    global word_cat_first_time, word
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


def generer_mot():
    creer_mot.destroy()
    mot_par_len = tk.Button(jeu,text="Choisir le mot par longueur", command=choix_len)
    mot_par_len.grid(column=3, row=4)
    mot_par_classe = tk.Button(jeu, text="Choisir par catégorie", command=choix_classe)
    mot_par_classe.grid(column=4, row=4)
    
creer_mot = tk.Button(jeu,text="Générer un mot", command=generer_mot)
creer_mot.grid(column = 3, row=3, columnspan=2)


def choix_len():
    global entry_len
    entry_len = tk.Entry(jeu)
    entry_len.grid(column=3, row=5)
    entry_len.bind("<Return>", config_len)
    
def config_len(event):
    global len_user
    len_user = int(entry_len.get())
    get_words_sorted_by_len(len_user)

def choix_classe():
    global entry_classe
    entry_classe = tk.Entry(jeu)
    entry_classe.grid(column=4, row=5)
    entry_classe.bind("<Return>",config_classe)
    
def config_classe(event):
    global class_user
    class_user = str(entry_classe.get())
    get_words_sorted_by_cat(class_user)
    


#bouton genérer un mot 


#def actionEvent(event):     
 #   lbl.configure(text = "Joueur : "+ entry.get())
  #  entry.destroy()   
 
#entry = tk.Entry(jeu)
#entry.bind("<Return>", actionEvent) 
#lbl = tk.Label(jeu, text = "Joueur :") 
#ntry.grid(column=1, row=5) 
#lbl.grid(column=0, row = 5) 

jeu.mainloop()

    