import pygame
import pymunk
from pygame.locals import *
from pymunk import Vec2d
import pymunk.pygame_util
from pygame.color import *



pygame.init()
maFenetre= pygame.display.set_mode((1250,700))   # fenêtre de dimensions   1250X700

monEspacePhysique=pymunk.Space() # Création de l’objet représentant l’espace physique
monEspacePhysique.gravity=0,-900  #On donne ici un couple de valeur à l’attribut gravity de notre objet monEspacePhysique
draw_options = pymunk.pygame_util.DrawOptions(maFenetre)

jeuEnCours=True #Tant que ce booléen est à True , on reste dans la boucle de jeu




while jeuEnCours :

    monSegment = pymunk.Segment(monEspacePhysique.static_body, (250, 150), (650, 150), 1.5)
    monSegment.elasticity = 1
    monSegment.color = pygame.color.THECOLORS['whitesmoke']
    monEspacePhysique.add(monSegment)

    bumber = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    bumber_object = pymunk.Poly(bumber,[(40,40),(-40,40),(-40,-40),(40,-40)])

    bumber_object.friction = 0.5
    bumber_object.elasticity = 1.2
    bumber.position = (400,400)
    bumber_object.color = THECOLORS["deeppink"]
    bumber_object.collision_type = 1
    monEspacePhysique.add(bumber_object, bumber)

    for event in pygame.event.get():
        if event.type == QUIT :    # Si l’utilisateur clique sur la croix rouge
            jeuEnCours=False

        if  event.type == KEYDOWN and event.key == K_b:
            inertia = pymunk.moment_for_circle(40, 10, 15, (0, 0))
            ball = pymunk.Body(0.1, inertia)
            ball.position = 500,500
            ball_object = pymunk.Circle(ball, 15, (0, 0))
            ball_object.elasticity = 0.9
            ball_object.color = THECOLORS['blueviolet']
            monEspacePhysique.add(ball,ball_object)


# mise à jour des aspects physiques et de l’affichage des objets Pymunk
    dt = 1.0 / 60.0 / 5.
    for x in range(5):
        monEspacePhysique.step(dt)
    maFenetre.fill(0)
    monEspacePhysique.debug_draw(draw_options)

    # mise à jour de l’affichage des éléments Pygame
    pygame.display.flip()
    pygame.time.Clock().tick(60)
