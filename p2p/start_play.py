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
import queue
import threading

sys.path.append('./')
from client2 import *

def destroy_root_and_start():
    global root4
    root4.destroy()
    start_client('localhost')

def first_player():
    global root4
    root4 = tk.Tk()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(ip)
    l_your_ip = tk.Label(root4, text = f'Envoyer ce code aux joueurs:{ip}')
    button = tk.Button(root4, text = 'Si vous avez copie le code clickez ici', command = destroy_root_and_start)
    l_your_ip.grid(column = 1, row = 1)
    button.grid(column = 1, row = 2)
    root4.mainloop()

first_player()
