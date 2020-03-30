from Character import Character #import de la classe mère
import threading #import du threading pour gérer des timers

class Player(Character): #classe

    def __init__(self, hp, posx, y, vx, vy, img, ammo):
        super(Player, self).__init__(hp, posx, y, vx, vy, img) #Player hérite des méthodes et caractéristiques de Character
        self.ammo = ammo #nombre de munition actuel
        self.ammo_max = ammo #nombre de munition max
        self.time_to_reload = 3 #durée de rechargement = au nombre de munitions (1s/munition)
        self.reloading = False #entrain de recharger ?
        self.jumping = False #True quand on reste appuyé sur la touche de saut

    def update_sprite(self, key_s, img_mando_r, ll): #méthode d'actualisation du sprite de l'objet
        if self.facing == True:
            if self.walk == 0:
                self.img = img_mando_r[0]
                
            if self.walk != 0:
                if self.walk%2 == 0:
                    self.img = img_mando_r[1]
                if self.walk%2 == 1:
                    self.img = img_mando_r[2]

            if self.jumping:
                self.img = img_mando_r[3]
            if key_s and not self.jumping:
                self.img = img_mando_r[4]
            
        if self.facing == False:
            if self.walk == 0:
                self.img = ll[0]

            if self.walk != 0:
                if self.walk%2 == 0:
                    self.img = ll[1]
                if self.walk%2 == 1:
                    self.img = ll[2]

            if self.jumping:
                self.img = ll[3]
            if key_s and not self.jumping:
                self.img = ll[4]

    def jump(self, key_j): #méthode pour sauter
        if key_j:
            if self.y == 330:
                self.jumping = True

            if self.jumping:
                self.y -= self.vy

            if self.y < 30:
                self.jumping = False
        else:
            self.jumping = False

        if not self.jumping:
            if self.y < 330:
                self.y += self.vy

    def reload(self): #méthode de rechargement appelée plus bas apès un timer dans la méthode shoot
        self.ammo = self.ammo_max
        print("have reloaded", "remaining ammo =", self.ammo)
        self.reloading = False

    def shoot(self): #méthode pour tirer
        #if not self.reloading:  #on tire uniquement lorsque le joueur n'est pas entrain de recharger
        if self.ammo !=0 :
            self.ammo -= 1
            if self.facing == True:
                print("right shoot -", "remaining ammo =", self.ammo)
            if self.facing == False:
                print("left shoot -", "remaining ammo =", self.ammo) 
        if self.ammo == 0:
            self.reloading = True
            print("reloading") 
            timer = threading.Timer(self.time_to_reload, self.reload) #utilisation du timer
            timer.start() #on appelle la methode self.reload à la fin du timer 

    def get_reloading(self):
        return(self.reloading)

    def get_ammo(self):
        return(self.ammo)