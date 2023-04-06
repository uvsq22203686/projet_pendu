import socket
import threading
from random import randint
import tkinter as tk
from time import sleep
from bs4 import BeautifulSoup
import requests
import pickle
import os
import gensim.downloader
from googletrans import Translator
from PIL import Image, ImageTk
import sys
from tkVideoPlayer import TkinterVideo

sys.path.append('./')
from interface import *


def start_client(server_ip):
    global root
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client.bind(('localhost', randint(8000,9000)))
    print(client)
    root = None
    #have_root = False
    #condition = threading.Condition()


    def receive():
        global root
        global client
        
        while True:
            #try:
            print('a')
            message, _ = client.recvfrom(1024)
            if message.decode().startswith('ATTENDRE_JOUEURS'):
                print('b')
                if message.decode().startswith('ATTENDRE_JOUEURS_FIRST:'):
                    names = message.decode()[message.decode().index(':')+1:].split(',')
                    root_attendre_utilisateurs(root, client, server_ip)
                    for i in range(len(names[:-1])):
                        #print(i)
                        append_label_utilisateur(root, names[i], i)
                    
                else:
                    names = message.decode()[message.decode().index(':')+1:].split(',')
                    append_label_utilisateur(root, names[-2], len(names)-2)

            elif message.decode().startswith('START_GAME'):
                print('b')
                info = message.decode()[message.decode().index(':')+1:].split(',')
                #print(name)
                start_game(root, info[0])
                #play_game(root, name)
                if message.decode().startswith('START_GAME_CHOIX'):
                    choose_word(root, client)
                else:
                    wait_choose_word(root, info[1])
                
            elif message.decode().startswith('PLAY_GAME'):
                print('b')
                if message.decode().startswith('PLAY_GAME:'):
                    destroy_all_widgets(root)
                    mot = message.decode()[message.decode().index(':')+1:]
                    root_jeu(mot, root)
                    #création du clavier 
                    canvas = []
                    lettre = []
                    for i in range(0,38): 
                        canvas.append(tk.Canvas(root, bg="#C0BCB5",bd ='0',height=48, width = 40))
                        lettre.append(ImageTk.PhotoImage(Image.open(f'../utils/lettres/{str(i)}.png')))
                        canvas[i].bind('<Button-1>', envoyer_lettre)
                        canvas[i].create_image(3,3,anchor = 'nw',image =lettre[i])

                    #placement clavier
                    for k in range (0,15):
                        canvas[k].place(x = 90+50*k, y=530)
                    for k in range (15, 29):
                        canvas[k].place(x = 105+50*(k-15), y=590)
                    for k in range (29,len(canvas)):
                        canvas[k].place(x = 250+50*(k-29), y=650)
                    
                    #placer le mot
                    c_mot = []
                    lettre_inconnue = []
                    for i in range(len(mot)):
                        c_mot.append(tk.Canvas( bg="#C0BCB5",bd ='0',height=48, width = 40))
                        lettre_inconnue.append(ImageTk.PhotoImage(Image.open('../utils/lettres/tiret.png')))
                        c_mot[i].place(x = 450-(40*int(len(mot)/2))+(40*i), y=445)
                        c_mot[i].create_image(3,3, anchor = 'nw',image = lettre_inconnue[i])

                elif message.decode().startswith('PLAY_GAME_LETTRE:'):
                    
                    lettre1 = message.decode()[message.decode().index(':')+1:].split(',')
                    joueur = lettre1[1]
                    lettre1 = lettre1[0]

                    lettres_images = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7,'h':8, 'i':10, 'j':9, 'k':11, 'l':12,\
                                        'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23,\
                                        'x':24, 'y':25, 'z':26, 'é':0, 'à':27, "è":28, "ê":29, "ë": 30, "î":31, "ï": 32,\
                                        "ö": 33, "ù":34, '-':35, ' ':36, "'":37}
                    #ù è ê  _
                    lettre_number = lettres_images[lettre1]
                    c = canvas[lettre_number]
                    c.create_line((0,51), (43, 0))
                    c.create_line((0,0), (43, 51))

                    creer_croix(lettre1, lettre_number, joueur, c_mot, lettre_inconnue, canvas)
                    

                elif message.decode().startswith('PLAY_GAME_ERROR:'):
                    
                    nouvelle_erreur(canvas)
                

                
            
            '''
            elif придумать универсальную функцию которая по названию кнопки определяет что включить
            
            message.decode().startswith('START_GAME:'):
                name = message.decode()[message.decode().index(':')+1:]
                print(name)
                start_game(root, name)
                #play_game(root, name)
            '''

        #print(message.decode())
            #except:
            # pass
    def build_root():
        global root
        #global have_root
        root = tk.Tk()
        root.title('Pendu')
        root.mainloop()





    #while True:
        #message = input("")
        #if message == '!q':
        #    exit()
        #else:
        #client.sendto(print1.encode(), ('localhost', 9999))
    #client.sendto(f"USER_NAME: {root_entry_utilisateur_name1()}".encode(), ('localhost', 9999))
    client.sendto(f"USER_NAME: {root_entry_utilisateur_name1()}".encode(), (server_ip, 7999))
    t3 = threading.Thread(target = build_root)
    t3.start()
    t1 = threading.Thread(target = receive)
    t1.start()


def destroy_root_and_start2(event):
    global root3
    global e_ip
    ip = e_ip.get()
    root3.destroy()
    start_client(ip)

def second_player():
    global root3
    global e_ip
    root3 = tk.Tk()
    t_title = tk.Label(root3, text="Entrez le code")
    e_ip = tk.Entry(root3)

    root3.bind('<Return>', destroy_root_and_start2)
    
    t_title.grid(row = 0, column = 0)
    e_ip.grid(row = 1, column = 0)
    root3.mainloop()


#start_client()
second_player()