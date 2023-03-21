from bs4 import BeautifulSoup
import requests
from random import randint
import tkinter as tk
import pickle
import os
from random import randint
import gensim.downloader
from googletrans import Translator
from PIL import Image, ImageTk
#pip install googletrans==3.1.0a0

#fenetre debut de jeu 
debutjeu = tk.Tk()
debutjeu.title("Jeu du pendu")
debutjeu.config(bg ="#C0BCB5")
debutjeu.geometry("900x600")

 
def generer_mot():
    global mot_par_classe, mot_par_len
    creer_mot.destroy()
    mot_par_len = tk.Button(debutjeu,text="Choisir le mot par longueur", command=choix_len)
    mot_par_len.pack(pady=5)
    mot_par_classe = tk.Button(debutjeu, text="Choisir par catégorie", command=choix_classe)
    mot_par_classe.pack(pady =5)

    
def debut(event):
    global creer_mot
    play.destroy()
    phrase.destroy()
    titre.config(font=('Chalkduster',"30"))
    creer_mot = tk.Button(debutjeu,text="Générer un mot", command=generer_mot)
    creer_mot.pack(fill ='y', side= 'top')
    

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


def choix_len():
    global entry_len
    entry_len = tk.Entry(debutjeu)
    entry_len.pack(side='bottom')
    entry_len.bind("<Return>", config_len)
    
def config_len(event):
    global len_user
    len_user = int(entry_len.get())
    get_words_sorted_by_len(len_user)
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
    class_user = str(entry_classe.get())
    get_words_sorted_by_cat(class_user)
    mot_par_len.destroy()
    mot_par_classe.destroy()
    entry_classe.destroy()
    debutjeu.destroy()
    

debutjeu.mainloop()

#fenetre de jeu 
jeu = tk.Tk()
jeu.title("Jeu du pendu")
jeu.config(bg ="#C0BCB5")
jeu.geometry("900x600") 
titre1=tk.Label(jeu, font=('Chalkduster',"30"), text="Le jeu du pendu", bg="#404040", fg="#C0BCB5")
titre1.pack(side="top")

#création du clavier 
canvas = []
lettre = []
for i in range(0,27): 
    canvas.append(tk.Canvas(jeu, bg="#C0BCB5",bd ='0',height=48, width = 40))
    lettre.append(ImageTk.PhotoImage(Image.open('%s.png'%i)))
    canvas[i].create_image(3,3,anchor = 'nw',image =lettre[i])

#placement clavier
a = 40 
b= 500
for k in range (18,27):
    canvas[k].place(x = a+50, y=b)
    a+=50
a =55
b = 430
for k in range (10,18):
    canvas[k].place(x = a+50, y=b)
    a+=50
a = 40 
b = 360
for k in range (1,10):
    canvas[k].place(x = a+50, y=b)
    a += 50
canvas[0].place(x = 300,y=290)


def confirm_nom(event):     
    joueur.configure(text = "Joueur : "+ zone_nom.get())
    zone_nom.destroy()   
 
#entrer informations du jeu
zone_nom = tk.Entry(jeu)
zone_nom.bind("<Return>", confirm_nom) 
joueur = tk.Label(jeu, text = "Joueur :") 

zone_nom.place(x=60, y=0, anchor='nw')
joueur.place(x = 0, y =3, anchor='nw')


jeu.mainloop()