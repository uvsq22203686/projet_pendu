import tkinter as tk

def si_lettre_dans_le_mot(lettre, mot, c_mot):
    c_coords = c_mot.coords(c) 
    for i in range(len(mot)):
        if mot[i] == lettre:
            c_mot.create_Image(c_coords[0]+10*i, c_coords[1], c_coords[0]+10*(i+1), c_coords[3], image= f'{lettre}.png')




root = tk.Tk()
width_c = 10
#if width_c*len(mot)> root.winfo_width():
#    width_c = 5
c_mot = tk.Canvas(root, width=width_c*len(mot), height=width_c)


