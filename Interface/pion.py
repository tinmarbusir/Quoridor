class Pion:
    def __init__(self, id_canevas, x_grille, y_grille, joueur):
        self.id_canevas = id_canevas
        self.x = x_grille
        self.y = y_grille
        self.joueur = joueur

    @property
    def coords(self):
        return self.x, self.y


    def deplacer(self, coordonnees):
        x_coord, y_coord = coordonnees
        x_move = x_coord - self.x
        y_move = y_coord - self.y
        self.x = x_coord
        self.y = y_coord
        return True

    def __str__(self):
        return f"pion du {self.joueur}"