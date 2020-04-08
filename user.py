from tkinter import *
import pyautogui
from random import randint
from random import uniform
from simu import *

window = Tk()
screen_size = pyautogui.size()

def random_scale():
    people_s.set(randint(50,screen_size[0]//2))
    danger_s.set(randint(1,100))
    gueri_s.set(uniform(0.01,100))
    mort_s.set(uniform(0.01,100))
    vaccin_s.set(randint(0,100))

def get_user():
    parametre = []

    parametre.append(people_s.get())
    parametre.append(danger_s.get())
    parametre.append(gueri_s.get())
    parametre.append(mort_s.get())
    parametre.append(vaccin_s.get())

    window.destroy()
    print(parametre)
    is_launch = True
    main(parametre)

#Création des échelles
people_s = Scale(window, from_=0, to=screen_size[0]//2, orient=HORIZONTAL, length=300)
danger_s = Scale(window, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=300)
gueri_s = Scale(window, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=300)
mort_s = Scale(window, from_=0, to=100, resolution=0.1, orient=HORIZONTAL, length=300)
vaccin_s = Scale(window, from_=0, to=100, orient=HORIZONTAL, length=300)
#Création des boutons
start_b = Button(window, text='[ Start ]', command=get_user)
random_b = Button(window, text='[ Random ]', command=random_scale)
about_b = Button(window, text='[ About ]')
#Création des textes
title_l = Label(window, text='---- CORONASIMU ----')
people_l = Label(window, text='Personne/ligne')
danger_l = Label(window, text='Contagiosité (%)')
gueri_l = Label(window, text='Guérison par jour (%)')
mort_l = Label(window, text='Mortalité par jour (%)')
vaccin_l = Label(window, text='Immunisée (%)')

#Placement provisoire des widgets
#Ligne 1
title_l.grid(row=1, column=2, columnspan=10)
#Ligne 2
people_s.grid(row=2, column=2, padx=(10,0))
danger_s.grid(row=2, column=4, padx=(0,10))
#Ligne 3
people_l.grid(row=3, column=2, padx=(20,0))
danger_l.grid(row=3, column=4, padx=(5,10))
#Ligne 4
gueri_s.grid(row=4, column=2, padx=(10,0))
mort_s.grid(row=4, column=4, padx=(0,10))
#Ligne 5
gueri_l.grid(row=5, column=2, padx=(20,0))
mort_l.grid(row=5, column=4, padx=(5,10))
#Ligne 6
vaccin_s.grid(row=6, column=2, padx=(10,0))
#Ligne 7
vaccin_l.grid(row=7, column=2, pady=(0,10), padx=(20,0))
#Ligne 8
start_b.grid(row=8, column=3, pady=(0,10))
random_b.grid(row=8, column=2, pady=(0,10))
about_b.grid(row=8, column=4, pady=(0,10))

window.mainloop()
