import time
from random import *
import pygame
from pygame.locals import *
import pyautogui

# Variables de la maladie
people = 200 # max 1920
danger = 10 #Une chance sur
vaccin = 2 #Une chance sur
# Parametres
xmax = people
ymax = int(people/2)+1
screen_size = pyautogui.size()
height, width = screen_size[1]-(screen_size[1]%ymax), screen_size[0]-(screen_size[0]%xmax)
lenthx = width//xmax
lenthy = height//ymax
# Autre
is_dead = True
# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.display.set_caption('CoronaSimu')
screen = pygame.display.set_mode((width,height))
humain = pygame.Surface((width, height))

def gen_virus():
    """Génération des individus normaux, vaccinés et contaminés."""
    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if x == xmax//2 and y == ymax//2 :
                pygame.draw.rect(humain, RED, (x,y,lenthx,lenthy))
            elif randint(0,vaccin) == 0 :
                pygame.draw.rect(humain, BLUE, (x,y,lenthx,lenthy))
            else :
                pygame.draw.rect(humain, GREEN, (x,y,lenthx,lenthy))

    screen.blit(humain,(0,0))
    pygame.display.update()

def check_virus():
    """Détéction des individus contaminés."""
    global is_dead
    green = 0
    for y in range(0, ymax*lenthy, lenthy):
        for x in range(0, xmax*lenthx, lenthx):
            if humain.get_at((x, y)) == GREEN:
                green = 1
                if randint(0,danger) == 0:
                    pygame.draw.rect(humain, RED, (x,y,lenthx,lenthy))
    screen.blit(humain,(0,0))
    pygame.display.update()
                    #time.sleep(0.01)
    if green == 0:
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
                gen_virus()
            if event.key == K_SPACE:
                is_dead = True
                while is_dead:
                    check_virus()
