from random import randint
import tkinter as tk
import gensim.downloader
from PIL import Image, ImageTk
import sys
from tkVideoPlayer import TkinterVideo
import json
import threading
import spacy

sys.path.append('./utils')
from choose_words import *
from enigmes import create_bouton_ask_eni, create_fenetre_def_eni_root


nom = "Current"
current_nb_gagne = 0


def generer_mot():
    '''cree une fenetre avec des boutons qui permettent de choisir le mot'''
    global mot_par_classe, mot_par_len
    creer_mot.destroy()
    mot_par_len = tk.Button(debutjeu,text="Choisir le mot par longueur",font=('Chalkduster',"15"), command=choix_len)
    mot_par_len.pack(pady=5)
    mot_par_classe = tk.Button(debutjeu, text="Choisir par catégorie",font=('Chalkduster',"15"), command=choix_classe)
    mot_par_classe.pack(pady =5)

def debut(event):
    '''cree la fenetre du debut du jeu'''
    global creer_mot
    global play
    global phrase
    global titre

    play.destroy()
    phrase.destroy()
    titre.config(font=('Chalkduster',"30"))
    creer_mot = tk.Button(debutjeu,text="Générer un mot", font=('Chalkduster',"15"), fg = "#5A5A5A",
                          command=generer_mot, relief = 'ridge')
    creer_mot.place(x = 380, y = 290)

def choix_len():
    global entry_len
    global donner_len
    try : 
            entry_classe.destroy()
            donner_categorie.destroy()
            #entry_len = tk.Entry(debutjeu) 
    except NameError :
        None
    entry_len = tk.Entry(debutjeu)   
    donner_len = tk.Label(debutjeu, text='Longueur ?',font=('Chalkduster',"15"))  
    entry_len.pack(side='bottom')
    donner_len.pack(side='bottom')
    entry_len.bind("<Return>", config_len) 
    
def config_len(event):
    '''permet de touver le mot par longueur'''
    global len_user
    global MOT
    global debutjeu

    MOT = get_words_sorted_by_len(entry_len.get())
    if MOT[-1]:
        t_alert = tk.Label(debutjeu, text=MOT[0])
        t_alert.pack(side = 'top')
    else:
        MOT = MOT[0].lower()
        debutjeu.destroy()
        root_jeu()

def choix_classe():
    global entry_classe
    global donner_categorie
    try : 
        entry_len.destroy()
        donner_len.destroy()
    except NameError : 
        None
    entry_classe = tk.Entry(debutjeu)
    donner_categorie = tk.Label(debutjeu,text="Catégorie ?",font=('Chalkduster',"15"))
    entry_classe.pack(side = 'bottom')
    donner_categorie.pack(side='bottom')
    entry_classe.bind("<Return>",config_classe)
    
def config_classe(event):
    '''permet de trouver le mot par la categorie'''
    global class_user
    global debutjeu 
    global MOT
    global dict_cat_word
    global nlp

    class_user = str(entry_classe.get())
    MOT = get_words_sorted_by_cat(class_user, dict_cat_word, nlp)
    if MOT[-1]:
        t_alert = tk.Label(debutjeu, text=MOT[0])
        t_alert.pack(side = 'top')
    else:
        MOT = MOT[0].lower()
        debutjeu.destroy()
        root_jeu()

def fontionrecommencer(dico_joueurs_gagne):
    '''recommence le jeu'''

    global jeu
    global racine

    json.dump(dico_joueurs_gagne, open("dico_joueurs_gagne.json","w"))
    #sauvegarde le nombre de parties gagnees

    jeu.destroy()
    racine.destroy()
    root_debut_jeu()

def gagne_perdu(gagne_perdu, mot = ''):
    '''cree la fenetre quand le joueur a gagne ou perdu'''
    global racine
    global nom
    global current_nb_gagne

    with open('dico_joueurs_gagne.json', 'r') as f:
        dico_joueurs_gagne = json.load(f)
    
    racine = tk.Tk()
    racine.geometry("600x350")
    racine.resizable(width=False, height=False) 
    
    if gagne_perdu:

        if nom == "Current":
            current_nb_gagne += 1
            dico_joueurs_gagne["Current"] = current_nb_gagne
        elif nom not in list(dico_joueurs_gagne):
            dico_joueurs_gagne[nom] = 1
        else:
            dico_joueurs_gagne[nom] += 1

        racine.title("Gagne!")
        #changer le path!
        img= Image.open('../interface/CONFETTIS 2.png')
        img = img.resize((600, 350))
        img = ImageTk.PhotoImage(img, master = racine)
        label = tk.Label(racine, image = img)
        label.place(x=0, y=0)
        gagne=tk.Label(racine, text = "Félicitations vous avez gagné !",font=("Arial", 25))
        gagne.place(x = 75, y = 130)

    
    else:
        if nom == "Current":
            dico_joueurs_gagne["Current"] = current_nb_gagne
        elif nom not in list(dico_joueurs_gagne):
            dico_joueurs_gagne[nom] = 0

        racine.title("Perdu")
        img= Image.open('../interface/rouge.png')
        img = img.resize((400, 200))
        img = ImageTk.PhotoImage(img, master = racine)
        label = tk.Label(racine, image = img)
        label.place(x=100, y=75)
        gagne=tk.Label(racine, text = "Vous avez perdu.",font=("Arial", 25))
        perdu = tk.Label(racine, text = f"Le mot cache etait {mot}.")
        gagne.place(x = 180, y = 100)
        perdu.place(x = 225, y = 160)

    #boutons
    restart2 = tk.Button(racine, text="Recommencer une partie à plusieurs joueurs ",
                          command = lambda: fontionrecommencer(dico_joueurs_gagne),font=("Arial", 15))#mettre le code en comman
    restart2.place(x=125, y = 210)
    restart1 = tk.Button(racine, text="Recommencer une partie à 1 joueur",
                          command = lambda: fontionrecommencer(dico_joueurs_gagne),font=("Arial", 15)) 
    restart1.place(x=130, y = 270)

    #nb victoires changer par la fonction
    sessions = tk.Label(racine,text=f"Tu as gagné {dico_joueurs_gagne[nom]} sessions", font=("Arial", 10))
    sessions.place(x = 450, y = 0)
    racine.mainloop()

def destroy_root(root):
    root.destroy()

def root_debut_jeu():
    '''fenetre debut de jeu '''
    global play
    global phrase
    global titre
    global debutjeu 

    debutjeu = tk.Tk()
    debutjeu.title("Jeu du pendu")
    debutjeu.config(bg ="#C0BCB5")
    debutjeu.geometry("950x720")
    debutjeu.resizable(width=False, height=False) 

    #création widgets accueil
    play = tk.Canvas(debutjeu, height=250, width=400, bg ="#C0BCB5", bd='0', highlightthickness=0)
    photo = ImageTk.PhotoImage(Image.open("play1.png")) 
    play.create_image(0,0,anchor = 'nw', image=photo)
    titre=tk.Label(debutjeu, font=('Chalkduster',"30"), text="Le jeu du pendu", bg="#5A5A5A", fg="#C0BCB5")
    phrase=tk.Label(debutjeu, font=('Chalkduster',"15"), text="Allez-vous réussir à échapper à la pendaison ?", fg="#404040", bg='#C0BCB5')
    b_quitter = tk.Button(debutjeu, text = 'Quitter', command = lambda: destroy_root(debutjeu), 
                          relief = 'ridge', bg = '#5C5C5C')
    #placement accueil
    titre.pack(side = 'top', pady= 20)
    play.place(x = 250, y = 150)
    phrase.place(x = 250, y = 430)
    b_quitter.pack(side = 'bottom', pady = 15)

    play.bind("<Button-1>", debut)
    debutjeu.mainloop()

def new_nom(event):
    '''permet de changer le joueur'''
    global joueur   
    global zone_nom
    global nom

    try:
        nom = 'Current'
        joueur.configure(text = "Joueur : ")
        zone_nom = tk.Entry(jeu)
        zone_nom.place(x=60, y=3, anchor='nw')
        zone_nom.bind("<Return>", confirm_nom)
    except: pass

def confirm_nom(event):  
    '''permet de s'autentifier'''
    global joueur   
    global zone_nom
    global nom

    try:
        nom = zone_nom.get()
        joueur.configure(text = "Joueur : "+ nom)
        zone_nom.destroy() 
    except: pass

def confirm_nom1():  
    '''permet de s'autentifier lorsque le jeu recommence'''
    global joueur   
    global zone_nom
    global nom

    joueur.configure(text = "Joueur : "+ nom)
    zone_nom.destroy() 

def creer_croix(event):
    '''barre la lettre choisi'''
    global jeu
    global canvas
    global lettre
    global c_mot
    global lettre_inconnue
    global MOT
    global lettres_images
    global nb_errors
    global videoplayer
    global mot_non_decouvert
    global image_to_lettre, mot_non_decouvert
    
    lettres_images = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7,'h':8, 'i':10, 'j':9, 'k':11, 'l':12,\
                        'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23,\
                        'x':24, 'y':25, 'z':26, 'é':0, 'à':27, "è":28, "ê":29, "ë": 30, "î":31, "ï": 32,\
                        "ö": 33, "ù":34, '-':35, ' ':36, "'":37}
    
    if event.widget == jeu : 
        lettre = event.keysym
        #rechercher la lettre dans les images sur le clavier de l'écran 
        num = image_to_lettre.index(str(lettre)) -1
        # créer la croix qui barre les lettres
        canvas[num].create_line((0,51), (43, 0))
        canvas[num].create_line((0,0), (43, 51))
    else : 
        #ù è ê  _

        event.widget.create_line((0,51), (43, 0))
        event.widget.create_line((0,0), (43, 51))
        try:
            lettre = image_to_lettre[int(str(event.widget)[8:])]
            image_to_lettre[int(str(event.widget)[8:])] = '0'
        except:
            lettre = image_to_lettre[1]
            image_to_lettre[1] = '0'
        
    
        

    if lettre not in MOT and lettre != '0':
        nb_errors += 1
        videoplayer.load(f"../pendu_video/{str(nb_errors)}.mp4") #play the video if lettre not in word
        videoplayer.play()
        if nb_errors == 14:
            for i in canvas:
                i.destroy()
            jeu.geometry("900x600") 
            b_def = tk.Button(jeu, text = f'Definition du mot {MOT}', command = lambda: create_fenetre_def_eni_root(MOT, 'definition'))
            b_def.place(x = 400, y=530)
            gagne_perdu(0, MOT)

    elif lettre != '0':
        for i in range(len(MOT)):
            if MOT[i]==lettre:
                lettre_inconnue[i]=ImageTk.PhotoImage(Image.open(f'./lettres/{str(lettres_images[lettre])}.png'))
                c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])
                mot_non_decouvert-=1

        if mot_non_decouvert == 0:
            for i in canvas:
                i.destroy()
            jeu.geometry("900x600") 
            b_def = tk.Button(jeu, text = f'Definition du mot {MOT}', 
                              command = lambda: create_fenetre_def_eni_root(MOT, 'definition'))
            b_def.place(x = 400, y=530)
            gagne_perdu(1)

def recommencer(jeu):
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

    nb_errors = 0
    mot_non_decouvert = len(MOT)

    image_to_lettre = ['0','é', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j','i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z', 'à', 'è', 'ê', 'ë', 'î', 'ï', 'ö', 'ù', '-', ' ', "'"]

    jeu = tk.Tk()
    jeu.title("Jeu du pendu")
    jeu.config(bg ="#C0BCB5")
    jeu.geometry("950x720")
    jeu.resizable(width=False, height=False) 


    titre1=tk.Label(jeu, font=('Chalkduster',"30"), text="Le jeu du pendu", bg="#404040", fg="#C0BCB5")
    titre1.pack(side="top")
    
    #création du clavier 
    canvas = []
    lettre = []
    for i in range(0,38): 
        canvas.append(tk.Canvas(jeu, bg="#C0BCB5",bd ='0',height=48, width = 40))
        lettre.append(ImageTk.PhotoImage(Image.open('./lettres/%s.png'%i)))
        canvas[i].create_image(3,3,anchor = 'nw',image =lettre[i])
        canvas[i].bind('<Button-1>', creer_croix)

    jeu.bind("<Key>", creer_croix)
    
        
    #placement clavier
    for k in range (0,15):
        canvas[k].place(x = 90+50*k, y=530)
    for k in range (15, 29):
        canvas[k].place(x = 105+50*(k-15), y=590)
    for k in range (29,len(canvas)):
        canvas[k].place(x = 250+50*(k-29), y=650)
    
    #placer video
    c_vid_canvas=tk.Canvas(jeu, width=450, height=350, bg="#404040")
    c_vid_canvas.place(x = 225, y=75)
    videoplayer=TkinterVideo(master = jeu, scaled=True)
    videoplayer.place(x = 250, y=100, height=300, width=400)

    #placer le mot
    c_mot = []
    lettre_inconnue = []
    for i in range(len(MOT)):
        c_mot.append(tk.Canvas( bg="#C0BCB5",bd ='0',height=48, width = 40))
        lettre_inconnue.append(ImageTk.PhotoImage(Image.open('./lettres/tiret.png')))
        c_mot[i].place(x = 450-(40*int(len(MOT)/2))+(40*i), y=445)
        c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])
    
    #enigme
    create_bouton_ask_eni(MOT, jeu, image_to_lettre, nlp)
    print(MOT)


    #entrer informations du jeu
    zone_nom = tk.Entry(jeu)
    zone_nom.bind("<Return>", confirm_nom) 


    joueur = tk.Label(jeu, text = "Joueur :") 
    joueur.bind("<Button-1>", new_nom) 

    zone_nom.place(x=60, y=3, anchor='nw')
    joueur.place(x = 0, y =3, anchor='nw')

    if nom != 'Current':
        confirm_nom1()

    b_recommencer = tk.Button(jeu, text = 'Recommencer', command = lambda: recommencer(jeu), 
                          relief = 'ridge', bg = '#5C5C5C')
    b_recommencer.place(x = 800, y = 20)

    b_quitter = tk.Button(jeu, text = 'Quitter', command = lambda: destroy_root(jeu), 
                          relief = 'ridge', bg = '#5C5C5C')
    b_quitter.place(x = 820, y =50)

    jeu.mainloop()



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
    avant aue le jeu commence'''
    global root
    root = tk.Tk()
    root.title('Pendu')
    root.config(bg ="#C0BCB5")
    root.geometry("600x400") 
    root.resizable(width=False, height=False) 

    titre=tk.Label(root, font=('Chalkduster',"30"), text="Le jeu du pendu", bg="#C0BCB5", fg="#404040")
    titre.place(x = 150, y = 120)
    
    
    l_attendre = tk.Label(root,text = 'Le jeu commencera bientot', font=('Chalkduster',"10"),bg="#C0BCB5", fg="#404040")
    s_attendre = tk.Scale(root, from_ = 0, to = 10 , orient = 'horizontal',bg="#C0BCB5", 
                          showvalue = 0, length = 200,  troughcolor= "#404040")
    
    l_attendre.place(x = 210, y = 200)
    s_attendre.place(x = 190, y = 250)
    
    t1_1 = threading.Thread(target = load_lib_nlp)
    t1_2 = threading.Thread(target = load_lib_glove)

    t1_1.start()
    t1_2.start()
    for i in range(11):
        s_attendre.set(i)
        root.update()
        root.after(500)
    destroy_root(root)
    
    root.mainloop()


wait_load_lib()
root_debut_jeu()




