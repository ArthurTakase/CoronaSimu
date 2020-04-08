import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import pyautogui
from random import randint
from PIL import Image

screen_size = pyautogui.size()

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def affiche_result(logs, total, screen):
    plot1, plot2 = graph_result(logs, total, screen)
    #window = Tk()

    #img = Image.open('screen/simu'+str(screen)+'.png')
    #img.show()

def graph_result(logs, total, screen):
    # Graphique
    plt.figure(1)
    immu = []
    clean = []
    dead = []
    days = []
    bad = []
    good = []

    for i in range(len(logs)) :
        immu.append(logs[i][2])
        clean.append(logs[i][1])
        dead.append(logs[i][3])
        days.append(logs[i][0])
        bad.append(logs[i][4])
        good.append(total-logs[i][3])

    plt.title("Recapitulatif par jour")
    plt.plot(days, immu, "b--", label="Immu")
    plt.plot(days, clean, "g--", label="Clean")
    plt.plot(days, dead, "k", label="Morts")
    plt.plot(days, bad, "r", label="Malade")
    plt.plot(days, good, "c", label="Vivant")
    plt.ylabel('Results')
    plt.xlabel('days')
    plt.legend()

    plot1 = randint(0,99999)
    plt.savefig('screen/graph'+str(plot1)+'.png')

    # Fromage
    plt.figure(2)

    data = [logs[len(logs)-1][2], logs[len(logs)-1][3], logs[len(logs)-1][1]]
    labels = ['Immu', 'Mort', 'Clean']
    color = ['b', 'k', 'g']
    explode = (0.2, 0.2, 0.2)

    plt.pie(data, colors=color, explode=explode,
            autopct=lambda pct: func(pct, data), shadow=True, textprops={'color':"w"})
    plt.legend(labels)
    plt.title("Bilan de la simulation (total : "+str(total)+")")
    plt.show()
    plot2 = randint(0,99999)
    plt.savefig('screen/pie'+str(plot2)+'.png')

    #Clear
    logs.clear()
    good.clear()

    return plot1, plot2
