import tkinter as tk
import PIL as pil
import tkinter.font as font
from PIL import Image
from PIL import ImageTk 
from tkinter import StringVar, filedialog, simpledialog, messagebox
import numpy as np 
from PIL import Image, ImageTk
import sys


def fontionrecommencer():
    L=tk.Label(racine, text="Remplacer cette fontion par la fonction qui recommence", bg="red")
    L.place(x=10, y=0)

def gagne_perdu(gagne_perdu, mot = ''):
    racine = tk.Tk()
    racine.geometry("600x350")
    
    if gagne_perdu:
        racine.title("Gagne!")
        print(sys.path[0])
        #changer le path!
        img=Image.open(sys.path[0]+'\\CONFETTIS 2.png')
        img = img.resize((600, 350))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(racine, image = img)
        label.place(x=0, y=0)
        gagne=tk.Label(racine, text = "Félicitations vous avez gagné !")
        gagne.place(x = 75, y = 130)
    
    else:
        racine.title("Perdu")
        img=Image.open('rouge.png')
        img = img.resize((400, 200))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(racine, image = img)
        label.place(x=100, y=75)
        gagne=tk.Label(racine, text = "Vous avez perdu.")
        perdu = tk.Label(racine, text = f"Le mot cache etait {mot}.")
        gagne.place(x = 180, y = 100)
        perdu.place(x = 225, y = 160)
    
    #img = tk.PhotoImage(file = "CONFETTIS 2.png")
    #label.place(x=0, y=0, relwidth=1,relheight = 1)
    #probleme : la phot ne prend pas toute la fenetre quand on la met en grand écran je sais pas si c'est normal 
    #changer d'image

    #écriture   
    police = font.Font(size = 25)
    gagne['font'] = police

    #boutons
    restart2 = tk.Button(text="Recommencer une partie à 2 joueurs ", command = fontionrecommencer)#mettre le code en comman
    restart2.place(x=125, y = 210)
    restart1 = tk.Button(text="Recommencer une partie à 1 joueur", command = fontionrecommencer) 
    restart1.place(x=130, y = 270)
    policeB = font.Font(size = 15)
    restart1['font'] = policeB
    restart2['font'] = policeB
    #nombre de sessions gagnées 
    #nb victoires changer par la fonction
    victoires = 3
    sessions = tk.Label(racine,text=f"Tu as gagné {victoires} sessions")
    sessions.place(x = 450, y = 0)
    vic = font.Font(size = 10)
    sessions['font'] = vic
    racine.mainloop()


# fonctions qui permettent d'afficher les indications par rapport aux emplacements des widgets 
def aide() :
    l = tk.Label(racine, text = "← clique ici pour avoir un indice sur le mot secret")
    l.place(x=500, y=0)
    l2 = tk.Label(racine, text="← clique ici pour générer un mot au hasard")

    l2.place(x=50, y = 200) #pb : je ne sais pas comment faire pour enlever les écritures quand y'a plus besoin
#fonction qui permet de donner un indice sur une lettre du mot secret 
def indiceslettres(event) :
    if event.widget == indices :
        vraifonction()

def vraifonction(mot, mask) :
    MotVar = StringVar(value = mot)

    for i in range(len(mot)):
        #changer la prise en prise 
        if mask[i]== "non prise" :
            j= "La", i+1, "eme lettre est", mot[i]
    v = tk.Label(textvariable = MotVar)
    hidden_word = "*" * len(mot)

    for k in range(len(mot)):

            if mot[k]==input_letter:                     #input_letter -> fonction à revoir lors du dev de l'entrée utilisateur
                hidden_word = hidden_word[:k] + input_letter + hidden_word[k+1:]
                MotVar.set(value=hidden_word)
                
    #demander a jules pour completer la fontion 
    #indices = tk.Button(text="Indices", command = indiceslettres)
    #indices.grid(column = 100, row = 10)

def aide1():
    racine = tk.Tk()
    racine.title("Indications")
    racine.geometry("1242x790")
    b1 = tk.Button(text= "Indice", bg ="red")
    b2 = tk.Button(text= "Générer un mot", bg="blue")
    b1.place(x = 0, y =200)
    b3 = tk.Button(text = "Aide", command = aide)
    b3.place(x = 300, y = 300)
    b2.place(x=400, y=0)

    racine.mainloop()
            
        


   

