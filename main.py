import random as rd
import pygame as pg
from pygame.locals import*
import random
from Player import Player
from Laser import Laser
#from Mob import Mob

# ================================================================================
# MAIN
# ================================================================================

#INIT
pg.mixer.pre_init(frequency=48000)
pg.init()
pg.mixer.init()

screen = pg.display.set_mode([1000, 750]) #ouvre une fenêtre
pg.display.set_caption('The Mandalorian') #donne son titre
clock = pg.time.Clock() #créé une horloge qu'on utilisera dans la boucle principale

#MUSIC
pg.mixer.music.load("the-mandalorian-theme-8-bit.wav")
pg.mixer.music.play(-1) #-1 pour jouer en boucle la musique

#SONS
blaster_1 = pg.mixer.Sound("blaster_1.wav")
blaster_2 = pg.mixer.Sound("blaster_2.wav")
blaster_3 = pg.mixer.Sound("blaster_3.wav")
blasters = [blaster_1, blaster_2, blaster_3]

clic_sound = pg.mixer.Sound("clic.wav")

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

# -----------------------------------------------------------------------------
#DESSIN

RED = pg.Color(255, 0, 0) #on definit les couleurs
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
GREY = pg.Color(192, 192, 192)

laser_img = pg.Surface((30, 5))  # créé une surface sur laquelle on peut dessiner
pg.draw.rect(laser_img, WHITE, laser_img.get_rect()) #fill
pg.draw.rect(laser_img, RED, laser_img.get_rect(), 3)  #border

hp_img = pg.Surface((120, 20))
pg.draw.rect(hp_img, RED, hp_img.get_rect())
pg.draw.rect(hp_img, BLACK, hp_img.get_rect(), 3)

ammo_img = pg.Surface((10, 20))
pg.draw.rect(ammo_img, GREY, ammo_img.get_rect())
pg.draw.rect(ammo_img, BLACK, ammo_img.get_rect(), 3)

#TEXTE
police = pg.font.Font(None,30)
reloading_img = police.render("reloading...",True,BLACK)
# -----------------------------------------------------------------------------

running = True #booléens utilisés dans la boucle principale
r = False
l = False
j = False
s = False
lasers = [] #lasers contenant les objets laser à l'écran 

player = Player(3, 330, 330, 5, 5, mando_r[0], 5)  #on crée notre objet player grâce à la class Player du fichier Player (qui hérite de Entity)
                                              # + on renseigne ses paramètres
print(player)

"""
spawn_list = [64, 2936]
Spawner = rd.choice(spawn_list)
mob = Mob( Spawner, 330,  9, jawa_r_1, jawa_l_1 )
print(mob)
"""

# -----------------------------------------------------------------------------
#BOUCLE PRINCIPALE
while running:

    dt = clock.tick(120) #clock qui régie le nombre d'images calculées en 1s (FPS)
                        #ça lag étonnement moins à 120 qu'a 60 mais c'est aussi plus rapide

    x_player = player.get_x()
    y_player = player.get_y()
    # .........................................................................
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pg.KEYDOWN:        
            if event.key == pg.K_RIGHT :
                r = True
            if event.key == pg.K_LEFT : 
                l = True  
            if event.key == pg.K_UP :
                j = True 
            if event.key == pg.K_SPACE :
                s = True
                if player.get_reloading():
                    clic_sound.play() 
                if not player.get_reloading():  #on tire uniquement lorsque le joueur touche le sol et qu'il n'est pas entrain de recharger
                    player.shoot()                  #gère le nb de munitions et le rechargement
                    blast_sound = random.choice(blasters)
                    blast_sound.play()
                    lasers.append(Laser(x_player+150, y_player+195, player.get_facing())) #ajoute un Laser à la liste lasers
                

        if event.type == pg.KEYUP:                    
            if event.key == pg.K_RIGHT :
                r = False
                player.reset_walk()
            if event.key == pg.K_LEFT : 
                l = False 
                player.reset_walk()
            if event.key == pg.K_UP :
                j = False      
            if event.key == pg.K_SPACE :
                s = False

    # .........................................................................
    # déplacements
    if r:
        player.right()

    if l:   
        player.left()

    player.jump(j)
    player.update_sprite(s, mando_r, mando_l)

    # .........................................................................
    # scrolling                                
    if x_player <= 330:
        scroll_x=0
       
    elif x_player > 330:
        scroll_x=x_player - 330
                
    if scroll_x>2000:
        scroll_x=2000
    # .........................................................................
    #ACTUALISATION GRAHIQUE
                        
    screen.blit(background,[0,0],[scroll_x,0,1000,750]) #3 paramètres ?
    screen.blit(player.get_img(), [x_player-scroll_x, y_player])
   
    #LASER
    for laser in lasers:
        if laser.x > 0 and laser.x < 3000:
            if laser.facing == True:
                laser.x += laser.vx
            if laser.facing == False:
                laser.x -= laser.vx
        else:
            lasers.pop(lasers.index(laser))
        screen.blit(laser_img, [laser.x-scroll_x, laser.y])

    #ATH
    screen.blit(hp_img, [10, 10])

    for loop in range(player.get_ammo()):
        pas = loop * 10
        screen.blit(ammo_img, [10+pas, 40])
    if player.get_reloading():
        screen.blit(reloading_img, [10, 40])

    pg.display.flip() #actualise l'affichage des images
    # .........................................................................
   
# -----------------------------------------------------------------------------
                                        
pg.quit()
# ================================================================================
