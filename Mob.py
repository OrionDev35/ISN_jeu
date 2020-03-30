
class Mob():

    def __init__(self, spawn_x, spawn_y, vMobx, img_Mob_r,img_Mob_l ):
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.vMobx = vMobx
        self.img_Mob_r = img_Mob_r
        self.img_Mob_l = img_Mob_l

    
        












































"""

from Entity import Entity

class Mob(Entity): #classe pour les ennemis qui hérite de Entity

    def __init__(self, hp, posx, posy, img):
        super(Mob, self).__init__(hp, posx, posy, img)

    def update_mob_sprite(self, img_r, img_l,):
        if self.direction == True:
            self.img = img_r
        if self.direction == False:
            self.img = img_l

    def ia(self): #ici la méthode principale qui ferait appel à d'autres methodes de la classe pour régir une ia des ennemis

"""