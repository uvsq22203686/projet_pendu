import tkinter as tk
import PIL as pil
import tkinter.font as font
from PIL import Image
from PIL import ImageTk 
from tkinter import StringVar
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np 



gagneperd = 0 # variable a laquelle on ajoute +1 ou -1 a chaque fois que le joueur perd ou gagne

def fontionrecommencer() :
    L=tk.Label(racine, text="Remplacer cette fontion par la fonction qui recommence", bg="red")
    L.place(x=10, y=0)

if gagneperd >= 1 :
    racine = tk.Tk()
    racine.title("Pop up gagné/perdu")
    racine.geometry("1063x752")
    can = tk.Canvas(bg ="gray16", width = 1063, height = 752 )
    img = tk.PhotoImage(file = "CONFETTIS 2.png")
    label = tk.Label(racine, image = img)
    label.place(x=0, y=0, relwidth=1,relheight = 1)
#probleme : la phot ne prend pas toute la fenetre quand on la met en grand écran je sais pas si c'est normal 
#changer d'image

#écriture 
    gagne=tk.Label(racine, text = "Félicitations vous avez gagné !")
    gagne.place(x = 100, y = 200)
    police = font.Font(size = 50)
    gagne['font'] = police
#boutons
    restart2 = tk.Button(text="Recommencer une partie à 2 joueurs ", command = fontionrecommencer)#mettre le code en comman
    restart2.place(x=300, y = 320)
    restart1 = tk.Button(text="Recommencer une partie à 1 joueur", command = fontionrecommencer) 
    restart1.place(x=310, y = 400)
    policeB = font.Font(size = 20)
    restart1['font'] = policeB
    restart2['font'] = policeB
#nombre de sessions gagnées 
    victoires = 3
    sessions = tk.Label(racine,text="Tu as gagné x sessions") # je ne sais pas comment remplacer le x par une variable 
    sessions.place(x = 750, y = 0)
    vic = font.Font(size = 20)
    sessions['font'] = vic
    racine.mainloop()

else :
    racine = tk.Tk()
    racine.title("Pop up gagné/perdu")
    racine.geometry("1000x1000")
    can = tk.Canvas(bg ="black", width = 500, height = 500 )
    img = tk.PhotoImage(file = "rouge.png")
    label = tk.Label(racine, image = img)
    label.place(x=0, y=0, relwidth=1,relheight = 1)
#probleme : la phot ne prend pas toute la fenetre quand on la met en grand écran je sais pas si c'est normal 
#changer d'image
#je dois remplacer par un pack pour que le background prenne toute la place de l'écran 
#écriture 
    gagne=tk.Label(racine, text = "Vous avez perdu !")
    gagne.place(x = 350, y = 250)
    police = font.Font(size = 50)
    gagne['font'] = police
#boutons
    restart2 = tk.Button(text="Recommancer une partie à 2 joueurs ", command = fontionrecommencer)#mettre le code en comman
    restart2.place(x=360, y = 350)
    restart1 = tk.Button(text="Recommencer une partie à 1 joueur", command = fontionrecommencer) 
    restart1.place(x=360, y = 410)
    policeB = font.Font(size = 20)
    restart1['font'] = policeB
    restart2['font'] = policeB
#nombre de sessions gagnées 
    victoires = 3
    j=victoires, "sessions gagnées"
    sessions = tk.Label(racine,text=j) # je ne sais pas comment remplacer le x par une variable 
    sessions.place(x = 900, y = 0)
    vic = font.Font(size = 20)
    sessions['font'] = vic
    # code à modifier selon l'image qu'on mettra au fond
    racine.mainloop()


# fonctions qui permettent d'afficher les indications par rapport aux emplacements des widgets 
def aide() :
    l = tk.Label(racine, text = "← clique ici pour avoir un indice sur le mot secret")
    l.place(x=500, y=0)
    l2 = tk.Label(racine, text="← clique ici pour générer un mot au hasard")
    l2.place(x=50, y = 200) #pb : je ne sais pas comment faire pour enlever les écritures quand y'a plus besoin

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


indices = tk.Button(text="Indices", command = indiceslettres)
indices.grid(column = 100, row = 10)
