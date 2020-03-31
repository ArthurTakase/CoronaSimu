import time
from random import *
import pygame
from pygame.locals import *
import pyautogui
from result import *

# Variables de la maladie
people = 400 # nombre de personne par ligne, max 1920
danger = 100 #%
gueri = 20 #%
mort = 0.3 #%
vaccin = 50 #%
#--------------------
xmax = people
ymax = int(people/2)+1
screen_size = pyautogui.size()
height, width = screen_size[1]-(screen_size[1]%ymax-1), screen_size[0]-(screen_size[0]%xmax-1)
lenthx = width//xmax
lenthy = height//ymax
# Autre
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
# Initialisation
pygame.init()
pygame.font.init()
pygame.display.set_caption('CoronaSimu')
screen = pygame.display.set_mode((width,height))
humain = pygame.Surface((width, height))


# Permet d'écire facilement des textes
def text_draw(text, position, color, size):
    myfont = pygame.font.SysFont('Arial', size)
    textsurface = myfont.render(text, True, color)
    screen.blit(textsurface,position)


# tableau pour savoir si une case à été modifiée
def tab_check_true():
    global is_check
    is_check.clear()
    is_check_line = []

    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
                is_check_line.append(True)
        is_check.append(is_check_line)
        is_check_line = []


# Création de la population test
def gen_virus():
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
    tab_check_true()


# Compte chaque jour pour les informations finales
def compte(day):
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
def check_virus():
    global is_dead, is_check
    action = 0

    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if humain.get_at((x, y)) == RED and is_check[y//lenthy][x//lenthx]:#------------------------------------------------------------
                action = 1
                borderx = [x-lenthx,x,x+lenthx,x-lenthx,x+lenthx,x-lenthx,x,x+lenthx]#------------------------------------------------------------
                bordery = [y-lenthy,y-lenthy,y-lenthy,y,y,y+lenthy,y+lenthy,y+lenthy]#------------------------------------------------------------

                for i in range(len(borderx)):
                    try :
                        if humain.get_at((borderx[i], bordery[i])) == GREEN and randint(0,100) < danger:
                            is_check[int(bordery[i]//lenthy)][int(borderx[i]//lenthx)] = False #------------------------------------------------------------
                            pygame.draw.rect(humain, RED, (borderx[i],bordery[i],lenthx,lenthy))
                            #screen.blit(humain,(0,0))
                            #pygame.display.update()
                            #time.sleep(0.1)
                    except :
                        continue

                if randint(0,100) < mort:
                    pygame.draw.rect(humain, BLACK, (x,y,lenthx,lenthy))
                elif randint(0,100) < gueri:
                    pygame.draw.rect(humain, BLUE, (x,y,lenthx,lenthy))
                is_check[y//lenthy][x//lenthx] = False#------------------------------------------------------------

    screen.blit(humain,(0,0))

    if action == 0:
        is_dead = False
        return


# Fonction principale
def simu_start(day):
    global is_dead

    while is_dead:
        tab_check_true()
        check_virus()

        day += 1
        text_draw(str(day), (10,10), WHITE, 30)
        pygame.display.update()
        day_logs.append(compte(day))

    day_logs.append(compte(day))
    affiche_result(day_logs, total)


# First launch
tab_check_true()
gen_virus()
text_draw(str(day), (10,10), WHITE, 30)
pygame.display.update()


# Game loop
while True :
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN :
            if event.key == K_r: #Nouvelle simulation
                day_logs.clear()
                day = 0
                total = 0
                tab_check_true()
                gen_virus()
            if event.key == K_SPACE : #Lance la simulation
                simu_start(day)
