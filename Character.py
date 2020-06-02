import pygame
class Character(pygame.sprite.Sprite): #classe mère

    def __init__(self, hp, x, y, vx, vy, img):
        self.hp = hp #points de vie
        self.x = x 
        self.y = y
        self.vx = vx
        self.vy = vy
        self.img = img
        self.facing = True #true pour droite, false pour gauche
        self.walk = 0 #nombre de pas jusqu'à arret du deplacement
        pygame.sprite.Sprite.__init__(self)  
    
    def right(self): #méthode de déplacement droit
        self.facing = True
        if self.x <= 2770:
            self.x += self.vx
            self.walk += 1

    def left(self): #méthode de déplacement gauche
        self.facing = False
        if self.x >= 100:
            self.x -= self.vx
            self.walk += 1

    def reset_walk(self):
        self.walk = 0

    def get_hp(self): #méthode de renvoie des points de vie de l'objet
        return(self.hp)

    def get_x(self): #méthode de renvoie de position x de l'objet
        return(self.x)

    def get_y(self): #méthode de renvoie de position y de l'objet
        return(self.y)

    def get_facing(self): #méthode de renvoie de l'orientation de l'objet
        return(self.facing)

    def get_img(self): #méthode de renvoie de l'image de l'objet
        return(self.img)