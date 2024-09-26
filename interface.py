from random import randint
import tkinter as tk
import gensim.downloader
from PIL import Image, ImageTk
from tkVideoPlayer import TkinterVideo
import json
import threading
import spacy
from bs4 import BeautifulSoup
import requests
import pickle
import os
from random import randint
from googletrans import Translator


'''
enigmes
'''
def enigme_lettre():
    '''enigme
    renvoye la premiere lettre non decouverte'''

    global MOT
    global image_to_lettre

    for i in range(len(MOT)):
        if MOT[i] in image_to_lettre: 
            return ['Astuce:', f'La {i+1}ème lettre est {MOT[i].upper()}', 'lettre']
    return ['Astuce:','Tu sait deja toutes les lettres du mot', 'lettre']


def homonyme(bs):
        '''Cherche la definition de l'homonyme du mot '''

        res = bs.find('a', 'lienarticle').text #touve le 'a' dans le texte de la page web
        definition = make_request(res, 'definition') #cherche la definition de l'homonime
        if definition[1] == 'error':
            res = [definition[0], '', 'honomyme']
        else:
            res = ["La definition de l'homonyme de ce mot est la suivante:",
                    definition[2].split('Synonymes')[0], 'homonyme']
        return res


def locution(bs, mot):
        '''Cherche la locution avec le mot donne'''
        global nlp

        res1 = bs.find('li', 'Locution').text

        #try:
        res_lemma = nlp(res1)
        mot = nlp(mot)
        mot = mot[0].lemma_ #lemmanize le mot
        res = ''
        for i in range(len(res_lemma)):
            if res_lemma[i].lemma_ == mot: #compare le mot du text lemmatize 
                    #au mot recherche pour le pas decouvrire le mot au joueur
                    res += '...'
                    res += ' '
            else:
                    res += res_lemma[i].text
                    res +=' '
        
        res = ['Voici une locution avec ce mot:', res, 'locution']
        return res


def citation(bs, mot):
        '''Cherche la citation avec le mot donne'''

        res = [bs.find('span', 'AuteurCitation').text] #cherche les tag donnes dans le texte de la page web
        res.append(bs.find('span', 'TexteCitation').text)
        res.append(bs.find('span', 'InfoCitation').text)

        res_lemma = nlp(res[1])
        mot = nlp(mot)
        mot = mot[0].lemma_
        res1 = ''
        for i in range(len(res_lemma)): #cache le mot recherche au joueur
            #pour sela lemmatize le mot de la citation et le compare au mot recherche
            if res_lemma[i].lemma_ == mot:
                    res1 += '...'
                    res1 += ' '
            else:
                    res1 += res_lemma[i].text
                    res1 += ' '
                    
        res = ['Voici une citation avec ce mot:', res[0],
                res1[:-1]+'.', res[2], 'citation']
                    
        return res


def enigme(sous_action, bs, mot=None):
        '''appelle la fonction de la bonne sous action'''
        try:
                if sous_action == 'homonymes':
                        return homonyme(bs)

                elif sous_action == 'locutions':
                        return locution(bs, mot)
                        
                elif sous_action == 'citations':    
                        return citation(bs, mot)
                else:
                        return enigme_lettre()

        
        except AttributeError:
                return None


def make_request(mot, action, sous_action = None):
    '''make a request to the Larous dictionnary to get the definition
    of a word or a complement information
    parsing de larousse.fr -> connection internette indispensable'''
    
    url = 'https://www.larousse.fr/dictionnaires/francais/' + mot
    #attention timeout 
    response = requests.get(url, timeout = 15) 

    try:
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'html.parser') #affecte le code html de la page web a la variable en tant que str
            
            if action == 'definition':
                try:
                    try:
                        mot_f_m = bs.find('p', 'CatgramDefinition')
                        definitions = bs.find('li', 'DivisionDefinition')
                        return [mot, mot_f_m.text, definitions.text.split('.\xa0')[1].split('\r')[0]]
                    except AttributeError:
                        return [mot, '', definitions.text]
                #except IndexError:
                except: #si la definition est indispenible, le dit au joueur
                    return ["Oh! Ce mot est trop complique! On ne peut pas trouver sa definition.", 'error']
                
            elif action == 'enigme':
                actions = ['homonymes', 'locutions', 'citation', 'lettre']
                if sous_action == None: #si la sous-action n'est pas choisit, la choisit au hasard
                    while len(actions) >= 1: #si la sous action est indispenible pour le mot, en choisit une autre
                        sous_action = actions.pop(randint(0, len(actions)-1))
                        res = enigme(sous_action, bs, mot)
                        if res != None:
                            return res

                    if  res == None:
                        return ["Oh! Ce mot est trop complique! " +\
                              "On ne peut pas trouver d'enigme.", 'error']
                
                else:
                    res = enigme(sous_action, bs, mot)
                    if res == None:
                        return ["Cet action est indisponible pour ce mot. " +\
                              "Veillez de choisir une autre action.", 'error']
                    else:
                        return res
                    

        else:
            return ['Errer! Status code:'+ response.status_code, 'error']

    except TimeoutError:
        return ['Verifiez la connection internet.\n Status code:'+ response.status_code, 'error']


def fermer_fenetre_def_eni_root(def_eni_root):
    '''detruit la fenetre tkinter'''

    def_eni_root.destroy()


def create_fenetre_def_eni_root(mot, action, sous_action = None):
    '''cree une fenetre qui affiche la definition ou l'enigme'''

    global nlp

    try:
         mot = mot.split()
         mot = mot[1]
    except: pass

    try:
        mot = nlp(mot[0])
        mot = mot[0].lemma_
    except: pass

    res = make_request(mot, action, sous_action)

    def_eni_root = tk.Tk()
    def_eni_root.config(bg = "#C0BCB5")

    if res[-1] == 'error':
        def_eni_root.title('error')
        t_text1 = tk.Label(def_eni_root, text = res[0], font = ('Chalkduster',"10"), 
                           bg = "#C0BCB5", fg = "#404040", padx = 20)

    elif action == 'enigme':

        def_eni_root.title('enigme')
        t_title = tk.Label(def_eni_root, text = 'Enigme', font = ('Chalkduster',"15"), 
                           bg = "#C0BCB5", fg = "#404040", padx = 20)

        t_text1 = tk.Label(def_eni_root, text = res[0], font = ('Chalkduster',"10"), 
                           bg = "#C0BCB5", padx = 10)
        t_text2 = tk.Label(def_eni_root, text = res[1], font = ('Chalkduster',"10"), 
                           bg = "#C0BCB5", padx = 10)
        
        if res[-1] == 'citation':
            t_text3 = tk.Label(def_eni_root, text = res[2], font = ('Chalkduster',"10"), 
                               bg = "#C0BCB5", padx = 10)
            t_text4 = tk.Label(def_eni_root, text = res[3], font = ('Chalkduster',"10"), 
                               bg = "#C0BCB5", padx = 10)

            t_text3.grid(row = 3, column = 1)
            t_text4.grid(row = 4, column = 1)
        
        t_title.grid(row = 0, column = 0, columnspan = 2, padx = 10)
        t_text2.grid(row = 2, column = 1)


    else:
        def_eni_root.title('definition')
        t_title = tk.Label(def_eni_root, text = res[0].capitalize(), font = ('Chalkduster',"15"), 
                           bg = "#C0BCB5", fg = "#404040", padx = 20)
        t_text1 = tk.Label(def_eni_root, text = res[1], font = ('Chalkduster',"10"), 
                           bg = "#C0BCB5", padx = 10)
        t_text2 = tk.Label(def_eni_root, text = res[2], font = ('Chalkduster',"10"), 
                           bg = "#C0BCB5", padx = 10)

        t_title.grid(row = 0, column = 0, columnspan = 2, padx = 10)
        t_text2.grid(row = 2, column = 1)
        
    t_text1.grid(row = 1, column = 1)

    b_quitter = tk.Button(def_eni_root, text = 'Quitter', 
                          command = lambda: fermer_fenetre_def_eni_root(def_eni_root))
    b_quitter.grid(column = 1, row = 7, padx = 5)


    def_eni_root.mainloop()


sous_action = None


def choisir_sous_action(s_action):
    global sous_action
    sous_action = s_action


def create_bouton_ask_eni(mot, ask_eni_root, image_to_lettre1, nlp1):
    '''Affiche le bouton qui affiche des enigmes et un bouton
    qui permet de choisir le type d'enigme '''

    global sous_action
    global MOT
    global image_to_lettre
    global nlp

    MOT = mot
    image_to_lettre = image_to_lettre1
    nlp = nlp1

    ask_eni_bouton = tk.Button(ask_eni_root, text = 'Enigme', 
                               command = lambda: create_fenetre_def_eni_root(mot, 'enigme', sous_action))
    ask_eni_bouton1 =  tk.Menubutton(ask_eni_root, text = "Choisir le type d'enigme", 
                                     relief = 'ridge',fg ='white', bg ='green' )
    ask_eni_bouton1.menu = tk.Menu(ask_eni_bouton1, tearoff = 0 )
    ask_eni_bouton1["menu"] =  ask_eni_bouton1.menu

    ask_eni_bouton1.menu.add_command(label = 'Homonyme', 
                                     command = lambda : choisir_sous_action('homonymes'))
    ask_eni_bouton1.menu.add_command(label = 'Citation',  
                                     command = lambda : choisir_sous_action('citations'))
    ask_eni_bouton1.menu.add_command(label = 'Locution', 
                                     command = lambda : choisir_sous_action('locutions'))
    ask_eni_bouton1.menu.add_command(label = 'Lettre', 
                                     command = lambda : choisir_sous_action('lettre'))
    ask_eni_bouton1.menu.add_command(label = 'Tout', 
                                     command = lambda : choisir_sous_action(None))

    ask_eni_bouton.place(x = 450 + (40 * int(len(mot) / 2)) + 50, y = 445)
    ask_eni_bouton1.place(x = 450 + (40 * int(len(mot) / 2)) + 50, y = 465)

"""
choisir le mot
"""

word_len_first_time = True
word_cat_first_time = True
dict_len_word = None
dict_cat_word = None


def load_words_sorted_by_len():
    '''loads a dictionnary containing french words sorted by len'''

    p = os.path.abspath('./utils/dict/french_dict1.pkl')
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
    
    if word_len in list( dict_len_word) and word_len<15:
        word = dict_len_word[word_len][randint(0, len(dict_len_word[word_len]) - 1)]
        # indique s'il y a une erreur
        # erreur = False
        return [word, False]
    else:
        return ['On ne sait pas de mot de cette longeur. \
                Veuillez choisir une autre longueur', True]
    
    
def get_words_sorted_by_cat(categorie, dict_cat_word, nlp):
    """trouve un mot de categorie donnee"""

    global word_cat_first_time

    try:
        int(categorie)
        return ["La categorie doit etre un mot", True]
    except: pass

    translator = Translator()
    categorie1 = translator.translate(categorie, src = 'fr', dest = 'en').text
    try:
        for i in range(10):
            try:
                word = dict_cat_word.most_similar(categorie1, topn = 5)[randint(0,4)][0]
                word = translator.translate(word, src = 'en', dest = 'fr').text
                if (nlp(word)[0].lemma_) != (nlp(categorie)[0].lemma_):
                    break
            except: continue
        return [word, False]
    
    except:
        return ["Cette categorie n'existe pas, veillez choisir un autre mot", True]
    

'''
interface
'''

nom = "Current"
current_nb_gagne = 0
dico_joueurs_gagne = None


def generer_mot():
    '''cree une fenetre avec des boutons qui permettent de choisir le mot'''

    global mot_par_classe, mot_par_len
    global nb_err_dispo

    creer_mot.destroy()
    mot_par_len = tk.Button(debutjeu,text="Choisir le mot par longueur", 
                            command = choix_len, font = ('Chalkduster',"10"), relief = 'ridge')                        
    mot_par_len.place(x = 220, y = 270)
    mot_par_classe = tk.Button(debutjeu, text = "Choisir par catégorie", 
                               command = choix_classe, font = ('Chalkduster',"10"), relief = 'ridge')                             
    mot_par_classe.place(x = 530, y = 270)
    l_err_choix = tk.Label(debutjeu, text = 'Choisissez le nombre de tentatives possible :', 
                           font = ('Chalkduster',"10"), bg = "#C0BCB5", fg = "#404040")
    l_err_choix.place(x = 180, y = 170)
    nb_err_dispo = tk.Scale (debutjeu, from_ = 1, to = 8 , orient = 'horizontal',
                             bg = "#C0BCB5", length = 200,  troughcolor = "#404040", highlightthickness = 0)                            
    nb_err_dispo.set(8)
    nb_err_dispo.place(x = 480, y = 150)


def debut(event):
    '''cree la fenetre du debut du jeu'''
    global creer_mot
    global play
    global phrase
    global titre

    play.destroy()
    phrase.destroy()
    titre.config(font = ('Chalkduster',"30"))
    creer_mot = tk.Button(debutjeu,text = "Générer un mot", 
                          font = ('Chalkduster',"15"), fg = "#5A5A5A", command=generer_mot, relief = 'ridge')     
    creer_mot.place(x = 380, y = 290)


def choix_len():
    '''cree un widget qui permet de choisir la longeur du mot'''
    global entry_len
    global donner_len
    global entry_classe
    global donner_categorie

    try : 
        entry_classe.destroy()
        donner_categorie.destroy()
    except: pass

    entry_len = tk.Entry(debutjeu)   
    donner_len = tk.Label(debutjeu, text = 'Longueur ?',font = ('Chalkduster',"10"))  
    entry_len.place(x = 390, y = 440)
    donner_len.place(x = 420, y = 420)
    entry_len.bind("<Return>", config_len) 


def config_len(event):
    '''permet de touver le mot par longueur'''
    global MOT
    global debutjeu
    global nb_err_dispo

    MOT = get_words_sorted_by_len(entry_len.get())
    if MOT[-1]:
        t_alert = tk.Label(debutjeu, text = MOT[0])
        t_alert.pack(side = 'top')
    else:
        try:
            nb_err_dispo = nb_err_dispo.get()
        except AttributeError: pass
        MOT = MOT[0].lower()
        debutjeu.destroy()
        root_jeu()


def choix_classe():
    '''cree un widget aui permet de choisir la categorie du mot'''
    global entry_classe
    global donner_categorie
    global entry_classe
    global donner_len
    try : 
        entry_len.destroy()
        donner_len.destroy()
    except: pass
    entry_classe = tk.Entry(debutjeu)
    donner_categorie = tk.Label(debutjeu,text = "Catégorie ?",
                                font = ('Chalkduster',"10"))
    entry_classe.place(x = 390, y = 440)
    donner_categorie.place(x = 420, y = 420)
    entry_classe.bind("<Return>",config_classe)
 
    
def config_classe(event):
    '''permet de trouver le mot par la categorie'''
    global class_user
    global debutjeu 
    global MOT
    global dict_cat_word
    global nlp
    global nb_err_dispo
    
    class_user = str(entry_classe.get())
    MOT = get_words_sorted_by_cat(class_user, dict_cat_word, nlp)
    if MOT[-1]:
        t_alert = tk.Label(debutjeu, text = MOT[0])
        t_alert.pack(side = 'top')
    else:
        try:
            nb_err_dispo = nb_err_dispo.get()
        except AttributeError: pass
        MOT = MOT[0].lower()
        debutjeu.destroy()
        root_jeu()


def gagne_perdu(gagne_perdu, mot = ''):
    '''cree la fenetre quand le joueur a gagne ou perdu'''
    global racine
    global nom
    global current_nb_gagne
    global nb_pas
    global dico_joueurs_gagne
    

    racine = tk.Tk()
    racine.geometry("600x350")
    racine.resizable(width = False, height = False) 
    
    if gagne_perdu:

        if nom == "Current":
            current_nb_gagne += 1
            dico_joueurs_gagne["Current"][0] = current_nb_gagne
        elif nom not in list(dico_joueurs_gagne):
            dico_joueurs_gagne[nom] = [0, []]
            dico_joueurs_gagne[nom][0] = 1
        else:
            dico_joueurs_gagne[nom][0] += 1

        racine.title("Gagne!")
        racine.configure(bg = "#C0BCB5")
        img= Image.open('./interface/CONFETTIS 2.png')
        img = img.resize((600, 350))
        img = ImageTk.PhotoImage(img, master = racine)
        label = tk.Label(racine, image = img)
        label.place(x=0, y=0)
        gagne=tk.Label(racine, text = "Félicitations vous avez gagné !",font = ("Chalkduster", 25))
        gagne.place(anchor = 'center', x = 300, y = 175)
        sessions = tk.Label(racine,text=f"Tu as gagné {dico_joueurs_gagne[nom][0]} sessions",
                             font=("Chalkduster", 10))
        sessions.place(x = 400, y = 0)

        sessions1 = tk.Label(racine,text=f"Durant ce jeu tu as utilise {nb_pas} tentatives", 
                             font=("Chalkduster", 10))
        sessions1.place(x = 350, y = 22)

    
    else:
        
        if nom == "Current":
            dico_joueurs_gagne["Current"][0] = current_nb_gagne
        elif nom not in list(dico_joueurs_gagne):
            dico_joueurs_gagne[nom] = [0, []]
            dico_joueurs_gagne[nom][0] = 0

        racine.title("Perdu")
        racine.configure(bg = "#BB2222")
        img= Image.open('./interface/corde1.png')
        img = img.resize((130, 240))
        img = ImageTk.PhotoImage(img, master = racine)
        label = tk.Label(racine, image = img,bg = "#BB2222")
        label.place(anchor = 'nw', x=10, y=0)
        gagne=tk.Label(racine, text = "Vous avez perdu...",font=("Chalkduster", 27),bg = "#BB2222")
        perdu = tk.Label(racine, text = f'Le mot cache etait "{mot}"',font=("Chalkduster", 18),bg = "#BB2222")
        gagne.place(anchor ='center', x = 300, y = 100)
        perdu.place(anchor = 'center', x = 300, y = 160)

        #nb victoires changer par la fonction
        sessions = tk.Label(racine,text=f"Tu as gagné {dico_joueurs_gagne[nom][0]} sessions",
                             font=("Chalkduster", 10), bg = "#BB2222")
        sessions.place(x = 400, y = 0)

        sessions1 = tk.Label(racine,text=f"Durant ce jeu tu as utilise {nb_pas} tentatives", 
                             font=("Chalkduster", 10),bg = "#BB2222")
        sessions1.place(x = 350, y = 22)

    #boutons
    restart1 = tk.Button(racine, text="Recommencer une partie ", relief = 'ridge', bg = '#5C5C5C',
                         command = recommencer,font = ("Chalkduster", 10), highlightthickness = 0)
    restart1.place(anchor = 'center', x = 300, y = 240)
    b_quitter = tk.Button(racine, text = 'Quitter', command = lambda: destroy_root(racine), 
                          relief = 'ridge', bg = '#5C5C5C')
    b_quitter.place(anchor='center', x = 300, y = 280)
    

    dico_joueurs_gagne[nom][1].append([mot,nb_pas])
    json.dump(dico_joueurs_gagne, open("./utils/dico_joueurs_gagne.json","w"))

    racine.mainloop()


def destroy_root(root):
    '''detriot la fenetre'''
    root.destroy()


def root_debut_jeu():
    '''fenetre debut de jeu '''
    global play
    global phrase
    global titre
    global debutjeu 

    debutjeu = tk.Tk()
    debutjeu.title("Jeu du pendu")
    debutjeu.config(bg = "#C0BCB5")
    debutjeu.geometry("900x600")
    debutjeu.resizable(width = False, height = False) 

    #création widgets accueil
    play = tk.Canvas(debutjeu, height = 250, width = 400, bg = "#C0BCB5", 
                     bd = '0', highlightthickness = 0)
    photo = ImageTk.PhotoImage(Image.open("./utils/play1.png")) 
    play.create_image(0,0,anchor = 'nw', image = photo)
    titre = tk.Label(debutjeu, font = ('Chalkduster',"30"), text = "Le jeu du pendu", 
                     bg = "#5A5A5A", fg = "#C0BCB5")
    phrase=tk.Label(debutjeu, font = ('Chalkduster',"15"), 
                    text = "Allez-vous réussir à échapper à la pendaison ?", 
                    fg = "#404040", bg = '#C0BCB5')
    b_quitter = tk.Button(debutjeu, text = 'Quitter', command = lambda: \
        destroy_root(debutjeu), relief = 'ridge', bg = '#5C5C5C')
                          
    #placement accueil
    titre.pack(side = 'top', pady = 20)
    play.place(x = 250, y = 150)
    phrase.place(x = 250, y = 430)
    b_quitter.pack(side = 'bottom', pady = 15)

    play.bind("<Button-1>", debut)

    b_score = tk.Button(debutjeu, text = 'Score', command = root_score, 
                          relief = 'ridge', bg = '#5C5C5C')
    b_score.pack(side = 'bottom')

    debutjeu.mainloop()


def new_nom(event):
    '''permet de changer le joueur'''
    global joueur   
    global zone_nom
    global nom
    global jeu

    try:
        nom = 'Current'
        joueur.configure(text = "Joueur : ")
        zone_nom = tk.Entry(jeu)
        zone_nom.place(x = 60, y = 3, anchor = 'nw')
        zone_nom.bind("<Return>", confirm_nom)
    except: pass


def new_nom1(event):
    '''permet de changer le joueur pour savoir le score'''
    global joueur1
    global zone_nom1
    global nom
    global root

    try:
        nom = 'Current'
        joueur1.configure(text = "Joueur : ")
        zone_nom1 = tk.Entry(root)
        zone_nom1.place(x = 60, y = 3, anchor = 'nw')
        zone_nom1.bind("<Return>", confirm_nom1)
    except: pass


def confirm_nom(event):  
    '''permet de s'autentifier'''
    global joueur   
    global zone_nom
    global nom

    try:
        if zone_nom.get() != '':
            nom = zone_nom.get()
        joueur.configure(text = "Joueur : " + nom)
        zone_nom.destroy() 
    except: pass


def confirm_nom1(event):  
    '''permet de s'autentifier pour savoir le score'''
    global joueur1  
    global zone_nom1
    global nom
    global root
    global l_error

    try:
        if zone_nom1.get() != '':
            nom = zone_nom1.get()
        joueur1.configure(text = "Joueur : "+ nom)
        get_score()
    except: pass


def duration(event):

    '''stoppe la video avec le pendu 
    a une duree determinee a partir du nombre de tentatives possibles'''

    global nb_err_dispo
    global i_err
    global i_err2
    
    
    decoupage = {1: [9], 2: [7, 2], 3:[4,4,1], 4:[3,2,2,2], 5:[3, 2, 1, 1, 2], 
                 6:[3, 1, 1, 1, 1, 2], 7:[2, 1, 1, 1, 1, 1, 2], 
                 8:[2, 1, 1, 1, 1, 1, 1, 1]}
    
    if i_err2%decoupage[nb_err_dispo][i_err] == 0:
        videoplayer.pause()
        i_err += 1
    else:
        videoplayer.bind("<<SecondChanged>>", duration)
        i_err2 += 1


def creer_croix(event):
    '''barre la lettre choisi'''
    global jeu
    global canvas
    global c_mot
    global lettre_inconnue
    global MOT
    global nb_errors
    global videoplayer
    global mot_non_decouvert
    global image_to_lettre
    global nb_pas
    global l_tentatives
    global dico_joueurs_gagne
    global nb_err_dispo
    global i_err2


    nb_pas += 1
    

    image_to_lettre1 = ['0','é', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j','i', 
                        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z', 
                        'à', 'è', 'ê', 'ë', 'î', 'ï', 'ö', 'ù', '-', ' ', "'"]
                      

    lettres_images = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7,'h':8, \
        'i':10, 'j':9, 'k':11, 'l':12, 'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18,\
            's':19, 't':20, 'u':21, 'v':22, 'w':23,'x':24, 'y':25, 'z':26, 'é':0, 'à':27, \
                "è":28, "ê":29, "ë": 30, "î":31, "ï": 32, "ö": 33, "ù":34, '-':35, ' ':36, "'":37}
                    
    
    if event.widget == jeu: 
        try:
            lettre1 = event.keysym
            num = image_to_lettre1.index(str(lettre1)) - 1
            #rechercher la lettre dans les images sur le clavier de l'écran 
            lettre = image_to_lettre[lettres_images[lettre1] + 1]
            image_to_lettre[lettres_images[lettre1] + 1] = '0'
            # créer la croix qui barre les lettres
            canvas[num].create_line((0,51), (43, 0))
            canvas[num].create_line((0,0), (43, 51))
        except ValueError: pass

    
    elif jeu.winfo_pointery() > 200: 
        try:
            event.widget.create_line((0,51), (43, 0))
            event.widget.create_line((0,0), (43, 51))
        except AttributeError: pass
        try:
            lettre = image_to_lettre[int(str(event.widget)[8:])]
            image_to_lettre[int(str(event.widget)[8:])] = '0'
        except:
            lettre = image_to_lettre[1]
            image_to_lettre[1] = '0'
    try:
        if lettre not in MOT and lettre != '0':
            nb_errors += 1
            l_tentatives.config(text = f'Il te reste {nb_err_dispo-nb_errors} tentatives.')
            
            videoplayer.load(f"./pendu_all1.mp4") #play the video if lettre not in word
            videoplayer.play()
            i_err2 = 1
            videoplayer.bind("<<SecondChanged>>", duration)
            if nb_errors == nb_err_dispo:
                for i in canvas:
                    i.destroy()
                jeu.geometry("900x600") 
                b_def = tk.Button(jeu, text = f'Definition du mot {MOT}',
                                  command = lambda: create_fenetre_def_eni_root(MOT, 'definition'))
                b_def.place(x = 400, y = 530)
                gagne_perdu(0, MOT)

        elif lettre != '0':
            for i in range(len(MOT)):
                if MOT[i] == lettre:
                    lettre_inconnue[i] = ImageTk.PhotoImage(Image.open(f'./utils/lettres/{str(lettres_images[lettre])}.png'))
                    c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])
                    mot_non_decouvert -= 1

            if mot_non_decouvert == 0:
                for i in canvas:
                    i.destroy()
                jeu.geometry("900x600") 
                b_def = tk.Button(jeu, text = f'Definition du mot {MOT}', 
                                command = lambda: create_fenetre_def_eni_root(MOT, 'definition'))
                b_def.place(x = 400, y = 530)
                gagne_perdu(1, MOT)
    except UnboundLocalError: pass


def recommencer():
    '''permet de recommencer le jeu meme si le jeu n'est pas encore
    termine'''
    global jeu
    
    try:
        global racine
        racine.destroy()
        jeu.destroy()
    except:
        jeu.destroy()

    root_debut_jeu()


def root_jeu():
    '''fenetre de jeu'''
    global joueur
    global jeu
    global zone_nom
    global canvas
    global c_mot
    global lettre_inconnue
    global nb_errors
    global videoplayer
    global MOT
    global mot_non_decouvert
    global image_to_lettre
    global l_tentatives
    global dico_joueurs_gagne
    global nb_pas
    global i_err

    i_err = 0
    nb_pas = 0
    nb_errors = 0
    mot_non_decouvert = len(MOT)
    with open('./utils/dico_joueurs_gagne.json', 'r') as f:
        dico_joueurs_gagne = json.load(f)

    image_to_lettre = ['0','é', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j','i', 
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z', 
                       'à', 'è', 'ê', 'ë', 'î', 'ï', 'ö', 'ù', '-', ' ', "'"]
                        

    jeu = tk.Tk()
    jeu.title("Jeu du pendu")
    jeu.config(bg = "#C0BCB5")
    jeu.geometry("900x720")
    jeu.resizable(width = False, height = False) 


    titre1 = tk.Label(jeu, font = ('Chalkduster',"30"), text = "Le jeu du pendu", 
                      bg = "#404040", fg = "#C0BCB5")
    titre1.pack(side = "top")
    
    #création du clavier 
    canvas = []
    lettre = []
    for i in range(0,38): 
        canvas.append(tk.Canvas(jeu, bg = "#C0BCB5",bd ='0',
                                height = 48, width = 40))
        lettre.append(ImageTk.PhotoImage(Image.open('./utils/lettres/%s.png'%i)))
        canvas[i].create_image(3,3,anchor = 'nw',image = lettre[i])
        canvas[i].bind('<Button-1>', creer_croix)

    jeu.bind("<Key>", creer_croix)
    #placement clavier
    for k in range (0,15):
        canvas[k].place(x = 90 + 50 * k, y = 530)
    for k in range (15, 29):
        canvas[k].place(x = 105 + 50 * (k - 15), y = 590)
    for k in range (29,len(canvas)):
        canvas[k].place(x = 250 + 50 * (k - 29), y = 650)
    
    #placer video
    c_vid_canvas = tk.Canvas(jeu, width = 450, height = 350, bg = "#404040")
    c_vid_canvas.place(x = 225, y = 75)
    videoplayer = TkinterVideo(master = jeu, scaled = True)
    videoplayer.place(x = 250, y = 100, height = 300, width = 400)

    #placer le mot
    c_mot = []
    lettre_inconnue = []
    for i in range(len(MOT)):
        c_mot.append(tk.Canvas( bg = "#C0BCB5",bd = '0',height = 48, width = 40))
        lettre_inconnue.append(ImageTk.PhotoImage(Image.open('./utils/lettres/tiret.png')))
        c_mot[i].place(x = 450 - (40 * int(len(MOT) / 2)) + (40 * i), y = 445)
        c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])
    
    #enigme
    create_bouton_ask_eni(MOT, jeu, image_to_lettre, nlp)

    #affiche le mot dans le terminal
    print(MOT)


    #entrer informations du jeu
    zone_nom = tk.Entry(jeu)
    zone_nom.bind("<Return>", confirm_nom) 


    joueur = tk.Label(jeu, text = "Joueur :") 
    joueur.bind("<Button-1>", new_nom) 

    zone_nom.place(x=60, y=3, anchor='nw')
    joueur.place(x = 0, y =3, anchor='nw')

    if nom != 'Current':
        confirm_nom(0)

    b_recommencer = tk.Button(jeu, text = 'Recommencer', command = recommencer, 
                          relief = 'ridge', bg = '#5C5C5C')
    b_recommencer.place(x = 800, y = 20)

    b_quitter = tk.Button(jeu, text = 'Quitter', 
                          command = lambda: destroy_root(jeu), relief = 'ridge', bg = '#5C5C5C')
                          
    b_quitter.place(x = 820, y =50)

    b_score = tk.Button(jeu, text = 'Score', command = root_score, 
                          relief = 'ridge', bg = '#5C5C5C')
    b_score.place(x=825, y=80)
    

    l_tentatives = tk.Label(jeu, text = f'Il te reste {nb_err_dispo} tentatives',
                            font=('Chalkduster',"10"), bg="#C0BCB5", fg="#404040")
    l_tentatives.place(x = 720, y =260)

    jeu.mainloop()


def get_score():

    '''calcule l'efficacite du joueur pour la mettre dans le fenetre afficheant 
    le score du joueur'''

    global root
    global nom
    global dico_joueurs_gagne
    global l_error
    global zone_nom1
    global joueur1

    for widget in root.winfo_children():
        if widget != joueur1:
            widget.destroy()
    
    b_quitter = tk.Button(root, text = 'Quitter', command = lambda: destroy_root(root), 
                          relief = 'ridge', bg = '#5C5C5C')
    b_quitter.pack(side='bottom')

    if nom in list(dico_joueurs_gagne):
        titre = tk.Label(root, font = ('Chalkduster',"30"), text = f"Score de {nom}", 
                         bg = "#C0BCB5", fg = "#404040", pady = 20)
        titre.pack(side = 'top')
            
        l_nb_gains = tk.Label(root,text = f'Vous avez gagne {dico_joueurs_gagne[nom][0]} parties', 
                              font = ('Chalkduster',"20"),bg = "#C0BCB5", fg = "#404040",pady = 10)
                                
            
        nb_pas_moyen = 0
        l_nb_pas = []
        i = 0
        while i < 5:
            try:
                l_nb_pas.append(tk.Label(root, text = f'mot "{dico_joueurs_gagne[nom][1][-(i+1)][0]}":' +
                    f'{dico_joueurs_gagne[nom][1][-(i+1)][1]} pas',font = ('Chalkduster',"10"),
                    bg = "#C0BCB5", fg = "#404040", padx = 40))
                                
                nb_pas_moyen += dico_joueurs_gagne[nom][1][-(i+1)][1]
                i += 1
            except: break
            
        l_nb_gains.pack(side = 'top')

        try:
            l_nb_moyen_gains = tk.Label(root,text = f'Votre nombre moyen de tentatives est ' +
                f'{int(nb_pas_moyen/i)} ', font = ('Chalkduster',"15"),bg = "#C0BCB5", 
                fg = "#404040", pady = 15)
                                            
            l_nb_moyen_gains.pack(side = 'top')
        except ZeroDivisionError: pass

        l_text = tk.Label(root,text = f'Vos tentatives:', 
                            font = ('Chalkduster',"15"),bg = "#C0BCB5", fg = "#404040", pady = 15)
        l_text.pack(side = 'top')

        for i in range(len(l_nb_pas)):
            l_nb_pas[i].pack(side = 'top')
    else:
            l_error = tk.Label(root, text = 'Vous devez finir au moins '+
                'une partie pour voir le score')
            l_error.place(x = 150, y = 200)
           
           
def root_score():

    '''cree le fenetre qui permet de voir le score du joueur'''

    global nom
    global dico_joueurs_gagne
    global root
    global joueur1
    global zone_nom1
    global l_error
    global dico_joueurs_gagne

    root = tk.Tk()
    root.title('Pendu - Score')
    root.config(bg = "#C0BCB5")
    root.geometry("600x400") 
    root.resizable(width = False, height = False) 

    if dico_joueurs_gagne == None:
        with open('./utils/dico_joueurs_gagne.json', 'r') as f:
            dico_joueurs_gagne = json.load(f)

    zone_nom1 = tk.Entry(root)
    zone_nom1.bind("<Return>", confirm_nom1) 

    joueur1 = tk.Label(root, text = "Joueur :") 
    joueur1.bind("<Button-1>", new_nom1) 

    zone_nom1.place(x = 60, y = 3, anchor = 'nw')
    joueur1.place(x = 0, y = 3, anchor = 'nw')

    if nom == 'Current':
        l_error = tk.Label(root, text = 'Authentifiez vous avant de voire le score')
        l_error.place(x = 200, y = 200)
    else:
        confirm_nom1(0)
        get_score()
        
    b_quitter = tk.Button(root, text = 'Quitter', command = lambda: destroy_root(root), 
                          relief = 'ridge', bg = '#5C5C5C')
    b_quitter.pack(side='bottom')
    
    root.mainloop()


def load_lib_nlp():
    '''download dictionnaire francais de spacy'''
    global nlp
    nlp = spacy.load('fr_core_news_md') 
    return 0


def load_lib_glove():
    '''download wiki-gigaword-50 pour trouver les mots par categorie'''
    global dict_cat_word
    dict_cat_word = gensim.downloader.load('glove-wiki-gigaword-50')
    return 0
   
    
def wait_load_lib():
    '''fenetre avec slidebar permettant aux dictionnaires de se telecharger
    avant que le jeu commence'''
    root = tk.Tk()
    root.title('Pendu')
    root.config(bg = "#C0BCB5")
    root.geometry("600x400") 
    root.resizable(width = False, height = False) 

    titre = tk.Label(root, font = ('Chalkduster',"30"), text = "Le jeu du pendu", 
                     bg = "#C0BCB5", fg = "#404040")
    titre.place(x = 150, y = 120)
    
    
    l_attendre = tk.Label(root,text = 'Le jeu commencera bientot', font = ('Chalkduster',"10"),
                          bg = "#C0BCB5", fg = "#404040")
    s_attendre = tk.Scale(root, from_ = 0, to = 10 , orient = 'horizontal',bg = "#C0BCB5", 
                          showvalue = 0, length = 200,  troughcolor = "#404040")
    
    l_attendre.place(x = 210, y = 200)
    s_attendre.place(x = 190, y = 250)
    
    t1_1 = threading.Thread(target = load_lib_nlp)
    t1_2 = threading.Thread(target = load_lib_glove)

    t1_1.start()
    t1_2.start()
    for i in range(11):
        s_attendre.set(i)
        root.update()
        root.after(1000)
    destroy_root(root)
    
    root.mainloop()


wait_load_lib()
root_debut_jeu()