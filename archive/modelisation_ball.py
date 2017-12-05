import math
import pygame

from pygame.locals import *

#ici nous allons concevoir la physique de la balle

#variables globales

gameGUI=pygame.display.set_mode((1250,600))
red=(255,0,0)
running=True
gravity=(math.pi,0.002)
drag=0.999
elasticity=0.75

#objet balle

ball={"x":150,"y":50,"speed":4,"angle":math.pi,}


pygame.draw.circle(gameGUI,red,(ball["x"],ball["y"]),15,1)
pygame.display.flip()


#fonction qui associe des vecteurs a la balle

def vectors(angle1,angle2,lenght1,lenght2):
    x=math.sin(angle1)*lenght1+math.sin(angle2)*lenght2
    y=math.cos(angle1)*lenght1+math.cos(angle2)*lenght2
    lenght=math.hypot(x,y)
    angle=0.5*math.pi-math.atan2(y,x)
    return (angle,lenght)

#fonction qui effectue l'animation de la balle

def move(ball):
    (ball["angle"], ball["speed"]) = vectors(ball["angle"], gravity[0], ball["speed"], gravity[1])
    ball["x"]+=math.sin(ball['angle'])*ball['speed']
    ball["y"]-=math.cos(ball['angle'])*ball['speed']
    ball["speed"]*=drag



#fonction rebond

def bounce(ball):

    if ball["x"]>1250-15:
        ball["x"]=2*(1250-15)-ball["x"]
        ball["angle"]=-ball["angle"]
        ball["speed"] *= elasticity

    elif ball["x"]<15:
        ball["x"]=2*15-ball["x"]
        ball["angle"] = -ball["angle"]
        ball["speed"] *= elasticity

    if ball["y"]>600-15:
        ball["y"]=2*(600-15)-ball["y"]
        ball["angle"]=math.pi-ball["angle"]
        ball["speed"] *= elasticity

    elif ball["y"]<15:
        ball["y"]=2*15-ball["y"]
        ball["angle"] =math.pi-ball["angle"]
        ball["speed"] *= elasticity





while running:

    move(ball)
    bounce(ball)
    gameGUI.fill((0,0,0))
    pygame.draw.circle(gameGUI, red, (int(ball["x"]), int(ball["y"])), 15, 1)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            running= False