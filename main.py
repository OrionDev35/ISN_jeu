import time
import pygame as pg
from pygame.locals import*
import random
from Player import Player
from Mob import Mob
from Mob2 import Mob2

# ================================================================================
#                              MAIN
# ================================================================================

#INIT
pg.mixer.pre_init(frequency=48000) #réglé la fréquence sur du 48000Hz, pour mettre les sons dans leurs bonne fréquences
pg.init() #On démarre pygame
pg.mixer.init() #On démarre le module mixer, nous permettant de lire des musiques/sons

screen = pg.display.set_mode([1000, 750]) #ouvre une fenêtre
pg.display.set_caption('The Mandalorian') #donne son titre
clock = pg.time.Clock() #créé une horloge qu'on utilisera dans la boucle principale
score = 0

#MUSIC
pg.mixer.music.load("Musique_fond.wav")
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1) #-1 pour jouer en boucle la musique

#SONS

blaster_1 = pg.mixer.Sound("blaster_1.wav")# --> Son qui va être utilisé lors d'un tir du Blaster
blaster_2 = pg.mixer.Sound("blaster_2.wav")
blaster_3 = pg.mixer.Sound("blaster_3.wav")
blasters = [blaster_1, blaster_2, blaster_3] 
# On créer une liste avec les variables correspondant aux sons, pour ensuite les lire aléatoirement

jawa_d1 = pg.mixer.Sound("jawa_sound_1.wav")# --> Son qui sera utilisé pour la mort des mob(jawa)
jawa_d2 = pg.mixer.Sound("jawa_sound_2.wav")
jawa_d3 = pg.mixer.Sound("jawa_sound_3.wav")
jawa_d4 = pg.mixer.Sound("jawa_sound_4_death.wav")
jawa_d = [jawa_d1, jawa_d2, jawa_d3, jawa_d4]
#idem

sounddeath = random.choice(jawa_d) # On définit ici que la variable sounddeath qui sera un des sons mis dans la liste Jawa_d

clic_sound = pg.mixer.Sound("clic.wav") # Son utilisé lorsqu'on essaie de recharger mais qu'on a plus de munitions
reloading_sound = pg.mixer.Sound("Reloading.wav") # Son utilisé lors du rechargement de balles

#IMAGES (+opti que appel)
background = pg.image.load("background.png").convert() #lag sans le .convert()

jawa_r_1 = pg.image.load("jawa_r_1.png").convert_alpha()#.convert_alpha conserve la transparence
jawa_r_2 = pg.image.load("jawa_r_2.png").convert_alpha()
jawa_r = [jawa_r_1, jawa_r_2]

jawa_l_1 = pg.image.load("jawa_l_1.png").convert_alpha()
jawa_l_2 = pg.image.load("jawa_l_2.png").convert_alpha()
jawa_l = [jawa_l_1, jawa_l_2]

mando_r_0 = pg.image.load("mando_r_0.png").convert_alpha()
mando_r_1 = pg.image.load("mando_r_1.png").convert_alpha()
mando_r_2 = pg.image.load("mando_r_2.png").convert_alpha()
mando_r_j = pg.image.load("mando_r_j.png").convert_alpha()
mando_r_s = pg.image.load("mando_r_s.png").convert_alpha()
mando_r = [mando_r_0, mando_r_1, mando_r_2, mando_r_j, mando_r_s]

mando_l_0 = pg.image.load("mando_l_0.png").convert_alpha()
mando_l_1 = pg.image.load("mando_l_1.png").convert_alpha()
mando_l_2 = pg.image.load("mando_l_2.png").convert_alpha()
mando_l_j = pg.image.load("mando_l_j.png").convert_alpha()
mando_l_s = pg.image.load("mando_l_s.png").convert_alpha()
mando_l = [mando_l_0, mando_l_1, mando_l_2, mando_l_j, mando_l_s]

splash = pg.image.load("splash.png").convert_alpha()

GameOver_img = pg.image.load("GameOver.png").convert_alpha()

laser_img = pg.image.load("Laser.png").convert_alpha()

Final_score_img = pg.image.load("final_score.png").convert_alpha()

hp_img1 = pg.image.load("HP1.png").convert_alpha()
hp_img2 = pg.image.load("HP2.png").convert_alpha()
hp_img3 = pg.image.load("HP3.png").convert_alpha()
hp_img4 = pg.image.load("HP4.png").convert_alpha()

Score_img = pg.image.load("Score.png").convert_alpha()
# -----------------------------------------------------------------------------
#DESSIN

RED = pg.Color(255, 0, 0) #on definit les couleurs
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
GREY = pg.Color(192, 192, 192)
Rouge_foncé = pg.Color(172, 50, 50)

ammo_img = pg.Surface((10, 20)) #On créer l'image "ammo" --> c'est une surface ayant pour coordonnés[10, 20]
pg.draw.rect(ammo_img, GREY, ammo_img.get_rect()) #On rempli la surface avec du gris
pg.draw.rect(ammo_img, BLACK, ammo_img.get_rect(), 3) # Puis on fait des bordures de 3pixels

#TEXTE
police = pg.font.Font("Police_jeu.ttf",30) #on définit la police du texte
reloading_img = police.render("reloading...",True,BLACK) #on définit la var reloading_img, comme un texte noir avec comme police celle d'en haut

police_score = pg.font.Font("Police_jeu.ttf", 24) # idem que pour en haut
police_score_final = pg.font.Font("Police_jeu.ttf", 50)
# -----------------------------------------------------------------------------

running = True #booléens utilisés dans la boucle principale
r = False #Booléens utilisé pour la gestion du déplacement du player --> voir ligne 156 et ligne 195
l = False
j = False
s = False
Collide = True #Booléens utilisé plus tard pour la gestion de collisions
lasers = [] #lasers contenant les objets laser à l'écran 


player = Player(3, 330, 420, 5, 5, mando_r[0], 5) #on crée notre objet player grâce à la class Player du fichier Player (qui hérite de Character)
                                                    # + on renseigne ses paramètres
print(player) #on affiche dans le terminal l'objet player
#.................................................................................................................................................
#Spawn mob..................................................................;

spawn = [100, 2900] #Liste utilisé pour gérer aléatoirement l'abscisse sur laquelle le mob apparait
velocitymob = [5, -5]#Liste utilisé pour gérer aléatoirement la vitesse à laquelle le mob va aller

posmobx = random.choice(spawn)#On prends aléatoirement un membre de la liste Spawn
vmobx = random.choice(velocitymob)#On prends aléatoirement un membre de la liste velocitymob

mob = Mob(1, posmobx, 510, vmobx, 0, jawa_r[0])#On renseigne les paramètres du premier Mob
mob2 = Mob2(1, posmobx, 510, vmobx, 0, jawa_r[0])#On renseigne les paramètres du second Mob

mob2.spawn = False #On définit mob2.spawn false, pour ensuite le faire venir quand le score est supérieur à 10

#.............................................................................
#Laser    
class Laser(): #classe en test qui permettrait de créer un objet laser, soit le projectile envoyé quand le player tire
    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.vx = 10
        self.facing = f
        self.img = laser_img
        self.rect = self.img.get_rect()


# -----------------------------------------------------------------------------
#BOUCLE PRINCIPALE
while running:

    FPS = clock.tick(120) #clock qui régie le nombre d'images calculées en 1s (FPS)
    
    x_player = player.get_x()#x_player devient la position x du Player actuel
    y_player = player.get_y()#y_player devient la position y du Player actuel
    
    Laserspawn = Laser(x_player+60, player.get_y()+110, player.get_facing())#On créer l'objet Laserspawn 
                                                                        #+on renseigne ses paramètres
    
    mob.update_mob_sprite(jawa_r, jawa_l) #On update les class MOB et MOB2 avec leurs images respectives
    mob2.update_mob_sprite(jawa_r, jawa_l)
    # .........................................................................
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pg.KEYDOWN:   #Boucle principale du player, qui gére les touches clavier pour son déplacements     
            if event.key == pg.K_RIGHT :
                r = True
                Collide = False
            if event.key == pg.K_LEFT : 
                l = True  
                Collide = False
            if event.key == pg.K_UP :
                j = True 
            if event.key == pg.K_SPACE :
                s = True
                if player.get_reloading():
                    clic_sound.play() 
                if not player.get_reloading():  #on tire uniquement lorsque le joueur touche le sol et qu'il n'est pas entrain de recharger
                    player.shoot()                  #gère le nb de munitions et le rechargement
                    blast_sound = random.choice(blasters)
                    blast_sound.play()  #On joue le son Blast_sound prit aléatoirement dans blasters
                    lasers.append(Laserspawn) #ajoute un Laser à la liste lasers
          

        if event.type == pg.KEYUP:                    
            if event.key == pg.K_RIGHT :
                r = False
                player.reset_walk()
                Collide = True
            if event.key == pg.K_LEFT : 
                l = False 
                player.reset_walk()
                Collide = True
            if event.key == pg.K_UP :
                j = False      
            if event.key == pg.K_SPACE :
                s = False

    # .........................................................................
    # déplacements
    if r:
        player.right() #si r == True, on active la variables player.right() --> de la class Player

    if l:   
        player.left()  #si l == True, on active la variables player.left() --> de la class Player

    player.jump(j) #La variable player.jump() de la class player, est toujours active avec comme paramètre j
    player.update_sprite(s, mando_r, mando_l) #On update la class Player avec ses images respectives
    
    # .........................................................................
    # scrolling                                
    if x_player <= 450: # Si l'abscisse du player est inférieur ou égale à 450, scroll_x == 0, donc le background ne bouge pas
        scroll_x=0
       
    elif x_player > 450: #Si l'abscisse du player est supérieur à 450, alors scroll_x = x_player -450, 
        scroll_x=x_player - 450 #pour ensuite déplacer le background du nombre de pas dépassé
                
    if scroll_x>2000: #On met une limite, pour ne pas emmener l'image trop loin, et la stopper pour définir notre arène
        scroll_x=2000

    #..........................................................................
    # déplacements Mob
    
    mob.ia() #On active la var ia, de la class mob
    if mob.spawn == False: #Boucle permettant de gérer l'apparition et la disparition du mob quand il est touché
        mob.spawn = True
        mob.ia()
    if score >= 10 : # Quand le score dépasse 10 ou si il est égal à 10 alors on fait venir le deuxième mob
        mob2.spawn= True
        mob2.ia()
        if mob2.spawn == False:
            mob2.spawn = True
            mob2.ia()

    # .........................................................................
    #ACTUALISATION GRAHIQUE
                        
    screen.blit(background,[0,0],[scroll_x,0,1000,750]) #On affiche le bacground à [0, 0], puis on le décalle à l'aide de scroll_x
    screen.blit(Score_img, [875, 30]) #On affiche l'image SCORE : en haut à droite de l'écran

    
    if player.get_hp() > 0:     # Si les points de vie du player sont au dessus de 0, on affiche le player
        screen.blit(player.get_img(), [x_player-scroll_x, player.get_y()])
    if Collide == True:     #Si Collide == True, ça veut dire qu'on gère les collisions lorsque le player ne bouge ni à droite ni à gauche
        if mob.get_posx() == player.get_x() :   #Si x du mob == x du player et que son ordonné est supérieur à 340, 
            if player.get_y() < 340 :   #(ce qui signifie que le player saute au dessus du mob), alors on enlève 1 au points de vie du player
                pass                    #On affiche également l'image splash, montraant la collision
            if player.get_y() >340 :
                player.hp = player.get_hp() -1
                screen.blit(splash, [player.get_x(), player.get_y()])
        if mob2.get_posx() == player.get_x() :  # Idem pour le mob 2
            if player.get_y() < 340 :
                pass
            if player.get_y() >340 :
                player.hp = player.get_hp() -1
                screen.blit(splash, [player.get_x(), player.get_y()])
    if Collide == False:    #Si Collide == False, ça veut dire que le player est en mouvement vers là droite ou vers la gauche
        if mob.get_posx() == player.get_x() + 5  :  #Si xmob == xplayer +5, alors player pv = -0.5 . Le +5 et Le -5 réduisent le nb d'erreur, 
            if player.get_y() < 340 :   #car lorque le logiciel est trop rapide le mob.x n'est jamais égale à player x
                pass
            if player.get_y() >340 :
                player.hp = player.get_hp() -0.5
                screen.blit(splash, [player.get_x(), player.get_y()])
        if mob.get_posx() == player.get_x() - 5  :
            if player.get_y() < 340 :
                pass
            if player.get_y() >340 :
                player.hp = player.get_hp() -0.5
                screen.blit(splash, [player.get_x(), player.get_y()])
        if mob2.get_posx() == player.get_x() + 5  : #Idem pour mob2
            if player.get_y() < 340 :
                pass
            if player.get_y() >340 :
                player.hp = player.get_hp() -0.5
                screen.blit(splash, [player.get_x(), player.get_y()])
        if mob2.get_posx() == player.get_x() - 5  :
            if player.get_y() < 340 :
                pass
            if player.get_y() >340 :
                player.hp = player.get_hp() -0.5
                screen.blit(splash, [player.get_x(), player.get_y()])
              
    #LASER
    for laser in lasers:
        if laser.x > 0 and laser.x < 3000:
            if laser.facing == True:
                laser.x += laser.vx
            if laser.facing == False:
                laser.x -= laser.vx
        else:
            lasers.pop(lasers.index(laser))
        if laser.x == mob.get_posx() and player.get_y() == 420 :
                mob.spawn = False  
                score += 1
                sounddeath.play()
        if laser.x == mob2.get_posx() and player.get_y() == 420 :
                if mob2.get_posx() > 100 and mob2.get_posx() < 2900:
                    mob2.spawn = False  
                    score += 1
                    sounddeath.play()
        screen.blit(laser_img, [laser.x-scroll_x, laser.y])
    if mob.spawn == True:
        screen.blit(mob.img, [mob.posx - scroll_x, 525])
    if mob2.spawn == True:
        screen.blit(mob2.img, [mob2.posx - scroll_x, 525])
    
    nb_score_img = police_score.render(str(score), True, Rouge_foncé)
    nb_score_img_final = police_score_final.render(str(score), True, Rouge_foncé)
    
    screen.blit(nb_score_img, [945, 31])
   
    #ATH
    if player.get_hp() == 3:
        screen.blit(hp_img1, [10, 10])
    if player.get_hp() == 2:
        screen.blit(hp_img2, [10, 10])
    if player.get_hp() == 1:
        screen.blit(hp_img3, [10, 10])
    if player.get_hp() == 0:
        screen.blit(hp_img4, [10, 10])
        screen.blit(GameOver_img, [200, 200])
        screen.blit(Final_score_img,[360, 580])
        screen.blit(nb_score_img_final, [570, 590])
        pg.display.flip()
        time.sleep(4)
        pg.quit()
    #AMMO
    for loop in range(player.get_ammo()):
        pas = loop * 10
        screen.blit(ammo_img, [10+pas, 40])
    if player.get_reloading():
        screen.blit(reloading_img, [10, 40])
        reloading_sound.play()
    
    pg.display.flip() #actualise l'affichage des images
    # .........................................................................
   
# -----------------------------------------------------------------------------
                                        
pg.quit()
# ================================================================================
