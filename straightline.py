from re import S
from turtle import Screen
import pygame,sys
from pygame.locals import *
import math




class straightline:
    def __init__(self,screen,point1,point2,color=(255,0,0)) -> None:
        self.point1=point1
        self.point2=point2
        self.screen=screen;
        self.color=color;
        self.lineangle=(180-(math.atan2(point2[1]-point1[1],point2[0]-point1[0])*180/math.pi))

    def show(self):
        pygame.draw.line(self.screen,self.color,self.point1,self.point2,4)
        

class angleline(straightline):
    def __init__(self, screen, point,angle, color=(255, 0, 0),length=4000) -> None:
        self.angle=angle
        self.point=point
        self.length=length
        self.screen=Screen
        self.color=color
        sx,sy=point
        ex=int(sx+(length*math.cos(angle*math.pi/180)))
        ey=int(sy-(length*math.sin(angle*math.pi/180)))
        super().__init__(screen, point, (ex,ey), color)
    
    def updateAngle(self,state):
        if(state=="incr"):
            self.angle+=1;
        elif(state=="decr"):
            self.angle-=1;
        angle=self.angle
        sx,sy=self.point
        length=self.length
        ex=int(sx+(length*math.cos(angle*math.pi/180)))
        ey=int(sy-(length*math.sin(angle*math.pi/180)))
        super().__init__(self.screen, (int(sx),int(sy)), (int(ex),int(ey)), self.color)
    
        

