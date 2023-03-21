import tkinter as tk
from tkVideoPlayer import TkinterVideo
from threading import Thread

root = None
mot_trouve = False

def try_letter():
    global root
    global mot_trouve

    nb_errors = 0
    videoplayer=TkinterVideo(master = root, scaled=True)
    videoplayer.pack(side = 'left', expand=True, fill="both")

    while True:
        a = input()
        # au lieu de input() mettre les fonctions 'attendre le choix de la lettre' et 'lettre dans le mot?'
        if nb_errors==14 or mot_trouve:
            #appeler la fonction vous avez perdu
            print('fin')
            break
        if a != 'a':
            nb_errors+=1
            videoplayer.load(f"{str(nb_errors)}.mp4")
            videoplayer.play()


def play_pendu():
    global root
    global mot_trouve
    t1 = Thread(target = try_letter)
    root = tk.Tk()
    root.geometry('300x300')
    root.resizable(0,0)
    t1.start()
    root.mainloop()

play_pendu()