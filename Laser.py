class Laser(): #classe en test qui permettrait de créer un objet laser, soit le projectile envoyé quand le player tire

    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.vx = 10
        self.facing = f

    def __del__(self): #méthode appelée une fois l'objet détruit = récupérée dans la mémoire par le ramasse-miettes (garbage-collector)
        pass

