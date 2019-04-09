from copy import copy

class Plateau:
    def __init__(self, nb_cases, largeur_muret):
        self.nb_cases = nb_cases
        self.largeur_muret = largeur_muret
        self.cote = (nb_cases - 1) * 2  # 16 pour 9 cases de large
        self.coords_murets = []  # de type (1, 1) , coordonnées impaires de 1 à 15
        self.joueurs = []  # append lors de l'initialisation d'un joueur

    def __contains__(self, value):
        return value in self.coords_murets

    def __copy__(self):
        copie = Plateau(self.nb_cases, self.largeur_muret)
        copie.coords_murets = self.coords_murets[:]
        copie.joueurs = self.joueurs
        return copie

    def __add__(self, coord):
        """return another Plateau + coord"""
        plateau_test = copy(self)
        plateau_test += coord
        return plateau_test

    def __iadd__(self, coords):
        """  += """
        self.coords_murets.append(coords)
        return self

    def ajouter_muret(self, coord):
        # coords = (x, y, position)

        if coord not in self:
            x, y = coord
            plateau_test = copy(self)
            for supp in range(self.largeur_muret * 2 - 1):
                if x % 2:  # muret vertical
                    coord_test = (x, y + supp)
                    if y + supp > self.cote:
                        print(f"pose impossible du muret {coord}. il finit en dehors du terrain")
                        return False
                else:
                    coord_test = (x + supp, y)
                    if x + supp > self.cote:
                        print(f"pose impossible du muret {coord}. il finit en dehors du terrain")
                        return False
                if coord_test in self:
                    print(f"pose impossible du muret {coord}. case {coord_test} déjà posée")
                    return False
                else:
                    plateau_test += coord_test
            for joueur in self.joueurs:
                if not joueur.teste_plateau(plateau_test):
                    print(f"bloquant pour {joueur}")
                    break
            else:
                self.coords_murets = plateau_test.coords_murets[:]
                return True
        return False

    def coord_voisins(self, coord):
        x, y = coord
        voisins = set()
        if x > 0 and (x - 1, y) not in self:
            # Vers l' Ouest
            voisins.add((x - 2, y))
        if x < self.cote and (x + 1, y) not in self:
            # Vers l' Est
            voisins.add((x + 2, y))
        if y > 0 and (x, y - 1) not in self:
            # Vers le Nord
            voisins.add((x, y - 2))
        if y < self.cote and (x, y + 1) not in self:
            # Vers le Sud
            voisins.add((x, y + 2))
        return list(voisins)

    def coord_voisins_immediats(self, coord):
        x, y = coord
        coords_joueurs = [joueur.coords for joueur in self.joueurs]
        voisins = set()
        if x > 0 and (x - 1, y) not in self:
            # Vers l' Ouest
            if (x - 2, y) not in coords_joueurs:
                voisins.add((x - 2, y))
            else:
                if x == 2 or (x - 3, y) in self:
                    if (x - 2, y - 1) not in self:
                        voisins.add((x - 2, y - 2))
                    if (x - 2, y + 1) not in self:
                        voisins.add((x - 2, y + 2))
                else:
                    voisins.add((x - 4, y))
        if x < self.cote and (x + 1, y) not in self:
            # Vers l' Est
            if (x + 2, y) not in coords_joueurs:
                voisins.add((x + 2, y))
            else:
                if x == 14 or (x + 3, y) in self:
                    if (x + 2, y - 1) not in self:
                        voisins.add((x + 2, y - 2))
                    if (x + 2, y + 1) not in self:
                        voisins.add((x + 2, y + 2))
                else:
                    voisins.add((x + 4, y))

        if y > 0 and (x, y - 1) not in self:
            # Vers le Nord
            if (x, y - 2) not in coords_joueurs:
                voisins.add((x, y - 2))
            else:
                if y == 2 or (x, y - 3) in self:
                    if (x - 1, y - 2) not in self:
                        voisins.add((x - 2, y - 2))
                    if (x + 1, y - 2) not in self:
                        voisins.add((x + 2, y - 2))
                else:
                    voisins.add((x, y - 4))

        if y < self.cote and (x, y + 1) not in self:
            # Vers le Sud

            if (x, y + 2) not in coords_joueurs:
                voisins.add((x, y + 2))
            else:
                if y == 14 or (x, y + 3) in self:
                    if (x - 1, y + 2) not in self:
                        voisins.add((x - 2, y + 2))
                    if (x + 1, y + 2) not in self:
                        voisins.add((x + 2, y + 2))
                else:
                    voisins.add((x, y + 4))
        voisins.difference_update(coords_joueurs)
        return list(voisins)

    def __str__(self):
        if self.coords_murets:
            return f"le plateau avec les murets suivants: {self.coords_murets}"
        else:
            return f"le plateau encore vierge de murets"

    def __repr__(self):
        return str(self)
