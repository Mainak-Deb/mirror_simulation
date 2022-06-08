import imp
import pygame,sys
from pygame.locals import *
import math
from Updater import Updater
from straightline import straightline

pygame.init()
width=1200
height=680;
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Line rotate")
update=Updater()

update.add(straightline(screen,(0,200),-70))
update.add(straightline(screen,(400,500),290))



running=True

while running:
    screen.fill((0,0,0))       
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            break;
    
    
    update.update()
    pygame.display.update() 