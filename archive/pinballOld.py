import math
import pygame

from pygame.locals import *

pygame.init()

#Initialisation jeu
paintballGUI=pygame.display.set_mode((1350,800))


ballMask = pygame.sprite.Sprite()
ballMask.image = pygame.image.load("image/ballT.png").convert_alpha()
ballMask.rect = ballMask .image.get_rect()
ballMask.rect.topleft = 500,400
ballMask.mask = pygame.mask.from_surface(ballMask.image)

backgroundMask = pygame.sprite.Sprite()
backgroundMask.image = pygame.image.load("image/flipper_trsprt.png").convert_alpha()
backgroundMask.rect = backgroundMask.image.get_rect()
backgroundMask.rect.topleft=00,00
backgroundMask.mask=pygame.mask.from_surface(backgroundMask.image)


#variables globales

gameGUI=pygame.display.set_mode((1250,800))
red=(255,0,0)
running=True
gravity=(math.pi,0.001)
drag=0.999
elasticity=1.5

#objet balle : ici nous déclarons tous les paramètres qui définissent la balle de flipper

ball={"x":500,"y":200,"speed":2,"angle":math.pi,}

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

        paintballGUI.blit(backgroundMask.image, backgroundMask.rect)
        paintballGUI.blit(ballMask.image, ballMask.rect)

        ballMask.rect.topleft = ball["x"],ball["y"]
    elif ball["y"]<15:
        ball["y"]=2*15-ball["y"]
        ball["angle"] =math.pi-ball["angle"]
        ball["speed"] *= elasticity

def display(paintballGUI,ballMask,ball):
        paintballGUI.fill((0,0,0))

        pygame.display.flip()



def collison(backgroundMask, ballMask):
    coord=(pygame.sprite.collide_mask(backgroundMask, ballMask))
    if coord!=None:
       # print(coord[1])

        tangent=math.atan2(5,5)
        angle=0.5*math.pi+tangent

        ball["angle"]=2*tangent-ball["angle"]
        ball["speed"]*=elasticity

        ball["x"]+=math.sin(angle)+4
        ball["y"]-=math.cos(angle)+4









inprogress=True
time=pygame.time.Clock()

while inprogress:
    time.tick(60)

    move(ball)
    bounce(ball)
    display(paintballGUI, ballMask, ball)
    collison(backgroundMask, ballMask)
    print(ball["angle"])


    for event in pygame.event.get():
        if event.type==QUIT:
            inprogress=False
        if event.type==MOUSEBUTTONDOWN:
            print(event.pos[0],event.pos[1])

pygame.display.quit()
pygame.quit()