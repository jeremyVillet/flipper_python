import data as d
import pygame as pg
import physical_aspect as physic
from pygame.color import *
from pymunk import Vec2d


# fichier contenant tout les event du flipper : multiball , jail , changement gravité , tilt ..

#Fonction générant les balles lorsque l'event multiball est déclanché
def generateMultiball(space,balls,ball_Collection, ball_object_Collection, ball_spawn_coord):
    for x, y, z in zip(ball_Collection, ball_object_Collection, ball_spawn_coord):
        if x != "ball":  # On ne prend pas en compte le cas de la balle originelle pour ne pas la générer une deuxieme fois
            ball_Collection[x], ball_object_Collection[y] =physic.preGenerateBall(ball_spawn_coord[z][0],ball_spawn_coord[z][1],"deepskyblue")
            space.add(ball_Collection[x], ball_object_Collection[y])
            balls.append(ball_object_Collection[y])


#Fonction effacant  les positions des balls a t-1 afin de refresh la fenetre de jeu lors de l'event multiball
def refreshMultiBalls(window,ball2,ball3,ball4,past_ball2,past_ball3,past_ball4):
    pastBall=[past_ball2,past_ball3,past_ball4]
    for x in pastBall:
        pg.draw.circle(window, (0, 0, 0), x, 7)
    return (int(ball2.position[0]), 700 - int(ball2.position[1])),(int(ball3.position[0]), 700 - int(ball3.position[1])),(int(ball4.position[0]), 700 - int(ball4.position[1]))


# Fonction  Gestion  bumper animation lors de collisions avec balles

def manageBumper(space,imgBumperDisplayed):
        def collision(arbiter, spaceFlipper, data): #fonction callback s executant si une collision survient avec le bumper concerné
            pg.mixer.Sound.play(d.bumper)
            bumperObject = arbiter.shapes[1]
            x=bumperObject.collision_type-1
            if x==4: #correction inversion de deux bumpers
                x=5
            elif x==5:
                x=4
            if imgBumperDisplayed[x]:
                imgBumperDisplayed[x] = False
            else:
                imgBumperDisplayed[x] = True


        for y in range(1, 7):
            collide = space.add_collision_handler(7,y)
            collide.separate= collision

        return imgBumperDisplayed

#fonction event blocage balle dans la prison : detecte si la balle est emprisonnée ou non

def jailBall(ball,to_remove,timerJail):
    if  ball.body.position[0] >= 835 and ball.body.position[0] <= 876 and ball.body.position[1] <= 195 and ball.body.position[1] >= 180 :
        to_remove.append(ball)
        timerJail += 1
        return timerJail
    else:
        return 0

#fonction réalisant l'animation de la prison lorsque la balle rentre dedans

def jailAnimation(window,img,timerJail):
    if timerJail>=1 and timerJail%2==0:
        pg.draw.rect(window, (0, 0, 0), (832, 517, 44, 35))
        window.blit(img[1], (832, 517))
    elif timerJail >= 1:
        pg.draw.rect(window, (0, 0, 0), (832, 517, 44, 35))
        window.blit(img[2], (832, 517))

#fonction gerant l'event de la prison pour chacune des ball ( cas event multiball pris en compte )

def manageJail(space,window,balls,to_remove,ball_Collection, ball_object_Collection, timerJail,score):
    # Si la balle tombe dans la prison , on  supprime la ball concerné temporairement du jeu et on initialise timerJail
    for x, y, z in zip(ball_Collection, ball_object_Collection, timerJail):
        if timerJail[z] == 0:
            if ball_object_Collection[y] != 0:
                timerJail[z] = jailBall(ball_object_Collection[y], to_remove, timerJail[z])

# Lorsque la balle est en prison génere une animation , puis reinjecte la balle dans le jeu au bout d'un certain temps
        if timerJail[z] >= 1:
            timerJail[z] += 1
            score+=500
            pg.mixer.Sound.play(d.jailSound)


        if timerJail[z] == 60:  # temps durant lequel on bloque la balle avant de l'expulser de la prison
            physic.preGenerateBall(850, 185, "deeppink")
            ball_Collection[x].apply_impulse_at_local_point(Vec2d((1, 150)))
            space.add(ball_Collection[x], ball_object_Collection[y])
            balls.append(ball_object_Collection[y])
            timerJail[z] = 0
            pg.draw.rect(window, (0, 0, 0), (832, 517, 44, 35))
            window.blit(d.jails_img[0], (832, 517))


        # animation de la prison
        jailAnimation(window, d.jails_img, timerJail[z])
    return score

#gestion du tilt : On peut devier la balle a gauche ou a droite suelement une fois toute les 180 secondes sinon quoi le tilt se produit ( bloquage des flippers )
def tilt(ball_object_Collection):
    pastBallTilt={}
    i=0
    pg.mixer.Sound.play(d.soundtilt)
    for ball in ball_object_Collection: # Gestion repositionnement ball en cas de sanction tilt
        if ball_object_Collection[ball]!=0:
            pastBallTilt[ball]=(int(ball_object_Collection[ball].body.position[0]),700 - int(ball_object_Collection[ball].body.position[1]))
            ball_object_Collection[ball].body.position = (628, 295+i*20)
            ball_object_Collection[ball].body.velocity = Vec2d(0, 0)
            i+=1

    return False,(0, -900),pastBallTilt

#gestion du timer du tilt et de son affichage

def manageTimerTilt(window,space,timerTilt):
    if timerTilt!=0: #On active le timer si on a exercé un changement de gravité
        timerTilt+=1

    if timerTilt==60: # On retabli la gravité normal apres une seconde
        space.gravity = (0,-900)

    if timerTilt==600 :#On réautorise le changement de gravité au bout de 10 sec
        timerTilt=0

    pg.draw.rect(window, (0, 0, 0), (780, 640, 40, 20))
    timerTiltPrint = d.fontObjBomber.render(str(timerTilt//60), True, (255, 0, 220), (0, 0, 0))
    timerTiltPrintRect = timerTiltPrint.get_rect()
    timerTiltPrintRect.topleft = (780, 640)
    window.blit(timerTiltPrint, timerTiltPrintRect)
    return timerTilt

#gestion affichage repositionnement ball + image sanction title
def  printTilt(window,pastball_Tilt):
    for ball in pastball_Tilt:
        pg.draw.circle(window, (0, 0, 0), pastball_Tilt[ball], 7)

    pg.draw.rect(window, (0, 0, 0), (588, 417, 81, 64))
    window.blit(d.tiltIMG, (580, 377))
    pg.display.flip()

