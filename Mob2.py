
from Character import Character
import random

Position_new2 = [100, 2900]
class Mob2(Character): #classe pour les ennemis qui hérite de Character

    def __init__(self, hp, posx, posy, vx, vy, img):
        super(Mob2, self).__init__(hp,posx, posy, vx, vy, img)
        #self.img = img
        self.vy = vy
        self.direction = True
        self.spawn =True
        self.posx = posx
        self.rect = self.img.get_rect()
        self.Position_new = []

    def update_mob_sprite(self, img_r, img_l,):
        if self.direction == True:
            self.img = img_r[0]
        if self.direction == False:
            self.img = img_l[0]

    def ia (self):
        if self.spawn == True:
#Déplacements droits pour vx == 5 et posx == 100......................................;          
            if self.posx < (self.posx + self.vx) and self.posx < 2900  :
                self.direction = True                
                if self.direction == True :
                    self.posx += self.vx
                    if self.posx >= 2900:
                        self.spawn = False
#Déplacements gauche pour vx ==-5 et posx == 2900.....................................;
            if self.posx > (self.posx + self.vx) and self.posx > 100  :
                self.direction = False  
                if self.direction == False :
                    self.posx = self.posx + self.vx
                    if self.posx <= 100 : 
                        self.spawn = False
#Déplacements droits pour vx ==-5 et posx == 100.....................................;                        
            if self.posx > (self.posx + self.vx) and self.posx == 100  :
                self.direction = True
                self.vx = 5
                if self.direction == True:
                    self.posx += self.vx
                    if self.posx >= 2900:
                        self.spawn = False
#Déplacements droits pour vx ==5 et posx == 2900.....................................;
            if self.posx < (self.posx + self.vx) and self.posx >= 2900  :
                self.direction = False
                self.vx = -5
                if self.direction == False:   
                    self.posx += self.vx
                    if self.posx <= 100 : 
                        self.spawn = False
            print(self.posx)
        
        if self.spawn == False :
            self.posx = random.choice(Position_new2)
            
   
    def get_posx(self):
        return(self.posx)