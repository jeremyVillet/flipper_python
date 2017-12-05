import pygame as pg
from pygame.locals import *
from pymunk import Vec2d
import pymunk.pygame_util
import data
import physical_aspect as physic
import event_pinball as ev
import  score_management as score

#Initialisation de base du jeu
pg.init()
windowFlipper = pg.display.set_mode((1250,700))
backgroundFlipper = pg.image.load("image/flipper_trsprt.png").convert_alpha()
pg.display.set_caption("NIGHT MISSION PINBALL EDITION 2017")
clock = pg.time.Clock()

#lancememnt musique d'ambiance
pg.mixer.music.load("music/main1.mp3")
pg.mixer.music.queue("music/main1.mp3")
pg.mixer.music.play()


#varibales globales controlant l'etat du jeu

gamePaused=False #permet de mettre le jeu en pause ou non

ballCreated,multiBallActivated=False,False #Controle de la balle principale et des balls de l'event multiball

#Données propre a chacune des balles pouvant être présente simultanement dans le flipper

ball_Collection={"ball":0,"ball_N2":0,"ball_N3":0,"ball_N4":0} #Contient données relatives a l'affichage de la balle si cette derniere est crée
ball_object_Collection={"ball_object":0,"ball_object_N2":0,"ball_object_N3":0,"ball_object_N4":0} #Contient données relatives a l'aspect physique de la balle si cette dernière est créé
ball_spawn_coord={"ball":[892,161],"ball_N2":[827, 221],"ball_N3":[552, 672],"ball_N4":[478, 658]} #Définition du point d'appartion de chacune des balles dans le flipper
past_balls={"past_ball":(390, 644),"past_ball_N2":(390, 644),"past_ball_N3":(390, 644),"past_ball_N4":(390, 644) } #Coordonnées des balls a t-1 permettant d'effacer leur anciennes positions


ressort_position=1 #determine position du ressort
impulse={1:50,2:95,3:110,4:120,5:130}  #Contient la puissance de l'impulsion donnée a la balle lorsque le ressort est relaché. Depend de la position du ressort

manage_closure=1 # determine si la rampe de lancement de la balle doit être ouvert ou non

num_Bumper=["bumper1","bumper2","bumper3","bumper4","bumper5","bumper6"]


timerJail={"ball":0,"ball_N2":0,"ball_N3":0,"ball_N4":0} #Gestion du temps d'emprisonnement pour chacune des balles dans le cadre de l'event jail


keyBallInTunel=0 #Determine si un ball est dans le tunelle ou non et a quelle position du tunelle la balle se trouve
ballInTunel={0:(0,0),1:(90,1),2:(1,190),3:(20,90)} #Contient la puissance de l'impulsion et son orientation donnée a la balle en fonction de sa position dans le tunelle

imgBumperDisplayed={0:True,1:True,2:True,3:True,4:True,5:True} #On conait ainsi quelle est la couleur des bumpers affichés


balls = [] # les balles présentent dans le jeu sont inscritent dans cette liste

scorePlayer=[0,0,0,0] #Contient le score de chacun des joueurs
numberBallPlayer=[0,0,0,0] #Contient le nombre de balles restant pour chacun des joueurs
round=1 #indique quel joueur joue

insert,numberOfCredit=0,0 #Determine si l'event ajouter une piece est actif ou non / Represente le nombre de credits inserés
gameHasBegun,gameOver=False,False # Determine si la partie à commencé ou non / Determine si les joueurs ont perdu ou non

#Dictionnaire gérant tous les timer de la plupart des events du jeu
timer={"timerClosure":0,"timerRotor":0,"timerTitleCredit":0,"timerTitleBall":0,"timerAnimation":0,"timerRolloverNight":0,"timerRolloverDrop":0,"timerTilt":0}

#variables liés au rollover et bombers

rolloverNightActivate = {"N": False, "I": False, "G": False, "H": False, "T": False} #Determine si un rollover est activé ou non pour NIGHT
rolloverNightPosition={"N":(637,105),"I":(680,100),"G":(710,97),"H":(750,100),"T":(790,105)} #Determine la position des rollover pour NIGHT
hitboxRolloverNight=[["N",631,659,557,601],["I",669,697,560,612],["G",705,734,563,614],["H",742,771,561,613],["T",780,808,557,607]] #Coordonées permettant de generer une hitbox pour savoir si une balle est passée dessus ou non
numberRolloverNightMatches = 0 #Nombre de rollover NIGHT activé


rolloverDropActivate = {"D": False, "R": False, "O": False, "P": False} #Determine si un rollover est activé ou non pour DROP
rolloverDropPosition={"D":(374,444),"R":(399,444),"O":(421,444),"P":(447,444)} #Determine la position des rollover pour NDROP
hitboxRolloverDrop=[["D",366,386,234,264],["R",392,411,234,264],["O",415,435,234,264],["P",441,466,234,264]] #Coordonées permettant de generer une hitbox pour savoir si une balle est passée dessus ou non
numberRolloverDropMatches = 0 #Nombre de rollover DROP activé

bomberActivate={"A": True, "Q": True, "C": True, "D": True, "F": True, "L": True, "Y": True} #Determine si un bomber a été detruit par une balle ou pas encore

useFlippers=True # determine si les flippers sont bloqués ou non => utilisé dans le cadre de la punition tilt

running,inMenu=True,True #Determine si on est dans la boucle du jeu / Detremine si on est dans la sous boucle menu ou dans la sous boucle du flipper
numberBackground=0 # Determine qu'elle partie du menu est affiché à l'écran

while running:
    #Sous boucle menu
    while inMenu:
        windowFlipper.blit(data.menuIMG[numberBackground], (0, 0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:  # On quitte le jeu
                exit()

            if numberBackground!=3 and event.type == MOUSEBUTTONDOWN and event.button == 1:
                numberBackground+=1

            if numberBackground ==3 and event.type == MOUSEBUTTONDOWN and event.button == 1:
                hitboxNumberPlayer=[[1,238,429,227,287],[2,728,955,228,287],[3,230,455,399,453],[4,727,957,385,439]]
                for i in range(0,4):
                    if  event.pos[0]>=hitboxNumberPlayer[i][1] and event.pos[0]<=hitboxNumberPlayer[i][2] and event.pos[1]>=hitboxNumberPlayer[i][3] and event.pos[1]<=hitboxNumberPlayer[i][4]:
                        numberPlayer=hitboxNumberPlayer[i][0]
                        pg.draw.rect(windowFlipper, (0, 0, 0), (0, 0, 1250, 699))
                        inMenu=False
                        generateGame=True #Permet de generer une seule fois le jeu une fois sortie du menu


    if generateGame: #Apres etre sortie du menu nous avons besoin de generer le jeu une fois

        # Création d'un espace physique dans la fenetre de jeu
        spaceFlipper = pymunk.Space()
        spaceFlipper.gravity = (0, -900)
        draw_options = pymunk.pygame_util.DrawOptions(windowFlipper)

        # Generation de la hitbox des murs delimitant les decors de l'espace de progression de la balle
        physic.generateWall(spaceFlipper)

        # Generation des bumpers
        physic.generateBumpers(spaceFlipper)

        # Generation des deux flippers
        left_flipper, right_flipper = physic.generateFlipper(spaceFlipper)

        # Generation de la fermeture de la rampe
        closure, closure_object = physic.generateClosure(spaceFlipper)

        #Génération des décors
        windowFlipper.blit(backgroundFlipper, (0, 0))
        windowFlipper.blit(data.jail1, (832, 517))
        windowFlipper.blit(data.rotor1, (447, 136))
        windowFlipper.blit(data.closure1, (875, 115))


        generateGame=False

#Cycle du jeu une fois ce dernier généré
    #Interaction du joueur avec le jeu
    for event in pg.event.get():
        # Controle du flipper droit
        if useFlippers and event.type == KEYDOWN and event.key == K_c:
            right_flipper.apply_impulse_at_local_point(Vec2d.unit() * 45000, (-75, 0))
            pg.mixer.Sound.play(data.flip_right)

        # Controle du flipper gauche
        if useFlippers and event.type == KEYDOWN and event.key == K_x:
            left_flipper.apply_impulse_at_local_point(Vec2d.unit() * -45000, (-75, 0))
            pg.mixer.Sound.play(data.flip_right)

        # Réglage de la puissance du ressort
        if event.type == KEYDOWN and event.key == K_r and ballCreated==False :
            if numberBallPlayer[round-1]>0:
                ressort_position= ressort_position + 1
                if ressort_position>5:
                    ressort_position=1
                pg.mixer.Sound.play(data.reload)

        #Créer la balle et relacher le ressort pour la lancer
        if event.type == KEYDOWN and event.key == K_SPACE and ballCreated==False and ressort_position!=1:
            ball_Collection["ball"],ball_object_Collection["ball_object"]=physic.preGenerateBall(ball_spawn_coord["ball"][0], ball_spawn_coord["ball"][1],"deeppink")
            spaceFlipper.add(ball_Collection["ball"], ball_object_Collection["ball_object"])
            balls.append(ball_object_Collection["ball_object"])
            ball_Collection["ball"].apply_impulse_at_local_point(Vec2d((1, impulse[ressort_position])))
            ressort_position=1
            numberBallPlayer[round - 1]-=1
            ballCreated=True
            timer["timerRolloverNight"],timer["timerRolloverDrop"]= 0,0
            pg.mixer.Sound.play(data.ressortSound)

        # Inserer un pièce pour des crédits suplémentaire uniquement avant que la partie soit lancé ( avant l'achat d'une balle )
        if gameHasBegun==False and event.type == KEYDOWN and event.key == K_p:
            insert = 1
            pg.mixer.Sound.play(data.coinSound)

        #Consomme un credit pour donner 3 balles à chacun des joueurs
        if event.type == KEYDOWN and event.key == K_o:
            gameHasBegun=True # A partir de ce moment la partie est considerer comme commencée , on ne peut plus acheter de credit ou modifier le nombre de joueur
            if numberOfCredit>0:
                for x in range(0,numberPlayer):
                    numberBallPlayer[x]+=3
                numberOfCredit-=1


    #Simulation coup dans le flipper pour interferer avec la balle via changement de gravité /punition tilt

        # On declanche la punition tilt si le timer n'est pas réspecté
        if ballCreated and timer["timerTilt"] != 0 and event.type == KEYDOWN and event.key == K_b :
            useFlippers,spaceFlipper.gravity,pastBall_Tilt=ev.tilt(ball_object_Collection)

        # champs gravitationel vers la droite
        if ballCreated and timer["timerTilt"]==0 and event.type == KEYDOWN and event.key == K_b:
            spaceFlipper.gravity = (-900, 0)
            timer["timerTilt"]=1

        # On declanche la punition tilt si le timer n'est pas réspecté
        if ballCreated and timer["timerTilt"] != 0 and event.type == KEYDOWN and event.key == K_n:
            useFlippers, spaceFlipper.gravity, pastBall_Tilt = ev.tilt( ball_object_Collection)

        # champs gravitationel vers la gauche
        if ballCreated and timer["timerTilt"] == 0 and event.type == KEYDOWN and event.key == K_n:
            spaceFlipper.gravity = (900, 0)
            timer["timerTilt"]=1

        # On quitte le jeu
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False

        # Gestion de la fonctionnalité pause
        if event.type == KEYDOWN and event.key == K_j:
            gamePaused=True
            windowFlipper.blit(data.pauseIMG, (510, 397))
            pg.display.flip()

        # Sous boucle jeu en pause
        if gamePaused:
            while gamePaused:
                for event in pg.event.get():
                    #Redemmarer le jeu
                    if event.type == KEYDOWN and event.key == K_j:
                        pg.draw.rect(windowFlipper,(0,0,0),(510,397,219,114))
                        gamePaused = False

                    #Quitter le jeu durant la pause
                    if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                        running,gamePaused = False,False
                        pg.draw.rect(windowFlipper, (0, 0, 0), (510, 397, 219, 114))

        #Si game over , posibiliter de quitter le jeu ou de relancer la partie
        if gameOver and event.type == MOUSEBUTTONDOWN and event.button == 1:

            # On relance une partie , reinitialisation etat du jeu
            if event.pos[0]>=540 and event.pos[0]<=626 and event.pos[1]>=576 and event.pos[1]<=591:
                numberBackground=0
                inMenu,gameOver,gameHasBegun,round =True,False,False,1
                scorePlayer ,numberBallPlayer= [0, 0, 0, 0],[0, 0, 0, 0]

            # On quitte le jeu
            if event.pos[0] >= 655 and event.pos[0] <= 697 and event.pos[1] >= 576 and event.pos[1] <= 593:
                running=False

        # Declancher l'event multiball de façon manuelle pour le tester sans passer par l'event rollover NIGHT ( un seul multiball déclanchable a la fois )
        if multiBallActivated==False and event.type == KEYDOWN and event.key == K_t:
            ev.generateMultiball(spaceFlipper,balls,ball_Collection, ball_object_Collection, ball_spawn_coord)
            multiBallActivated=True

    #gestion du ressort
    physic.ressort(windowFlipper, data.ressorts_img, ressort_position)

    #gestion de la fermeture de la rampe de lancement de la balle
    manage_closure,timer["timerClosure"]=physic.manageClosure(windowFlipper,spaceFlipper,ball_object_Collection["ball_object"],manage_closure, closure_object,closure,data.closures_img,timer["timerClosure"])
    if timer["timerClosure"]==59:
        closure, closure_object = physic.generateClosure(spaceFlipper)


    #gestion affichage des balls et des deux flippers
    physic.manageDisplayComponents(windowFlipper, ball_Collection, past_balls)

    # gestion du rollover NIGHT
    if timer["timerRolloverNight"]==0:
        rolloverNightActivate,numberRolloverNightMatches=score.rollover(windowFlipper, ball_object_Collection,rolloverNightActivate, rolloverNightPosition,hitboxRolloverNight,data.fontObjRolloverNight)

    timer["timerRolloverNight"] = score.validatedRollover(numberRolloverNightMatches, timer["timerRolloverNight"], windowFlipper,rolloverNightPosition,ballCreated,data.fontObjRolloverNight)
    if timer["timerRolloverNight"]==200:
        timer["timerRolloverNight"]=0
        rolloverNightActivate = {"N": False, "I": False, "G": False, "H": False, "T": False}

    # gestion du rollover DROP

    if timer["timerRolloverDrop"]== 0:
        rolloverDropActivate, numberRolloverDropMatches = score.rollover(windowFlipper, ball_object_Collection,rolloverDropActivate, rolloverDropPosition,hitboxRolloverDrop,data.fontObjRolloverDrop)

    timer["timerRolloverDrop"] = score.validatedRollover(numberRolloverDropMatches, timer["timerRolloverDrop"], windowFlipper,rolloverDropPosition, ballCreated,data.fontObjRolloverDrop)
    if timer["timerRolloverDrop"] == 200:
        timer["timerRolloverDrop"] = 0
        rolloverDropActivate = {"D": False, "R": False, "O": False, "P": False}

    #gestion multiball => declancher si tous les rollovers Night on été activé
    x=0
    for rollover in rolloverNightActivate:
        if rolloverNightActivate[rollover]:
            x +=1

    if x==5 and multiBallActivated==False:
        ev.generateMultiball(spaceFlipper, balls, ball_Collection, ball_object_Collection, ball_spawn_coord)
        multiBallActivated = True
        score[round-1]=+5000

    #Si drop activé , le joueur actuel gagne deux balls
    x = 0
    for rollover in rolloverDropActivate:
        if rolloverDropActivate[rollover]:
            x +=1
    if x ==4 :
        numberBallPlayer[round-1] += 2
        score[round - 1] = +5000

    #gestion des bombers
    bomberActivate,scorePlayer[round-1]=score.bombers(windowFlipper,bomberActivate,ball_object_Collection,scorePlayer[round-1],data.bombers_img)

    #gestion du tilt et de son timer
    timer["timerTilt"]=ev. manageTimerTilt(windowFlipper,spaceFlipper,timer["timerTilt"])

    # actualisation decor
    if useFlippers==True:
        windowFlipper.blit(data.helico, (588, 417))

    #actualisation des formes pymunk
    if gameOver==False:
        spaceFlipper.debug_draw(draw_options)

    #On ajoute les balles sortant du jeu a la liste to remove en attendant qu'elles soient effacées du moteur physique
    to_remove = []
    for ball_Inprogress in balls:
        # la balle tombe hors jeu , on la supprime du jeu
        if int(ball_Inprogress.body.position[1]) <= 40:
            to_remove.append(ball_Inprogress)

    #gestion de la partie en fonction de la balle principale et des eventuels balles du multiball
    for ballObject in ball_object_Collection:
        if ball_object_Collection[ballObject]!=0:
            keyBallInTunel = physic.ballInTunnel(ball_object_Collection[ballObject])
            if int( ball_object_Collection[ballObject].body.position[1]) <= 40:
                ball_object_Collection[ballObject]=0
                pg.mixer.Sound.play(data.lose)

    #Si l'event muliball est terminé on réautorise son apparition
    if ball_object_Collection["ball_object_N2"]==0 and ball_object_Collection["ball_object_N3"]==0 and ball_object_Collection["ball_object_N4"]==0 :
        multiBallActivated=False
        #Le joueur a fini son tour , on reinitalise l'etat du jeu
        if ballCreated==True and ball_object_Collection["ball_object"]==0 and ball_object_Collection["ball_object_N2"]==0 and ball_object_Collection["ball_object_N3"]==0 and ball_object_Collection["ball_object_N4"]==0:
            rolloverNightActivate = {"N": False, "I": False, "G": False, "H": False, "T": False}
            rolloverDropActivate = {"D": False, "R": False, "O": False, "P": False}
            bomberActivate = {"A": True, "Q": True, "C": True, "D": True, "F": True, "L": True, "Y": True}
            useFlippers,ballCreated,multiBallActivated,timer["timerTilt"]=True,False,False,0
            pg.draw.rect(windowFlipper, (0, 0, 0), (580, 377, 100, 100))
            round+=1
            if round >numberPlayer:
                round=1

    #gestion du tunnel
    timer["timerRotor"]=physic.manageTunnel(ball_Collection, ball_object_Collection, ballInTunel,  timer["timerRotor"], keyBallInTunel)

    #Animation du rotor
    physic.rotorAnimation(windowFlipper, timer["timerRotor"],data.rotors_img)

   #Gestion de la prison
    scorePlayer[round - 1]=ev.manageJail(spaceFlipper, windowFlipper, balls, to_remove, ball_Collection, ball_object_Collection, timerJail,scorePlayer[round-1])

    #Detection collision ball / Bumber pour animation bumper
    imgBumperDisplayed=ev.manageBumper(spaceFlipper,imgBumperDisplayed)

    #Gestion affichage ball en cas sanction tilt
    if useFlippers==False:
        ev.printTilt(windowFlipper,pastBall_Tilt)

    #Gestion du gameOver
    gameOver=score.manageGameOver(windowFlipper, numberPlayer, numberBallPlayer,numberOfCredit, gameHasBegun,ballCreated,gameOver)

    #On supprime du moteur physique les balles se trouvant dans to_remove
    for ball_Inprogress in to_remove:
        spaceFlipper.remove(ball_Inprogress.body, ball_Inprogress)
        balls.remove(ball_Inprogress)

    # mise a jour des aspects physiques
    dt = 1.0 / 60.0 / 5.
    for x in range(5):
        spaceFlipper.step(dt)

    #gestion score bumpers
    scorePlayer[round-1],imgBumperDisplayed=score.manageScoreBumper(windowFlipper,ball_object_Collection,scorePlayer[round-1],imgBumperDisplayed)

    #affichage du score
    timer["timerAnimation"]=score.displayScore(windowFlipper,scorePlayer,numberPlayer,numberBallPlayer,round-1,timer["timerAnimation"])

    #affichage insert coins + gestion des credits
    if insert>0:
        insert,numberOfCredit = score.insertCoins(windowFlipper, insert,numberOfCredit)

    #gestion affichage nombre de credit
    score.displayCredit(windowFlipper,numberOfCredit)

    # Animation titre credit et ball si il y en a plus
    timer["timerTitleCredit"], timer["timerTitleBall"]=score.animateTitle(windowFlipper, numberOfCredit,timer["timerTitleCredit"],numberBallPlayer[round-1],timer["timerTitleBall"])



    #Affichage nombre fps
    printFps = data.fontObjBomber.render("fps : "+str(int(clock.get_fps())), True, (0, 255, 255), (0, 0, 0))
    printFpsRect = printFps.get_rect()
    printFpsRect.topleft = 1156,8
    windowFlipper.blit(printFps, printFpsRect)

    pg.display.flip()
    clock.tick(60)

