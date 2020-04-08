import time
from random import *
import pygame
from pygame.locals import *
import pyautogui
from result import *
import os

# Variables globales
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
# Tkinter
pygame.init()
pygame.font.init()
pygame.display.set_caption('CoronaSimu')

# Permet d'écire facilement des textes
def text_draw(text, position, color, size, day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen):
    myfont = pygame.font.SysFont('Arial', size)
    textsurface = myfont.render(text, True, color)
    screen.blit(textsurface,position)


# tableau pour savoir si une case à été modifiée
def tab_check_true(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen):
    global is_check
    is_check.clear()
    is_check_line = []

    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
                is_check_line.append(True)
        is_check.append(is_check_line)
        is_check_line = []


# Création de la population test
def gen_virus(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen):
    global is_check
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
    tab_check_true(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)


# Compte chaque jour pour les informations finales
def compte(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen):
    global total
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
def check_virus(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen):
    global is_dead, is_check
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
def simu_start(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen):
    global is_dead

    tab_check_true(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)
    gen_virus(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)
    text_draw(str(day), (10,10), WHITE, 30, day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)
    pygame.display.update()

    while is_dead:
        tab_check_true(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)
        check_virus(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)

        day += 1
        text_draw(str(day), (10,10), WHITE, 30, day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)
        pygame.display.update()
        day_logs.append(compte(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen))

    day_logs.append(compte(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen))

    myScreenshot = pyautogui.screenshot()
    screen = randint(0,999999)
    myScreenshot.save(r'screen\simu'+str(screen)+'.png')

    time.sleep(3)
    print(day_logs)
    affiche_result(day_logs, total, screen)


# Game loop
def main(user_choice):
    # Variables de la maladie
    xmax, people = user_choice[0], user_choice[0]
    danger = user_choice[1]
    gueri = user_choice[2]
    mort = user_choice[3]
    vaccin = user_choice[4]
    #Varibales de la simulation
    ymax = int(people/2)+1
    screen_size = pyautogui.size()
    height, width = screen_size[1]-(screen_size[1]%ymax-1), screen_size[0]-(screen_size[0]%xmax-1)
    lenthx = width//xmax
    lenthy = height//ymax
    # Initialisation de Pygame
    screen = pygame.display.set_mode((width,height), FULLSCREEN)
    humain = pygame.Surface((width, height))

    simu_start(day, xmax, ymax, lenthx, lenthy, danger, gueri, mort, vaccin, humain, screen)
