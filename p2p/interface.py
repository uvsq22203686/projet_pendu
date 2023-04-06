import tkinter as tk
from time import sleep
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

name = ''
root1 = None
t_name = None
t_mot = None
client1 = None
lettre_a_envoyer = ''
new_lettre = False

def send_to_server(client, message, event=None):
    global server_ip1
    #client.sendto(message.encode(), ('localhost', 9999))
    client.sendto(message.encode(), (server_ip1, 7999))

def append_label_utilisateur(root, name, i):
    
    t_utilisateur = tk.Label(root, text = name)
    t_utilisateur.grid(row = (i//4)+2, column = i%4)

def root_attendre_utilisateurs(root, client, server_ip):
    global server_ip1
    server_ip1 = server_ip
    t_title = tk.Label(root, text='On attend des joueurs')
    t_title1 = tk.Label(root, text='Le jeu commencera bientot')
    b_start = tk.Button(root, text='Commencer le jeu', \
                        command = lambda: send_to_server(client,'START_GAME:'))
    #+ gif

    t_title.grid(row = 0, column = 1)
    t_title1.grid(row = 1, column = 1)
    b_start.grid(row = 0, column = 2)
    

def entry_get(event):
    global name
    global t_name
    global root1

    name = t_name.get()
    if name == '':
        t_alert = tk.Label(root1, text="Ecrivez le nom d'utilisateur")
        t_alert.grid(row = 2, column = 0)
    else:
        root1.destroy()
        #destroy_all_widgets(root1)



def root_entry_utilisateur_name1():
    global name
    global t_name
    global root1
    #root1 = root
    root1 = tk.Tk()
    root1.title('Pendu auth')
    
    t_title = tk.Label(root1, text="Ecrivez votre nom d'utilisateur")
    t_name = tk.Entry(root1)

    root1.bind('<Return>', entry_get)
    
    t_title.grid(row = 0, column = 0)
    t_name.grid(row = 1, column = 0)
    root1.mainloop()
    return name

def root_entry_utilisateur_name(root):
    global name
    global t_name
    global root1
    root1 = root
    root.title('Pendu auth')
    
    t_title = tk.Label(root, text="Ecrivez votre nom d'utilisateur")
    t_name = tk.Entry(root)

    root.bind('<Return>', entry_get)
    
    t_title.grid(row = 0, column = 0)
    t_name.grid(row = 1, column = 0)
    return name

def destroy_all_widgets(root):
    for widget in root.winfo_children():
        widget.destroy()

def start_game(root, name):
    destroy_all_widgets(root)
    t_title = tk.Label(root, text=f'{name} a commence le jeu')
    t_title.grid(row = 1, column=1)
    sleep(3)
    destroy_all_widgets(root)

def append_word(event):
    global client1
    global t_mot
    send_to_server(client1, f'MOT:{t_mot.get()}')

def choose_word(root, client):
    global t_mot
    global client1

    client1 = client
    t_title = tk.Label(root, text="Choisissez le mot")
    t_mot = tk.Entry(root)
    root.bind('<Return>', append_word)
    
    t_title.grid(row = 0, column = 0)
    t_mot.grid(row = 1, column = 0)

def wait_choose_word(root, name):
    t_title = tk.Label(root, text=f'{name} choisit le mot')
    t_title.grid(row = 1, column=1)




sys.path.append('../utils')
from choose_words import *
from enigmes import create_bouton_ask_eni, create_fenetre_def_eni_root

sys.path.remove('../utils')
sys.path.append('../interface')
from code2 import gagne_perdu


def fontionrecommencer():
    global jeu
    global racine
    jeu.destroy()
    racine.destroy()
    #recommencer

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

def confirm_nom(event):  
    global joueur   
    global zone_nom
    joueur.configure(text = "Joueur : "+ zone_nom.get())
    zone_nom.destroy() 

def envoyer_lettre(event):
    
    global lettre_a_envoyer
     
    image_to_lettre = "éabcdefghjiklmnopqrstuvwxyzàèêëîïöù- '"
    lettre_a_envoyer = image_to_lettre[int(str(event.widget)[8:])-2]
    print(lettre_a_envoyer)
    #try:
    send_to_server(client1, f'PLAY_GAME_LETTRE:{lettre_a_envoyer}')
    #except AttributeError:
    #    pass

def nouvelle_erreur(canvas):
    global nb_errors
    global videoplayer
    global jeu
    global MOT

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

def creer_croix(lettre, lettre_number, joueur, c_mot, lettre_inconnue, canvas):
    global jeu
    global MOT
    global nb_errors
    global videoplayer
    global mot_non_decouvert


    if lettre not in MOT:
        #try:
        send_to_server(client1, 'PLAY_GAME_ERROR:', event=None)
        #except AttributeError:
        #    pass
        
    else:
        for i in range(len(MOT)):
            if MOT[i]==lettre:
                lettre_inconnue[i]=ImageTk.PhotoImage(Image.open(f'../utils/lettres/{str(lettre_number)}.png'))
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
      
def root_jeu(mot, root):
    #fenetre de jeu 
    global jeu
    global c_mot
    global lettre_inconnue
    global nb_errors
    global videoplayer
    global mot_non_decouvert
    global MOT
    MOT = mot
    jeu = root

    nb_errors = 0
    mot_non_decouvert = len(MOT)

    root.title("Jeu du pendu")
    root.config(bg ="#C0BCB5")
    root.geometry("900x720") 
    titre1=tk.Label(root, font=('Chalkduster',"30"), text="Le jeu du pendu", bg="#404040", fg="#C0BCB5")
    titre1.pack(side="top")
    
    
    #placer video
    c_vid_canvas=tk.Canvas(root, width=450, height=350, bg="#404040")
    c_vid_canvas.place(x = 225, y=75)
    videoplayer=TkinterVideo(master = root, scaled=True)
    videoplayer.place(x = 250, y=100, height=300, width=400)

    
    
    #enigme
    create_bouton_ask_eni(MOT, root)
    print(MOT)


#root_debut_jeu()