from bs4 import BeautifulSoup
import requests
from random import randint
import tkinter as tk
import pickle
import os
import gensim.downloader
from googletrans import Translator
from PIL import Image, ImageTk
import sys
from tkVideoPlayer import TkinterVideo

sys.path.append('./utils')
from choose_words import *
from enigmes import create_bouton_ask_eni, create_fenetre_def_eni_root

sys.path.remove('./utils')
sys.path.append('../interface')
from code2 import gagne_perdu

def generer_mot():
    global mot_par_classe, mot_par_len
    creer_mot.destroy()
    mot_par_len = tk.Button(debutjeu,text="Choisir le mot par longueur", command=choix_len)
    mot_par_len.pack(pady=5)
    mot_par_classe = tk.Button(debutjeu, text="Choisir par catégorie", command=choix_classe)
    mot_par_classe.pack(pady =5)

def debut(event):
    global creer_mot
    global play
    global phrase
    global titre

    play.destroy()
    phrase.destroy()
    titre.config(font=('Chalkduster',"30"))
    creer_mot = tk.Button(debutjeu,text="Générer un mot", command=generer_mot)
    creer_mot.pack(fill ='y', side= 'top')

def choix_len():
    global entry_len
    entry_len = tk.Entry(debutjeu)
    entry_len.pack(side='bottom')
    entry_len.bind("<Return>", config_len)

def config_len(event):
    global len_user
    global MOT
    global debutjeu
    len_user = int(entry_len.get())
    MOT = get_words_sorted_by_len(len_user)
    if MOT[-1]:
        t_alert = tk.Label(debutjeu, text=MOT[0])
        t_alert.pack(side = 'top')
    else:
        MOT = MOT[0].lower()
        debutjeu.destroy()
        root_jeu()

def choix_classe():
    global entry_classe
    entry_classe = tk.Entry(debutjeu)
    entry_classe.pack(side = 'bottom')
    entry_classe.bind("<Return>",config_classe)
    
def config_classe(event):
    global class_user
    global debutjeu 
    global MOT
    class_user = str(entry_classe.get())
    MOT = get_words_sorted_by_cat(class_user)
    if MOT[-1]:
        t_alert = tk.Label(debutjeu, text=MOT[0])
        t_alert.pack(side = 'top')
    else:
        MOT = MOT[0].lower()
        debutjeu.destroy()
        root_jeu()

def fontionrecommencer():
    global jeu
    global racine
    jeu.destroy()
    racine.destroy()
    root_debut_jeu()

def gagne_perdu(gagne_perdu, mot = ''):
    global racine
    racine = tk.Tk()
    racine.geometry("600x350")
    
    if gagne_perdu:
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
    restart2 = tk.Button(racine, text="Recommencer une partie à plusieurs joueurs ", command = fontionrecommencer,font=("Arial", 15))#mettre le code en comman
    restart2.place(x=125, y = 210)
    restart1 = tk.Button(racine, text="Recommencer une partie à 1 joueur", command = fontionrecommencer,font=("Arial", 15)) 
    restart1.place(x=130, y = 270)

    #nb victoires changer par la fonction
    victoires = 3
    sessions = tk.Label(racine,text=f"Tu as gagné {victoires} sessions", font=("Arial", 10))
    sessions.place(x = 450, y = 0)
    racine.mainloop()

def destroy_root(root):
    root.destroy()

def root_debut_jeu():
    #fenetre debut de jeu 
    global play
    global phrase
    global titre
    global debutjeu 

    debutjeu = tk.Tk()
    debutjeu.title("Jeu du pendu")
    debutjeu.config(bg ="#C0BCB5")
    debutjeu.geometry("900x600")

    #création widgets accueil
    play = tk.Canvas(debutjeu, height=250, width=400, bg ="#C0BCB5", bd='5')
    photo = ImageTk.PhotoImage(Image.open("play1.png")) 
    play.create_image(0,0,anchor = 'nw', image=photo)
    titre=tk.Label(debutjeu, font=('Chalkduster',"50"), text="Le jeu du pendu", bg="#404040", fg="#C0BCB5")
    phrase=tk.Label(debutjeu, font=('Chalkduster',"30"), text="Allez-vous réussir à échapper à la pendaison ?", fg="#404040", bg='#C0BCB5')
    b_quitter = tk.Button(debutjeu, text = 'Quitter', command = lambda: destroy_root(debutjeu))
    #placement accueil
    titre.pack(side='top', pady='15')
    play.pack()
    phrase.pack(side = 'bottom')
    b_quitter.pack(side = 'bottom')

    play.bind("<Button-1>", debut)
    debutjeu.mainloop()

def confirm_nom(event):  
    global joueur   
    global zone_nom
    joueur.configure(text = "Joueur : "+ zone_nom.get())
    zone_nom.destroy() 

def creer_croix(event):
    global jeu
    global canvas
    global c_mot
    global lettre_inconnue
    global MOT
    global nb_errors
    global videoplayer
    global mot_non_decouvert

    image_to_lettre = "éabcdefghjiklmnopqrstuvwxyzàèêëîïöù- '"
    lettres_images = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7,'h':8, 'i':10, 'j':9, 'k':11, 'l':12,\
                    'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23,\
                    'x':24, 'y':25, 'z':26, 'é':0, 'à':27, "è":28, "ê":29, "ë": 30, "î":31, "ï": 32,\
                     "ö": 33, "ù":34, '-':35, ' ':36, "'":37}
    #ù è ê  _

    event.widget.create_line((0,51), (43, 0))
    event.widget.create_line((0,0), (43, 51))
    lettre = image_to_lettre[int(str(event.widget)[8:])-1]
    #print(str(event.widget)[8:], lettre, lettres_images[lettre])

    if lettre not in MOT:
        nb_errors += 1
        videoplayer.load(f"../pendu_video/{str(nb_errors)}.mp4")
        videoplayer.play()
        if nb_errors == 14:
            for i in canvas:
                i.destroy()
            jeu.geometry("900x600") 
            b_def = tk.Button(jeu, text = f'Definition du mot {MOT}', command = lambda: create_fenetre_def_eni_root(MOT, 'definition'))
            b_def.place(x = 400, y=530)
            gagne_perdu(0, MOT)
    else:
        for i in range(len(MOT)):
            if MOT[i]==lettre:
                lettre_inconnue[i]=ImageTk.PhotoImage(Image.open(f'./lettres/{str(lettres_images[lettre])}.png'))
                c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])
                mot_non_decouvert-=1
                print(mot_non_decouvert)
        if mot_non_decouvert == 0:
            for i in canvas:
                i.destroy()
            jeu.geometry("900x600") 
            b_def = tk.Button(jeu, text = f'Definition du mot {MOT}', command = lambda: create_fenetre_def_eni_root(MOT, 'definition'))
            b_def.place(x = 400, y=530)
            gagne_perdu(1)
      
def root_jeu():
    #fenetre de jeu 
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

    nb_errors = 0
    mot_non_decouvert = len(MOT)

    jeu = tk.Tk()
    jeu.title("Jeu du pendu")
    jeu.config(bg ="#C0BCB5")
    jeu.geometry("900x720") 
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
    create_bouton_ask_eni(MOT, jeu)
    print(MOT)


    #entrer informations du jeu
    zone_nom = tk.Entry(jeu)
    zone_nom.bind("<Return>", confirm_nom) 
    joueur = tk.Label(jeu, text = "Joueur :") 

    zone_nom.place(x=60, y=0, anchor='nw')
    joueur.place(x = 0, y =3, anchor='nw')


    b_quitter = tk.Button(jeu, text = 'Quitter', command = lambda: destroy_root(jeu))
    b_quitter.pack(side='bottom')

    jeu.mainloop()

root_debut_jeu()
