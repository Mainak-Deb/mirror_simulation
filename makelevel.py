import pygame,sys
from pygame.locals import *
import math
import copy
import json
from os.path import exists



def make_wall(arr,box):
    wall=[]
    stack=[]
    for i in range(len(arr)-1):
        for j in range(len(arr[0])):
            if(((arr[i][j]==0) and (arr[i+1][j]==1)) or ((arr[i][j]==1) and (arr[i+1][j]==0))):
                nowpos=(j*box,(i+1)*box)
                if(len(stack)>=2):
                    if(stack[-1]==nowpos):
                        stack.pop(-1)
                        stack.append(((j+1)*box,(i+1)*box))
                    else:
                        wall.append(copy.deepcopy(stack))
                        stack.clear()
                        stack.append(nowpos)
                        stack.append(((j+1)*box,(i+1)*box))
                else:
                    stack.append(nowpos)
                    stack.append(((j+1)*box,(i+1)*box))
        if(len(stack)==2):
            wall.append(copy.deepcopy(stack))
            stack.clear()
        
    stack=[]
    for i in range(len(arr)):
        for j in range(len(arr[0])-1):
            if(((arr[i][j]==0) and (arr[i][j+1]==1)) or ((arr[i][j]==1) and (arr[i][j+1]==0))):
                nowpos=((j+1)*box,(i)*box)
                if(len(stack)>=2):
                    if(stack[-1]==nowpos):
                        stack.pop(-1)
                        stack.append(((j+1)*box,(i+1)*box))
                    else:
                        wall.append(copy.deepcopy(stack))
                        stack.clear()
                        stack.append(nowpos)
                        stack.append(((j+1)*box,(i+1)*box))
                else:
                    stack.append(nowpos)
                    stack.append(((j+1)*box,(i+1)*box))
        if(len(stack)==2):
            wall.append(copy.deepcopy(stack))
            stack.clear()

    return wall
            
def savelevel(name,arr,mirrorarray, wallarr,sp,ep):
    level={
        "gamemap":arr,
        "mirrorarr":mirrorarray,
        "wallarr":wallarr,
        "leaser":sp,
        "target":ep
    }
    with open(name, "w") as outfile:
        json.dump(level, outfile)

def makelevel(levvelname):
    levvelname+=".json"
    pygame.init()
    width=1200
    height=690;
    box=30
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption("Line rotate")

    arr=[]
    mirrorarray=[]
    startpoint=(0,0)
    endpoint=(width,height)
    wallarr=[]

    mirroractive=False
    mirror=False
    start=False
    end=False
    normview=False
    

    file_exists = exists("./"+levvelname)


    if(file_exists):
        f = open(levvelname,"r")
        data = json.load(f)
        arr=data["gamemap"]
        mirrorarray=data["mirrorarr"]
        startpoint=data["leaser"]
        endpoint=data["target"]
        wallarr=data["wallarr"]
        f.close()
    else:
        for j in range(0,height,box):
            a=[]
            for i in range(0,width,box):
                a.append(0)
            arr.append(a)
    
    
    running=True
    while running:
        screen.fill((0,0,0))       
        for event in pygame.event.get():
            if event.type == QUIT:
                wallarr=make_wall(arr,box)
                savelevel(levvelname,arr,mirrorarray,wallarr,startpoint,endpoint)
                pygame.quit()
                sys.exit()
                break;
            if event.type == KEYDOWN:
                if event.key == K_m :
                    mirror=True
                if event.key == K_s :
                    start=True
                if event.key == K_e :
                    end=True
                if event.key == K_w :
                    wallarr=make_wall(arr,box)
                if event.key == K_v :
                    normview=True
            if event.type == KEYUP:
                if event.key == K_m :
                    mirror=False
                if event.key == K_s :
                    start=False
                if event.key == K_e :
                    end=False
                if event.key == K_v :
                    normview=False
                if event.key == K_s :
                    wallarr=make_wall(arr,box)
                    savelevel(levvelname,arr,mirrorarray,wallarr,startpoint,endpoint)
        
        mx,my=pygame.mouse.get_pos()
        m,n=(my//box,mx//box)
        #print(m,n)
        mouse_state=pygame.mouse.get_pressed()
        if(mouse_state[0]):
            if(mirror):
                if(not mirroractive):
                    mirroractive=True
                    startpoint=(n*box,m*box)
            elif(start):
                arr[m][n]=2;
            elif(end):
                arr[m][n]=3;
            else:
                arr[m][n]=1;
        elif(mouse_state[2]):
            if(mirror):
                if(mirroractive):
                    mirroractive=False
                    endpoint=(n*box,m*box)
                    mirrorarray.append([startpoint,endpoint])
            else:
                arr[m][n]=0;

        for i in range(len(arr)): 
            for j in range(len(arr[0])):
                if(arr[i][j]==1):
                    pygame.draw.rect(screen,(0,255,0),(j*box,i*box,box,box))
                elif(arr[i][j]==2):
                    pygame.draw.rect(screen,(255,255,0),(j*box,i*box,box,box))
                elif(arr[i][j]==3):
                    pygame.draw.rect(screen,(0,255,255),(j*box,i*box,box,box))
                    
        if( not normview):
            for i in range(0,width,box):
                pygame.draw.line(screen,(255,0,0),(i,0),(i,height),2)
            for j in range(0,height,box):
                pygame.draw.line(screen,(255,0,0),(0,j),(width,j),2)

        for i in mirrorarray:
            pygame.draw.line(screen,(0,0,255),(i[0][0],i[0][1]),(i[1][0],i[1][1]),2)
        for i in wallarr:
            pygame.draw.line(screen,(255,255,255),(i[0][0],i[0][1]),(i[1][0],i[1][1]),2)
        pygame.display.update() 


makelevel("lev1")