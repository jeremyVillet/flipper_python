import pygame as pg
import data
fontObj = pg.font.Font("DS-DIGIB.TTF", 45)

#Nous définissons ici les fonctions intervenant dans le score de la partie et sur sa gestion ( affichage score ,compteur de point , gestion game Over ... )

#Fonction gérant l'affichage du score

def displayScore(window,score,numberPlayer,numberBallPlayer,round,timerAnimation):
    namePlayers=[["scoreP1","scoreRectP1"],["scoreP2","scoreRectP2"],["scoreP3","scoreRectP3"],["scoreP4","scoreRectP4"]]

    for x in range(0, 4):
        pg.draw.rect(window, (0, 0, 0), (110, 46 + 105 * x, 200, 41))
    for x in range(0,numberPlayer):
        namePlayers[x][0] = fontObj.render((str(score[x])).rjust(8,"0"), True, (0, 255, 255), (0, 0, 0))
        namePlayers[x][1] =  namePlayers[x][0].get_rect()
        namePlayers[x][1].topleft = (110, 46+105*x)
        window.blit( namePlayers[x][0],  namePlayers[x][1])

    pg.draw.rect(window, (0, 0, 0), (250,615, 70, 40))
    numberBallCurrentPlayer = fontObj.render(str(numberBallPlayer[round]), True, (255, 0, 220), (0, 0, 0))
    numberBallCurrentPlayerRect =numberBallCurrentPlayer.get_rect()
    numberBallCurrentPlayerRect.topleft = (270,615)
    window.blit(numberBallCurrentPlayer, numberBallCurrentPlayerRect)

    for x in range(0,4):
        pg.draw.rect(window, (0, 0, 0), (112,14+x*104, 50, 20))
        pg.draw.rect(window, (0, 0, 0), (249, 14+x*104, 50, 20))

    timerAnimation += 1
    x = 0 if ((timerAnimation // 10) - 1) % 2 == 0 else 1
    window.blit(data.currentPlayer_IMG[x], (112,14+round*104))
    window.blit(data.currentPlayer_IMG[x], (249, 14+round*104))

    return timerAnimation

#Fonction gérant les credits

def insertCoins(window,insert,numberOfCredit):
    insert+=1
    if insert%10==0:
        pg.draw.rect(window, (0, 0, 0), (926, 587, 240, 80))
        window.blit(data.insertCoins_img[insert//10], (926, 587))
    if insert == 10:
        return insert, numberOfCredit + 1
    if insert==50:
        return 0,numberOfCredit
    return insert,numberOfCredit

#Fonction gérant l'affichage des crédits

def displayCredit(window,numberOfCredit):
    pg.draw.rect(window, (0, 0, 0), (120, 614, 40, 40))
    numCredit = fontObj.render(str(numberOfCredit), True, (255, 0, 220), (0, 0, 0))
    numCreditRect =  numCredit.get_rect()
    numCreditRect.topleft = (120, 614)
    window.blit( numCredit,  numCreditRect)


#Gestion score bumber

def manageScoreBumper(window,ball_object_Collection,score,imgBumperDisplayed):
    hitBoxBumpers=[[570,650,333,399],[699,752,455,502],[762,805,457,500],[793,842,493,529],[607,658,458,534],[695,745,350,400]] #coordonnées générant la hitbox du flipper
    for ballObject in ball_object_Collection:
        for x in range(0,len(hitBoxBumpers)):
            if ball_object_Collection[ballObject]!=0:
                if ball_object_Collection[ballObject].body.position[0] >=hitBoxBumpers[x][0] and ball_object_Collection[ballObject].body.position[0] <= hitBoxBumpers[x][1] and ball_object_Collection[ballObject].body.position[1] >= hitBoxBumpers[x][2] and ball_object_Collection[ballObject].body.position[1] <= hitBoxBumpers[x][3]:
                    score+=100

    #Generation texture des bumpers en fonction de leur etat
    coorImgBump = [(584, 315), (696, 305), (697, 205), (768, 212),(611,170),(800,175)] #coordonnées des textures des bumpers
    for i in range(0, len(coorImgBump)):
        image=data.bumperIMG[i]  if imgBumperDisplayed[i] else data.bumperIMGBis[i]
        window.blit(image, coorImgBump[i])

    return score,imgBumperDisplayed

#Animation titre credit et ball si il y en a plus

def animateTitle(window, numberOfCredit,timerTitleCredit,numberBallPlayer,timerTitleBall):
    if numberOfCredit ==0:
        timerTitleCredit+=1
        x=0 if ((timerTitleCredit // 10)-1)%2==0 else 1
        pg.draw.rect(window, (0, 0, 0), (60, 578, 151, 31))
        window.blit(data.creditTitle_img[x], (60, 578))
    if numberBallPlayer == 0:
        timerTitleBall += 1
        y = 0 if ((timerTitleBall // 10) - 1) % 2 == 0 else 1
        pg.draw.rect(window, (0, 0, 0), (210, 578, 131, 31))
        window.blit(data.ballTitle_img[y], (210, 578))

    if numberOfCredit==0 and numberBallPlayer==0 and timerTitleCredit!=timerTitleBall: #Permet de garder synchroniser les deux animations
        timerTitleCredit,timerTitleBall=1,1

    return timerTitleCredit,timerTitleBall

#fonction gerant le rollover NIGHT et DROP

def rollover(window,ball_object_Collection, rolloverActivate, rolloverPosition,hitboxRollover,fontObj):
    numberRolloverMatches = 0
    for x in range(0,len(rolloverPosition)):
        for ballObject in ball_object_Collection:
            if ball_object_Collection[ballObject]!=0:
                if  ball_object_Collection[ballObject].body.position[0] >=hitboxRollover[x][1] and ball_object_Collection[ballObject].body.position[0] <= hitboxRollover[x][2] and ball_object_Collection[ballObject].body.position[1] >= hitboxRollover[x][3] and ball_object_Collection[ballObject].body.position[1] <= hitboxRollover[x][4]:
                    rolloverActivate[hitboxRollover[x][0]]=True
    for letter in rolloverPosition:
        color=(0, 255, 255) if rolloverActivate[letter] else (0,0,0)
        rollover = fontObj.render((str(letter)), True, color, (0, 0, 0))
        rolloverRect =rollover.get_rect()
        rolloverRect.topleft = rolloverPosition[letter]
        window.blit(rollover, rolloverRect)
        if rolloverActivate[letter]:
            numberRolloverMatches+=1

    return rolloverActivate,numberRolloverMatches


#fonction gerant l'animation et la recompense lorsque les rollovers sont validées

def validatedRollover(numberRolloverMatches,timerRollover,window, rolloverPosition,ballcreated,fontObj):
    if numberRolloverMatches==len(rolloverPosition) and timerRollover==0:
        timerRollover = 1
    elif timerRollover>=1 or ballcreated==False :
            timerRollover+=1
            for letter in rolloverPosition:
                color = (0, 255, 255) if ((timerRollover // 10)-1)%2==0 else (255, 0, 220)
                rollover = fontObj.render((str(letter)), True, color, (0, 0, 0))
                rolloverRect = rollover.get_rect()
                rolloverRect.topleft = rolloverPosition[letter]
                window.blit(rollover, rolloverRect)
    else:
        timerRollover=0

    return timerRollover

#fonction gerant les bombers ( animations + scores )

def bombers(window,bomberActivate,ball_object_Collection,score,bomber_img):
    coorBombers=[(812,309),(832,328),(512,32),(538,42),(475,304),(506,291),(537,278)]
    letter={"A":(812,319),"Q":(832,338),"C":(522,25),"D":(548,35),"F":(485,314),"L":(516,301),"Y":(547,288)}
    hitboxBomber=[["A",816,830,370,390],["Q",840,852,351,372],["C",512,531,643,658],["D",540,555,630,647],["F",476,495,380,396],["L",508,525,393,408],["Y",540,558,405,423]]

    for i in range(0,7):
        window.blit(bomber_img[i], coorBombers[i])

        for ballObject in ball_object_Collection:
            if ball_object_Collection[ballObject]!=0:
                if  ball_object_Collection[ballObject].body.position[0] >=hitboxBomber[i][1] and ball_object_Collection[ballObject].body.position[0] <= hitboxBomber[i][2] and ball_object_Collection[ballObject].body.position[1] >= hitboxBomber[i][3] and ball_object_Collection[ballObject].body.position[1] <=hitboxBomber[i][4]:
                    bomberActivate[hitboxBomber[i][0]]=False
                    score+=1000


    for x in letter:
        color = (0, 255, 255) if bomberActivate[x] else (0,0,0)
        letterBomber = data.fontObjBomber.render(x, True,color, (0, 0, 0))
        letterBomberRect = letterBomber.get_rect()
        letterBomberRect.topleft = letter[x]
        window.blit(letterBomber, letterBomberRect)


    bomber=[["A","Q"],["C","D"],["F","L","Y"]]
    for x in range(0,3):
        counter = 0
        for y in range(0,len(bomber[x])):
            if bomberActivate[bomber[x][y]]==False:
                counter+=1
        if counter==len(bomber[x]):
            score+=5000

    return bomberActivate,score

#gestion gameOver
def manageGameOver(window,numberPlayer,numberBallPlayer,numberOfCredit,gameHasBegun,ballCreated,gameOver):
    counter=0
    if ballCreated==False:
        for x in range(0,numberPlayer):
            if numberBallPlayer[x]==0:
                counter += 1

        if gameHasBegun and counter==numberPlayer and numberOfCredit==0:
            if gameOver==False:
                pg.mixer.Sound.play(data.gameOverSound)
            window.blit(data.gameOver, (510, 497))
            pg.display.flip()
            return True
    return False
