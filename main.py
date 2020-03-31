import time
from random import *
import pygame
from pygame.locals import *
import pyautogui
from result import *

# Variables de la maladie
people = 200 # max 1920
danger = 2 #Une chance sur
gueri = 10  #Une chance sur
mort = 10 #Une chance sur
vaccin = 2 #Une chance sur
#--------------------
xmax = people
ymax = int(people/2)+1
screen_size = pyautogui.size()
height, width = screen_size[1]-(screen_size[1]%ymax), screen_size[0]-(screen_size[0]%xmax)
lenthx = width//xmax
lenthy = height//ymax
# Autre
day = 1
day_logs = []
total = 0
# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.font.init()
pygame.display.set_caption('CoronaSimu')
screen = pygame.display.set_mode((width,height))
humain = pygame.Surface((width, height))

def text_draw(text, position, color, size):
    myfont = pygame.font.SysFont('Arial', size)
    textsurface = myfont.render(text, True, color)
    screen.blit(textsurface,position)

def gen_virus():
    """Génération des individus normaux, vaccinés et contaminés."""
    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if x == (xmax//2) * lenthx and y == (ymax//2) * lenthy:
                pygame.draw.rect(humain, RED, (x,y,lenthx,lenthy))
            elif randint(1,vaccin) == 1 :
                pygame.draw.rect(humain, BLUE, (x,y,lenthx,lenthy))
            else :
                pygame.draw.rect(humain, GREEN, (x,y,lenthx,lenthy))

    screen.blit(humain,(0,0))
    pygame.display.update()

def check_border(x,y):
    borderx = [x-lenthx,x,x+lenthx,x-lenthx,x+lenthx,x-lenthx,x,x+lenthx]
    bordery = [y-lenthy,y-lenthy,y-lenthy,y,y,y+lenthy,y+lenthy,y+lenthy]

    for i in range(len(borderx)):
        try:
            if humain.get_at((borderx[i], bordery[i])) == RED:
                return True
        except:
            continue

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

def check_virus():
    """Détection des individus contaminés."""
    global is_dead
    action = 0
    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if humain.get_at((x, y)) == GREEN:
                #action = 1
                if check_border(x,y):
                    if randint(1,danger) == 1:
                        pygame.draw.rect(humain, RED, (x,y,lenthx,lenthy))

                        #time.sleep(0.01)
            elif humain.get_at((x, y)) == RED:
                action = 1
                if randint(1,mort) == 1:
                    pygame.draw.rect(humain, BLACK, (x,y,lenthx,lenthy))
                elif randint(1,gueri) == 2:
                    pygame.draw.rect(humain, BLUE, (x,y,lenthx,lenthy))

    if action == 0:
        is_dead = False
        return

gen_virus()
while True :
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN :
            if event.key == K_r: #Nouvelle simu
                day_logs.clear()
                day = 1
                total = 0
                gen_virus()
            if event.key == K_SPACE:
                is_dead = True
                while is_dead:
                    check_virus()
                    screen.blit(humain,(0,0))
                    text_draw(str(day), (10,10), WHITE, 30)
                    day_logs.append(compte(day))
                    pygame.display.update()
                    day += 1
                day_logs.append(compte(day))
                affiche_result(day_logs, total)
