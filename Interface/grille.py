
class Grille:
    def __init__(self, id_canevas, x_grille, y_grille):
        self.id_canevas = id_canevas
        self.x = x_grille
        self.y = y_grille

    @property
    def coords(self):
        return self.x, self.y

    def __str__(self):
        return f"grille en ({self.x}, {self.y})"