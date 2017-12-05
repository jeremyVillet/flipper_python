import data
import pygame as pg
import pymunk
from pygame.color import *
from pymunk import Vec2d
import event_pinball as ev

# Nous definissons ici toute les fonctions qui definiront les aspects physique de notre flipper ( création balle , bumber , fliper , prison .. )

# On definit ici les obstacles de la balle
def generateWall(space):
    static_lines = [pymunk.Segment(space.static_body, (data.coor[x][0], data.coor[x][1]), (data.coor[x][2], data.coor[x][3]),1) for x in range(0, len(data.coor))]
    for x in range(0, len(static_lines)):
        static_lines[x].color = pg.color.THECOLORS['black']

    for line in static_lines:
        line.elasticity = 0.8
        line.group = 1
    space.add(static_lines)

#fonction preGenerant les aspects physiques de la balle avant qu'elle ne soit injecté dans le jeu après
def preGenerateBall(x,y,colorBall):
    inertia = pymunk.moment_for_circle(40, 0, 7, (0, 0))
    ball = pymunk.Body(0.1, inertia)
    ball.position = x,y
    ball_object = pymunk.Circle(ball, 6, (0, 0))
    ball_object.collision_type = 7
    ball_object.elasticity = 0.9
    ball_object.color = THECOLORS[colorBall]

    return ball,ball_object

# Fonction générant les six bumpers
def generateBumpers(space):
    # création des bumpers
    for x in range(0, len(data.coordBumper)):
        bumber = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        bumber_object = pymunk.Poly(bumber, data.coordBumper[x])

        bumber_object.friction = 0.5
        bumber_object.elasticity = 1.2
        bumber.position = data.bumperPos[x]
        bumber_object.color = THECOLORS["deeppink"] if x% 2 == 0 else  THECOLORS["deepskyblue"]
        bumber_object.collision_type = x+1
        space.add(bumber_object, bumber)


#On definit ici physiquement les deux flippers
def generateFlipper(space):

    # Construction des deux objetcs flippers
    coorBodyFlippers = [(-5, -10), (0, -5), (-85, -2), (-90, 5), (-85, 12), (-5, 10), (0, 5)]
    mass = 100
    moment = pymunk.moment_for_poly(mass, coorBodyFlippers)

    right_flipper = pymunk.Body(mass, moment)
    right_flipper.position = 729,100
    right_flipper_object = pymunk.Poly(right_flipper, coorBodyFlippers)
    right_flipper_object.color = THECOLORS["deepskyblue"]
    space.add(right_flipper, right_flipper_object)

    left_flipper = pymunk.Body(mass, moment)
    left_flipper.position = 513,101
    left_flipper_object = pymunk.Poly(left_flipper, [(-x, y) for x, y in coorBodyFlippers])
    left_flipper_object.color = THECOLORS["deepskyblue"]
    space.add(left_flipper, left_flipper_object)

    right_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    right_flipper_joint_body.position = right_flipper.position
    left_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    left_flipper_joint_body.position = left_flipper.position

    # Point de rotation des flippers
    joint_right = pymunk.PinJoint(right_flipper, right_flipper_joint_body, (0, 0), (0, 0))
    joint_left = pymunk.PinJoint(left_flipper, left_flipper_joint_body, (0, 0), (0, 0))
    juncture_right = pymunk.DampedRotarySpring(right_flipper, right_flipper_joint_body, 0.15, 15000000, 2000000)
    juncture_left = pymunk.DampedRotarySpring(left_flipper, left_flipper_joint_body, -0.15, 15000000, 2000000)

    space.add(joint_right, juncture_right)
    space.add(joint_left, juncture_left)

    # aspect physique des flippers
    right_flipper_object.elasticity = left_flipper_object.elasticity = 0.5

    return left_flipper,right_flipper

#Fonction effacant  les positions des objet a t-1 afin de refresh la fenetre de jeu

def refreshBalls(window, ball, past_ball):

    # On efface la position des balles a temps - 1
    pg.draw.circle(window, (0, 0, 0), past_ball, 7)

    return (int(ball.position[0]), 700 - int(ball.position[1]))

#Fonction gérant l'affichage des balls et des flippers

def manageDisplayComponents(window,ball_Collection,past_balls):
    # gestion affichage ball
    try:
        past_balls["past_ball"] =refreshBalls(window, ball_Collection["ball"],past_balls["past_ball"])
    except:
        past_balls["past_ball"] = (390, 644)

    # gestion affichage des balls lors de l'event multiball
    try:
        past_balls["past_ball_N2"], past_balls["past_ball_N3"], past_balls["past_ball_N4"] = ev.refreshMultiBalls(window, ball_Collection["ball_N2"], ball_Collection["ball_N3"], ball_Collection["ball_N4"],
            past_balls["past_ball_N2"], past_balls["past_ball_N3"], past_balls["past_ball_N4"])
    except:
        past_balls["past_ball_N2"], past_balls["past_ball_N3"], past_balls["past_ball_N4"] = (390, 644), (390, 644), (390, 644)

    # On refresh l'espace ou se trouve les deux flippers

    window.blit(data.areaFlippers, (487, 488))


#fonction ressort : determine position ressort et definit impulsion de la balle lors du relachement de ce dernier

def ressort(window,img,ressort_position):
    def displayressort(imgNumber):
        pg.draw.rect(window, (0, 0, 0), (878, 554, 31, 117))
        window.blit(imgNumber, (878, 554))
        pg.display.flip()

    displayressort(img[ressort_position-1])

#fonction générant la fermeture de la rampe

def generateClosure(space):
    coorClosure=[(-18,0),(11,0),(-18,2),(11,2)]
    mass = 100
    moment = pymunk.moment_for_poly(mass, coorClosure)
    closure= pymunk.Body(mass, moment)
    closure_object = pymunk.Poly( closure, coorClosure)
    closure_object.friction = 0.5
    closure_object.elasticity = 1.5
    closure.position = (894,568)
    closure_object.color = THECOLORS["black"]
    space.add(closure_object)
    return closure, closure_object

#gestion de la fermeture de la rampe de lancement de la balle
def manageClosure(window,space,ball_objet,manage_closure,closure, closure_object,img,timer):

    if ball_objet!=0:
        if timer==0 and ball_objet.body.position[0] >= 880 and ball_objet.body.position[0] <= 910 and ball_objet.body.position[1] <= 550 and ball_objet.body.position[1] >= 500:
            space.remove(closure)
            manage_closure=-1
            pg.draw.rect(window, (0, 0, 0), (875, 115, 34, 21))
            window.blit(img[1], (875, 115))
            timer=1
        if timer>=1:
            timer+=1
        if timer==60:
            timer=0
            pg.draw.rect(window, (0, 0, 0), (875, 115, 34, 21))
            window.blit(img[0], (875, 115))
    return manage_closure,timer

#fonction renseignant le comportement de la balle si elle est dans le tunnel en fonction de l'entrée empruntée

def ballInTunnel(ball):
    positionBall=[[1,410,450,475,450],[2,528,546,480,455],[3,527,560,611,588]] #position de la balle dans le tunnel
    for x in range(0,3):
        if  ball.body.position[0] >= positionBall[x][1] and ball.body.position[0] <=positionBall[x][2] and ball.body.position[1] <= positionBall[x][3] and ball.body.position[1] >= positionBall[x][4]:
            return positionBall[x][0]
    return 0

#fonction réalisant l'animation du rotor au dessus du tunnel

def rotorAnimation(window,timer,img):
    if timer>= 1 and timer% 2 == 0:
        pg.draw.rect(window, (0, 0, 0), (447, 136, 74, 41))
        window.blit(img[0], (447, 136))
    elif timer>= 1:
        pg.draw.rect(window, (0, 0, 0), (447, 136, 74, 41))
        window.blit(img[1], (447, 136))

#fonction gerant le tunel et l'animation du rotor

def manageTunnel(ball_Collection,ball_object_Collection,ballInTunel,timerRotor,keyBallInTunel):
    if ball_object_Collection["ball_object"]!=0:

        #Gestion du timer gerant l'animation du rotor au dessus du tunnel
        if timerRotor==0 and keyBallInTunel!=0: #La balle passe par le tunnel , on declanche l'animation
            timerRotor=1
        if timerRotor >= 1:
            timerRotor += 1
        if timerRotor == 60:  # temps durant lequel l'animation s'effectue
            timerRotor = 0

    # Gestion du tunnel
    for x,y in zip(ball_object_Collection,ball_Collection):
        if ball_object_Collection[x]!=0:
            keyBallInTunel =ballInTunnel(ball_object_Collection[x])  # Si la balle est dans le tunnel , subit un boost en fonction de la ou elle passe
            ball_Collection[y].apply_impulse_at_local_point(Vec2d(ballInTunel[keyBallInTunel]))

    return timerRotor