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
from threading import Thread
from tkVideoPlayer import TkinterVideo

sys.path.append('./utils')
from choose_words import *
from enigmes import create_bouton_ask_eni

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
    len_user = int(entry_len.get())
    MOT = get_words_sorted_by_len(len_user)
    #! list mot + error
    mot_par_len.destroy()
    mot_par_classe.destroy()
    entry_len.destroy()
    debutjeu.destroy()

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
    mot_par_len.destroy()
    mot_par_classe.destroy()
    entry_classe.destroy()
    debutjeu.destroy()

def play_video1():
    global jeu
    #global mot_trouve

    nb_errors = 0
    c_vid_canvas=tk.Canvas(jeu, width=450, height=350, bg="#404040")
    c_vid_canvas.place(x = 225, y=75)
    videoplayer=TkinterVideo(master = jeu, scaled=True)
    #videoplayer.pack(side = 'top', fill="both")
    videoplayer.place(x = 250, y=100, height=300, width=400)

    while True:
        a = input()
        # au lieu de input() mettre les fonctions 'attendre le choix de la lettre' et 'lettre dans le mot?'
        #if nb_errors==14 or mot_trouve:
        if nb_errors==14:
            #appeler la fonction vous avez perdu
            print('fin')
            break
        if a != 'a':
            nb_errors+=1
            videoplayer.load(f"../pendu_video/{str(nb_errors)}.mp4")
            videoplayer.play()

def play_video():
    global jeu
    global nb_errors
    global new_error
    #global mot_trouve
    c_vid_canvas=tk.Canvas(jeu, width=450, height=350, bg="#404040")
    c_vid_canvas.place(x = 225, y=75)
    videoplayer=TkinterVideo(master = jeu, scaled=True)
    #videoplayer.pack(side = 'top', fill="both")
    videoplayer.place(x = 250, y=100, height=300, width=400)

    while True:
        if new_error:
            videoplayer.load(f"../pendu_video/{str(nb_errors)}.mp4")
            videoplayer.play()
            new_error = False

        if nb_errors==14:
            
            print('fin')
            break
            

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
    #placement accueil
    titre.pack(side='top', pady='15')
    play.pack()
    phrase.pack(side = 'bottom')

    play.bind("<Button-1>", debut)
    debutjeu.mainloop()

def confirm_nom(event):  
    global joueur   
    global zone_nom
    joueur.configure(text = "Joueur : "+ zone_nom.get())
    zone_nom.destroy() 


def creer_croix(event):
    global c_mot
    global lettre_inconnue
    global MOT
    global nb_errors
    global new_error

    image_to_lettre = 'éabcdefghjiklmnopqrstuvwxyz'
    lettres_images = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7,'h':8, 'i':10, 'j':9, 'k':11, 'l':12,\
                    'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23,\
                    'x':24, 'y':25, 'z':26, 'é':0}
    #ù è ê  _

    event.widget.create_line((0,51), (43, 0))
    event.widget.create_line((0,0), (43, 51))
    mot = MOT[0].lower()
    lettre = image_to_lettre[int(str(event.widget)[8:])-1]
    print(str(event.widget)[8:], lettre, lettres_images[lettre])
    if lettre not in mot:
        nb_errors += 1
        new_error = True
    for i in range(len(mot)):
        if mot[i]==lettre:
            lettre_inconnue[i]=ImageTk.PhotoImage(Image.open(f'{str(lettres_images[lettre])}.png'))
            c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])
    
    

    

def root_jeu():
    #fenetre de jeu 
    global joueur
    global jeu
    global zone_nom
    global canvas
    global c_mot
    global lettre_inconnue
    global nb_errors
    global new_error
    t_play_video = Thread(target = play_video)

    nb_errors = 0
    new_error = False

    jeu = tk.Tk()
    jeu.title("Jeu du pendu")
    jeu.config(bg ="#C0BCB5")
    jeu.geometry("900x660") 
    titre1=tk.Label(jeu, font=('Chalkduster',"30"), text="Le jeu du pendu", bg="#404040", fg="#C0BCB5")
    titre1.pack(side="top")

    #création du clavier 
    canvas = []
    lettre = []
    for i in range(0,27): 
        canvas.append(tk.Canvas(jeu, bg="#C0BCB5",bd ='0',height=48, width = 40))
        lettre.append(ImageTk.PhotoImage(Image.open('%s.png'%i)))
        canvas[i].create_image(3,3,anchor = 'nw',image =lettre[i])
        canvas[i].bind('<Button-1>', creer_croix)

    #placement clavier
    for k in range (0,15):
        canvas[k].place(x = 90+50*k, y=530)
    for k in range (15,len(canvas)):
        canvas[k].place(x = 105+50*(k-15), y=600)
    
    #placer le mot
    c_mot = []
    lettre_inconnue = []
    mot = MOT[0].lower()
    for i in range(len(mot)):
        c_mot.append(tk.Canvas( bg="#C0BCB5",bd ='0',height=48, width = 40))
        lettre_inconnue.append(ImageTk.PhotoImage(Image.open('1.png')))
        c_mot[i].place(x = 450-(40*int(len(mot)/2))+(40*i), y=445)
        c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])
    
    #enigme
    create_bouton_ask_eni(mot, jeu)
    print(mot)

    #start of video
    t_play_video.start()


    #entrer informations du jeu
    zone_nom = tk.Entry(jeu)
    zone_nom.bind("<Return>", confirm_nom) 
    joueur = tk.Label(jeu, text = "Joueur :") 

    zone_nom.place(x=60, y=0, anchor='nw')
    joueur.place(x = 0, y =3, anchor='nw')


    jeu.mainloop()

root_debut_jeu()
root_jeu()