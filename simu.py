# ------------------------------------------------------------------------------
# Projet : CoronaSimu, Simulation de propagation de maladies
# Version : 1.0
# Auteur : Arthur DECAEN
# Fonction du fichier :  Affichage et gestion de la simulation. Transmission des
#                        donnés au fichier result.py.
# ------------------------------------------------------------------------------

import time
from random import randint
import pygame
from pygame.locals import *
import pyautogui
from result import *


# Variables globales
danger, people, danger, gueri, mort, vaccin = 0, 0, 0, 0, 0, 0
lenthx, lenthy = 0, 0
xmax, ymax = 0, 0
day = 0
day_logs = []
total = 0
is_dead = True
is_check = []

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption('CoronaSimu')


# Permet d'écire facilement des textes
def text_draw(text, position, color, size, screen):
    '''Fonction permettant de créer des textes dans une interface Pygame.
    Utilisation : text_draw("votre texte", (positionx, positiony), couleur, taille).
    Ne retourne rien.'''
    myfont = pygame.font.SysFont('Arial', size)
    textsurface = myfont.render(text, True, color)
    screen.blit(textsurface,position)


# tableau pour savoir si une case à été modifiée
def tab_check_true(day, screen, humain):
    '''Fonction permettant de set les valeurs de chaque case en début de chaque journée.
    Les cases True sont des cases non visitées.
    Les cases False sont déjà visitées et ne seront pas comptées pour le reste de la journée.
    Ne retourne rien.'''
    global is_check, people, danger, gueri, mort, vaccin, lenthx, lenthy, xmax, ymax
    is_check.clear()
    is_check_line = []

    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
                is_check_line.append(True)
        is_check.append(is_check_line)
        is_check_line = []


# Création de la population test
def gen_virus(day, screen, humain):
    '''Fonction permettant de générer une population dans laquelle le virus va se propager.
    la population ne peut depasser le nombre de pixel sur l'écran (sur un écran 1080p, 2 073 600 personnes).
    Ne retourne rien.'''
    global is_check, people, danger, gueri, mort, vaccin, lenthx, lenthy, xmax, ymax
    is_check_line = []

    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if x == (xmax//2) * lenthx and y == (ymax//2) * lenthy:
                pygame.draw.rect(humain, RED, (x,y,lenthx,lenthy))
            elif randint(0,100) < vaccin :
                pygame.draw.rect(humain, BLUE, (x,y,lenthx,lenthy))
            else :
                pygame.draw.rect(humain, GREEN, (x,y,lenthx,lenthy))

    screen.blit(humain,(0,0))
    pygame.display.update()
    tab_check_true(day, screen, humain)


# Compte chaque jour pour les informations finales
def compte(day, screen, humain):
    '''Fonction permettant de compter chaque jour le nombre de personne de chaque catégorie.
    Retourne une liste [jour, sains, immunisés, morts, malades].'''
    global total, people, danger, gueri, mort, vaccin, lenthx, lenthy, xmax, ymax

    count = [day,0,0,0,0]
    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if day == 1 :
                total +=1
            if humain.get_at((x, y)) == GREEN:
                count[1] += 1
            if humain.get_at((x, y)) == BLUE:
                count[2] += 1
            if humain.get_at((x, y)) == BLACK:
                count[3] += 1
            if humain.get_at((x,y)) == RED:
                count[4] += 1
    return count


# Propage de virus
def check_virus(day, screen, humain):
    '''Fonction qui regarde chaque membre de la population test pour lui appliquer différents effets.
    Si la case est rouge (malade), on regarde autour d'elle pour transmettre la maladie.
    Ensuite, on applique les taux de mort et de guérison.
    Si une action a été réalisée, la variable "action" est set à 1.
    Quand la variable action reste à 0, la simulation s'arrete.'''
    global is_dead, is_check, danger, people, gueri, mort, vaccin, lenthx, lenthy, xmax, ymax
    action = 0

    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if humain.get_at((x, y)) == RED and is_check[y//lenthy][x//lenthx]:
                action = 1
                borderx = [x-lenthx,x,x+lenthx,x-lenthx,x+lenthx,x-lenthx,x,x+lenthx]
                bordery = [y-lenthy,y-lenthy,y-lenthy,y,y,y+lenthy,y+lenthy,y+lenthy]

                for i in range(len(borderx)):
                    try :
                        if humain.get_at((borderx[i], bordery[i])) == GREEN and randint(0,100) < danger:
                            is_check[int(bordery[i]//lenthy)][int(borderx[i]//lenthx)] = False
                            pygame.draw.rect(humain, RED, (borderx[i],bordery[i],lenthx,lenthy))
                    except :
                        continue

                this_turn = randint(0,100)

                if this_turn < mort:
                    pygame.draw.rect(humain, BLACK, (x,y,lenthx,lenthy))
                elif mort < this_turn < mort + gueri :
                    pygame.draw.rect(humain, BLUE, (x,y,lenthx,lenthy))
                is_check[y//lenthy][x//lenthx] = False

    screen.blit(humain,(0,0))

    if action == 0:
        is_dead = False
        return


# Fonction principale
def simu_start(day, screen, humain, user_choice):
    '''Fonction principale de la simulation.
    Lance la simulation jusqu'à ce qu'aucun mouvment ne soit possible dans cette dernière.
    Prend une capture d'écran du resultat.
    Lance la fonction affiche_graph du fichier "result.py".
    Ne retourne rien.'''
    global is_dead, danger, people, gueri, mort, vaccin, lenthx, lenthy, xmax, ymax

    tab_check_true(day, screen, humain)
    gen_virus(day, screen, humain)
    text_draw(str(day), (10,10), WHITE, 30, screen)
    pygame.display.update()

    while is_dead:
        tab_check_true(day, screen, humain)
        check_virus(day, screen, humain)

        day += 1
        text_draw(str(day), (10,10), WHITE, 30, screen)
        pygame.display.update()
        day_logs.append(compte(day, screen, humain))

    day_logs.append(compte(day, screen, humain))

    myScreenshot = pyautogui.screenshot()
    screen = randint(0,999999)
    myScreenshot.save(r'screen\simu'+str(screen)+'.png')

    time.sleep(3)
    affiche_result(day_logs, total, screen)


# Initialisation
def main(user_choice):
    '''Fonction qui recupere les parametres fournis pas "user.py" pour les appliquer à la simlaution.
    Le lancement de la simulation se fait à partir d'ici.
    Ne retourne rien.'''
    global people, danger, gueri, mort, vaccin, lenthx, lenthy, xmax, ymax

    # Variables de la maladie
    xmax, people = user_choice[0], user_choice[0]
    danger = user_choice[1]
    gueri = user_choice[2]
    mort = user_choice[3]
    vaccin = user_choice[4]

    #Varibales de la simulation
    ymax = int(people/2)+1
    screen_size = pyautogui.size()
    height = screen_size[1]-(screen_size[1]%ymax-1)
    width = screen_size[0]-(screen_size[0]%xmax-1)
    lenthx = width//xmax
    lenthy = height//ymax

    # Initialisation de Pygame
    screen = pygame.display.set_mode((width,height), FULLSCREEN)
    humain = pygame.Surface((width, height))

    simu_start(day, screen, humain, user_choice)
