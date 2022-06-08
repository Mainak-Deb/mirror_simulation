from hashlib import new
import math
import pygame
from straightline import straightline,angleline


def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def is_intersect(line1,line2):
    A=line1.point1
    B=line1.point2
    C=line2.point1
    D=line2.point2
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)



def intersect_point(line1,line2):
    A=line1.point1
    B=line1.point2
    C=line2.point1
    D=line2.point2
    a1 = B[1] - A[1]
    b1 = A[0] - B[0]
    c1 = a1*(A[0]) + b1*(A[1])
    a2 = D[1] - C[1]
    b2 = C[0] - D[0]
    c2 = a2*(C[0]) + b2*(C[1])
    determinant = a1*b2 - a2*b1
    if (determinant != 0):
        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant
        return (x, y)
    return (0,0)


def shortest(light,mirrors):
    minpoint=list(light.point2)
    mindist=10**7;
    minline=light
    for i in mirrors:
        p1,p2=intersect_point(light,i)
        dis=math.dist(light.point,[p1,p2])
        if((mindist>dis) and (dis>5)):
            mindist=dis
            minpoint=[p1,p2]
            minline=i
    #print(minpoint)
    minpoint.append(minline)
    return minpoint
def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]


def angle_incident(line1,line2):
    lineA = [line1.point1, line1.point2]
    lineB = [line2.point1,line2.point2]
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    dot_prod = dot(vA, vB)
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    cos_ = dot_prod/magA/magB
    #print(dot_prod/magB/magA)
    angle = math.acos(min(1,max(dot_prod/magB/magA,-1)))
    ang_deg = math.degrees(angle)%360
    
    if ang_deg-180>=0:
        return 360 - ang_deg
    else: 
        
        return ang_deg

def fixang(a):
    if(a<0):return (360+a)
    else:return a%360;

def check(screen,light,mirrors):
    newarr=[]
    for i in mirrors:
        if(is_intersect(light,i.reflector)):
            newarr.append(i.reflector)
    #print(newarr)
    p1,p2,reflector=shortest(light,newarr)
    pygame.draw.line(screen,(255, 233, 36),light.point,(p1,p2),4)
    if(len(newarr)>0):
        inc_ang=angle_incident(light,reflector)
        next_ang=(-1)*(inc_ang+(180-reflector.lineangle))
        next_line=angleline(screen,(p1,p2),next_ang,(255, 233, 36))
        #print(fixang(light.angle),reflector.lineangle,fixang(light.angle-180))
        if((light.angle>0) and (light.angle-180<0)):
           if not( (fixang(light.angle)>=reflector.lineangle) or (reflector.lineangle>=fixang(light.angle-180))):
                #next_line.show()
                check(screen,next_line,mirrors)
        else:
            if not (fixang(light.angle)>=reflector.lineangle>=fixang(light.angle-180)):
                #next_line.show()
                check(screen,next_line,mirrors)



