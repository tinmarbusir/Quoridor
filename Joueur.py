from collections import deque
from pprint import pprint

class Joueur:
    def __init__(self, num_joueur, coord_depart, nb_murets, plateau):
        self.num_joueur = num_joueur
        self.nb_murets = nb_murets
        self.x_depart, self.y_depart = coord_depart
        self.x = self.x_depart
        self.y = self.y_depart
        self.plateau = plateau
        plateau.joueurs.append(self)
        self.mon_tour = False
        self.zone_arrivee = []
        for i in range(0, plateau.cote + 2, 2):
            if self.x == 0:
                self.zone_arrivee.append((plateau.cote, i))
            elif self.x == plateau.cote:
                self.zone_arrivee.append((0, i))
            elif self.y == 0:
                self.zone_arrivee.append((i, plateau.cote))
            elif self.y == plateau.cote:
                self.zone_arrivee.append((i, 0))

    @property
    def coords(self):
        return self.x, self.y

    @coords.setter
    def coords(self, coords):
        self.x, self.y = coords

    def victorieux(self):
        return self.coords in self.zone_arrivee

    def distances(self, plateau):
        to_visit = deque()
        dist = {self.coords: 0}
        to_visit.appendleft(self.coords)
        while to_visit:
            actuel = to_visit.pop()
            for voisin in plateau.coord_voisins(actuel):
                if voisin not in dist:
                    dist[voisin] = dist[actuel] + 1
                    to_visit.appendleft(voisin)
        print("\n")
        print(f"#### distances pour {self}")
        for y in range(plateau.cote + 1):
            if y % 2:  # muret horizontal
                for x in range(0, plateau.cote + 1):
                    if x % 2:
                        print("   ", end="")  # rien
                    else:
                        if (x, y) in plateau:
                            print("──", end="")
                        else:  # Rien
                            print("  ", end="")
            else:
                for x in range(plateau.cote + 1):
                    if x % 2:
                        if (x, y) in plateau:
                            print(" | ", end="")
                        else:
                            print("   ", end="")
                    else:
                        if (x, y) in dist:
                            print("{:0>2d}".format(dist[x, y]), end="")
                        else:
                            print("  ", end="")
            print()
        return dist

    def teste_plateau(self, plateau_test):
        return set(self.distances(plateau_test)).intersection(self.zone_arrivee)

    def jouer(self, coup):
        pass

    def __str__(self):
        return f"joueur {self.num_joueur}, {self.nb_murets} murets en ({self.x},{self.y}) "
