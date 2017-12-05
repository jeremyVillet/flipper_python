import pygame as pg


# On stocke ici tous les tableaux de données du flipper, les images , musiques ...
pg.init()
windowFlipper = pg.display.set_mode((1250,700))


#definition des images pygames
menu1=pg.image.load("image/menu1.png").convert_alpha()
menu2=pg.image.load("image/menu2.png").convert_alpha()
menu3=pg.image.load("image/menu3.png").convert_alpha()
menu4=pg.image.load("image/menu4.png").convert_alpha()



areaFlippers=pg.image.load("image/areaFlippers.png").convert_alpha()
ressort1=pg.image.load("image/ressort1.png").convert_alpha()
ressort2=pg.image.load("image/ressort2.png").convert_alpha()
ressort3=pg.image.load("image/ressort3.png").convert_alpha()
ressort4=pg.image.load("image/ressort4.png").convert_alpha()
ressort5=pg.image.load("image/ressort5.png").convert_alpha()

jail1=pg.image.load("image/jail1.png").convert_alpha()
jail2=pg.image.load("image/jail2.png").convert_alpha()
jail3=pg.image.load("image/jail3.png").convert_alpha()

rotor1=pg.image.load("image/rotor1.png").convert_alpha()
rotor2=pg.image.load("image/rotor2.png").convert_alpha()

bumper1=pg.image.load("image/bumper1.png").convert_alpha()
bumper2=pg.image.load("image/bumper2.png").convert_alpha()
bumper3=pg.image.load("image/bumper3.png").convert_alpha()
bumper4=pg.image.load("image/bumper4.png").convert_alpha()
bumper6=pg.image.load("image/bumper6.png").convert_alpha()

bumperBis1=pg.image.load("image/bumper1Bis.png").convert_alpha()
bumperBis2=pg.image.load("image/bumper2Bis.png").convert_alpha()
bumperBis3=pg.image.load("image/bumper3Bis.png").convert_alpha()
bumperBis4=pg.image.load("image/bumper4Bis.png").convert_alpha()
bumperBis6=pg.image.load("image/bumper6Bis.png").convert_alpha()

bumperIMG=[bumper1,bumper2,bumper3,bumper4,bumper2,bumper6]
bumperIMGBis=[bumperBis1,bumperBis2,bumperBis3,bumperBis4,bumperBis2,bumperBis6]

closure1=pg.image.load("image/closure1.png").convert_alpha()
closure2=pg.image.load("image/closure2.png").convert_alpha()

currentPlayerIMG1=pg.image.load("image/currentPlayer.png").convert_alpha()
currentPlayerIMG2=pg.image.load("image/currentPlayer2.png").convert_alpha()

insertCoins0=pg.image.load("image/insertCoins0.jpg").convert_alpha()
insertCoins1=pg.image.load("image/insertCoins1.jpg").convert_alpha()
insertCoins2=pg.image.load("image/insertCoins2.jpg").convert_alpha()
insertCoins3=pg.image.load("image/insertCoins3.jpg").convert_alpha()
insertCoins4=pg.image.load("image/insertCoins4.jpg").convert_alpha()

creditTitle1=pg.image.load("image/creditTitle1.png").convert_alpha()
creditTitle2=pg.image.load("image/creditTitle2.png").convert_alpha()

ballTitle1=pg.image.load("image/ballTitle1.png").convert_alpha()
ballTitle2=pg.image.load("image/ballTitle2.png").convert_alpha()

bomberA=pg.image.load("image/A.png").convert_alpha()
bomberD=pg.image.load("image/D.png").convert_alpha()
bomberC=pg.image.load("image/C.png").convert_alpha()
bomberDbis=pg.image.load("image/Dbis.png").convert_alpha()
bomberF=pg.image.load("image/F.png").convert_alpha()
bomberL=pg.image.load("image/L.png").convert_alpha()
bomberY=pg.image.load("image/Y.png").convert_alpha()

pauseIMG=pg.image.load("image/pause.png")
tiltIMG=pg.image.load("image/tilt.png")
gameOver=pg.image.load("image/gameOver.png")
helico=pg.image.load("image/helicoDeco.png")
#creation de liste d'images facilitant leurs utilisation dans des fichiers externes

menuIMG=[menu1,menu2,menu3,menu4]
ressorts_img=[ressort1,ressort2,ressort3,ressort4,ressort5]
jails_img=[jail1,jail2,jail3]
closures_img=[closure1,closure2]
rotors_img=[rotor1,rotor2]
currentPlayer_IMG=[currentPlayerIMG1,currentPlayerIMG2]
insertCoins_img=[insertCoins0,insertCoins1,insertCoins2,insertCoins3,insertCoins4,insertCoins0]
creditTitle_img=[creditTitle1,creditTitle2]
ballTitle_img=[ballTitle1,ballTitle2]
bombers_img=[bomberA,bomberD,bomberC,bomberDbis,bomberF,bomberL,bomberY]

# coordonnées des mur de la hitbox  (si on cherche coordonnée sur paint.net , enlever 350 a l axe y )

coor=[[368.0,320.0,368,32],[368.0,320,440.0, 351.0],[440.0, 351.0,375, 460],[375, 460,375,654],[375,654,410,675],[410,675,531,674],[531,674,607,696],[607,696,775 ,696],
[403,632,412,632],[412,630,412,468],[412,472,427,455],[427,457,546,457],[546,457,546,597],[546,597,569,616],[569,616,577,616],[577,616,577,557],[577,557,577,567]
,[577,567,577,557],[577,557,569,536],[569,536,564,533],[564,533,564,528],[564,528,562,527],[560,527,564,430],[564,430,553,430],[553,430,553,427],[553,427,469,391],
      [469,391,462,389],[462,389,415,441],[415,441,402,463],[400,463,400,632],[503, 655,553, 634],[553, 634,560, 631],[560, 631,560, 626],[560, 626,544, 619],
      [544, 619,540, 615],[540, 615,536, 613],[536, 613,527, 599],[527, 599,524, 599],[524, 599,524, 478],
      [524, 478,520, 476],[520, 476,448, 476],[448, 476,444, 479],[444, 479,444, 609],[444, 609,469, 630],
      [469, 630,494, 651],[494, 651,498, 655],[498, 655,503, 655],
[386, 266,386, 174],[386, 174,402, 174],[402, 174,402, 104],[402, 104,440, 104],[440, 104,440, 83],[440, 83,449, 83],[449, 83,449, 89],[449, 89,452, 89],
      [452, 89,452, 97],[452, 97,457, 97],[457, 97,457, 107],[457, 107,461, 107],[461, 107,461, 104],[461, 104,477, 104],[477, 104,477, 100]
,[477, 100,493, 100],[493, 100,494, 97],[494, 97,503, 97],[503, 97,503, 100],[503, 100,511, 100],[511, 100,511, 104],[511, 104,507, 104],[507, 104,507,108],
     [441,136,512,105],[441, 136,436, 136],[436, 136,436, 144],[436, 144,432, 152],[432, 152,428, 158],[428, 158,424, 164],[424, 164,420, 171],[420, 171,415, 175],[415, 175,411, 178],
      [411, 178,392, 178],[392, 178,391, 266],[411, 266,416, 266],[416, 266,416, 226],[416, 226,411, 226],[411, 226,411, 266],
      [435, 266,441, 266],[441, 266,441, 226],[441, 226,435, 226],[435, 226,435, 266],[461, 266,465, 266],[465, 266,466, 260],[466, 260,469, 259],[469, 259,474, 249]
    ,[474, 249,478, 237],[478, 237,481, 227],[481, 227,485, 220],[485, 220,490, 213],[490, 213,494, 203],[494, 203,498, 191],[498, 191,503, 181],[503, 181,507, 171],
      [507, 171,510, 160],[510, 160,514, 150],[514, 150,520, 143],[520, 143,520, 135],[520, 135,514, 132],[514, 132,510, 128],[510, 128,498, 128],[498, 128,490, 132],
      [490, 132,481, 135],[481, 135,473, 139],[473, 139,464, 143],[464, 143,457, 145],[457, 145,452, 149],[452, 149,452, 149],[452, 149,447, 157],[447, 157,447, 163],
      [447, 163,452, 168],[452, 168,457, 171],[457, 171,460, 172],[366, 321,366, 31],[460,171,460,264], [366, 31,636, 31],
[907, 359,907, 150],[907, 150,879, 150],[879, 150,879, 359],[862, 359,846, 345],[844, 345,844, 336],[846, 336,854, 318],[854, 318,858, 317],[858, 317,858,308],[
858, 308,866, 287],[866, 287,870, 285],[870, 285,870, 266],[870, 266,874, 266],[874, 266,874, 175],[874, 175,870, 175],
[870, 175,866, 181],[866, 181,846, 181],[846, 181,837, 174],[837, 174,837, 171],[837, 171,833, 171],
[833, 171,833, 209],[833, 209,829, 213],[829, 213,825, 213],[825, 213,820, 209],[820, 209,820, 144],[820, 144,816, 143],[816, 143,735, 108],[735, 108,730, 103],[730, 103,730, 100],[730, 100,737, 97],[737, 97,747, 97],[747, 97,747, 100],[747, 100,763, 100],[763, 100,780, 103],[780, 103,780, 107],[780, 107,783, 107],[783, 107,783, 97],[783, 97,787, 97],[787, 97,787, 90],[787, 90,783, 83],[783, 83,800, 83],
      [800, 83,800, 103],[800, 103,841, 103],[841, 103,841, 31],[841, 31,638, 31],[821, 321,821, 308],[821, 308,826, 308],[826, 308,833, 285],[833, 285,833, 237],[833, 237,829, 237],[829, 237,816, 258]
,[816, 258,808, 276],[808, 276,799, 290],[799, 290,799, 300],[799, 300,816, 321],[816, 321,821, 321], [780, 266,792, 244], [792, 244,792, 150], [792, 150,741, 129], [741, 129,735, 129],
[735, 129,722, 139],[722, 139,722, 145],[767, 248,775, 266],[775, 266,780, 266],[764,248,720,143],[607,461,607,497],[607,497,598,497],[596,497,596,462],[596,462,607,462],[623, 601,630, 601]
,[809, 601,817, 601],[817, 601,817, 556],[817, 556,809, 556],[907,355,907,599],[907,599,895,623],[895,623,883,647],[883,647,833,679],[833,679,776,693],[776,693,776,696],[776,696,593,696]
,[879,355,879,554],[879,554,883,556],[883,556,883,564] ,[874,569,874,497],[874,497,869,497] ,[869,497,869,479],[869,479,866,479],[866,479,862,472] ,[862,472,816,413],[816,413,816,399],[816,399,858,363]
,[858,363,862,363],[862,363,862,358],[630,599,630,556],[630,556,622,556],[622,556,622,599],[622,599,630,599],[668,609,659,609], [659,609,659,560], [659,560,668,560], [668,560,668,609],
[697,563,705,563], [705,563,705,615], [705,615,697,615], [697,615,697,563],[734,616,742,616], [742,616,742,563], [742,563,734,563], [734,563,734,616],[780,559,770,559], [770,559,770,609], [770,609,780,609], [780,609,780,559],[808,601,808,556]
     ]

#coordonnées propres aux bumpers

coordBumper=[[(26, -10),(14, -20),(-15, -20),(-28, -11),(-28, 10),(-15, 18),(14, 18),(26, 10)],[(15, -7) ,(15, 7) ,(10, 11) ,(-10, 11) ,(-15, 7) ,(-15, -7) ,(-10, -11)
,(10, -11)],[(-19, 8) ,(-19, -8) ,(-17, -13) ,(-11, -15) ,(11, -15) ,(16, -13) ,(18, -8) ,(18, 8) ,(16, 12) ,(11, 14) ,(-11, 14) ,(-17, 12)],[(5, -9) ,(-6, -9) ,(-6, -5) ,(-15, -5) ,(-15, 4) ,(-6, 4) ,(-6, 8) ,(6, 8) ,(6, 4) ,(10, 4) ,(10, -5) ,(5, -5)],[(-9, -12) ,(8, -12) ,(18, -5) ,(18, 4) ,
(11, 11) ,(-9, 11) ,(-18, 3) ,(-18, -5)],[(19, -5) ,(19, 5) ,(10, 11) ,(-9, 11) ,(-18, 5) ,(-18, -5) ,(-13, -5) ,(-9, -11) ,(10, -11) ,(15, -5) ]]

bumperPos=[(612,366),(720,377),(726,477),(785,474),(818,511),(632,515),(632,184)]

#son du jeu

reload = pg.mixer.Sound("music/load.wav")
flip_right = pg.mixer.Sound("music/flip_right.wav")
lose = pg.mixer.Sound("music/gameOver.wav")
choc = pg.mixer.Sound("music/choc.wav")
bumper = pg.mixer.Sound("music/bumpers.wav")
end_jail = pg.mixer.Sound("music/end_jail.wav")
soundtilt=pg.mixer.Sound("music/tilt.wav")
gameOverSound=pg.mixer.Sound("music/gameOverGame.wav")
jailSound=pg.mixer.Sound("music/jail.wav")
coinSound=pg.mixer.Sound("music/piece.wav")
ressortSound=pg.mixer.Sound("music/ressort.wav")

#police et taille d'ecriture

fontObjRolloverNight = pg.font.Font("DS-DIGIB.TTF", 35)
fontObjRolloverDrop= pg.font.Font("DS-DIGIB.TTF", 20)
fontObjBomber= pg.font.Font("DS-DIGIB.TTF", 20)