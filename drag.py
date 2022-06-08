import math
from re import M
import pygame,sys
from pygame.locals import *

from straightline import straightline,angleline


class Drag:
    def __init__(self,screen,center,size) -> None:
        self.screen=screen;
        self.center=list(center)
        self.arm=size
        self.calculate_pos()
        self.setState()
        self.bg=pygame.image.load('mirror.png')
        self.bg=pygame.transform.scale(self.bg,(self.arm,self.arm))
        self.rightClick=False
        self.dorotate=False
        self.rotate=90;
        self.prevang=90
    def __str__ (self):
        return 'Drag->({},{})'.format(self.center[0],self.center[1])

    def render_image(self,image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle-90)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
        self.screen.blit(rotated_image, new_rect)
            
    def calculate_pos(self):
        self.pos1=[self.center[0]-self.arm//2,self.center[1]-self.arm//2]
        self.pos2=[self.center[0]+self.arm//2,self.center[1]+self.arm//2]

    def setState(self):
        mouse_state=pygame.mouse.get_pressed()
        if(self.is_over(self.arm//2)):
            if(not mouse_state[0]):
                self.rightClick=False
            if(mouse_state[0]):
                if(not self.rightClick):
                    mx,my=pygame.mouse.get_pos()
                    self.offx=mx-self.center[0]
                    self.offy=my-self.center[1]
                    self.rightClick=True
                
                self.rightClick=True

    def is_over(self,radius):
        mx,my=pygame.mouse.get_pos()
        angle=math.atan2((my-self.center[1]),(mx-self.center[0]))
        px,py=(abs(radius*math.cos(angle)),abs(radius*math.sin(angle)))
        #print(self.center[0]-px,self.center[0]+px,angle)
        if( (self.center[0]-px<mx<self.center[0]+px) and 
            (self.center[1]-py<my<self.center[1]+py)):
            return True
        return False

    def line(self):
        sx=self.center[0]+(self.arm//2*math.cos((self.rotate)*math.pi/180))
        sy=self.center[1]-(self.arm//2*math.sin((self.rotate)*math.pi/180))
        ex=self.center[0]-(self.arm//2*math.cos((self.rotate)*math.pi/180))
        ey=self.center[1]+(self.arm//2*math.sin((self.rotate)*math.pi/180))
        return straightline(self.screen,(sx,sy),(ex,ey))
        


    def is_drag(self):
        mouse_state=pygame.mouse.get_pressed()
        if(mouse_state[0] and self.is_over(self.arm//4)):
            return True
        return False
    
    def is_rotate(self):
        ov1=self.is_over(self.arm//4)
        ov2=self.is_over(self.arm//2)
        if(ov1):
            return False
        elif(not ov1 and ov2):
            return True
        else:
            return False
 

    def show(self):
        # if(self.is_drag()):
        #     pygame.draw.rect(self.screen,(255, 170, 0),(self.pos1[0],self.pos1[1],self.arm,self.arm))    
        # else:
        #     pygame.draw.rect(self.screen,(255, 255, 100),(self.pos1[0],self.pos1[1],self.arm,self.arm))
        ov1=self.is_over(self.arm//4)
        ov2=self.is_over(self.arm//2)
        if(ov1):
            color1=(51, 255, 235)
            color2=(244, 255, 255)
        elif(not ov1 and ov2):
            color1=(244, 255, 255)
            color2=(244, 255, 28)
        else:
            color1=(244, 255, 255)
            color2=(244, 255, 255)

        
        
        self.render_image(self.bg,tuple(self.pos1),self.rotate)
        pygame.draw.circle(self.screen,color2,tuple(self.center),(self.arm//2),3)
        pygame.draw.circle(self.screen,color1,tuple(self.center),(self.arm//4),1)
        #self.reflector.show()
        

    def update(self):
        if(self.is_drag()):
            mx,my=pygame.mouse.get_pos()
            self.center=(mx-self.offx,my-self.offy)
            self.calculate_pos()
            print("working")
            

        # if(self.is_rotate()):
        #     mx,my=pygame.mouse.get_pos()
        #     mouse_state=pygame.mouse.get_pressed()
        #     #print(mouse_state)
        #     if(mouse_state[0]):
        #         self.rotate+=0.1;  
        #     elif(mouse_state[2]):
        #         self.rotate-=0.1; 

        if(self.is_rotate()):
            mx,my=pygame.mouse.get_pos()
            mouse_state=pygame.mouse.get_pressed()
            if(mouse_state[0]):
                ang=(-1)*math.atan2(self.center[1]-my,self.center[0]-mx)*180/math.pi
                if(not self.dorotate):
                    self.prevang=ang
                    self.dorotate=True
                else:
                    self.rotate+=(ang-self.prevang);
                    self.prevang=ang
            else:
                self.dorotate=False
        
                
            # elif(mouse_state[2]):
            #     self.rotate-=0.1; 
        self.reflector=self.line()
        
