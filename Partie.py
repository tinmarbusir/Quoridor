from Joueur import Joueur
from Interface import InterfaceCorridor
from Plateau import Plateau

class Partie:

    def __init__(self, nb_joueurs, nb_cases=9, largeur_muret=2):
        ###########################
        ### Initialiser plateau
        ###########################
        self.nb_cases = nb_cases
        self.case_max = (nb_cases - 1) * 2
        self.largeur_muret = largeur_muret
        self.plateau = Plateau(nb_cases, largeur_muret)
        if nb_joueurs not in (2, 4):
            raise(TypeError, "nb joueurs : 2 ou 4")
        milieuj1 = self.case_max // 4 * 2
        milieuj2 = self.case_max - milieuj1  # En cas de cases paires, évite de mettre les pions en face
        coord_joueurs = [(milieuj1, 0), (milieuj2, self.case_max)]
        if nb_joueurs == 4:
            coord_joueurs.insert(1, (0, milieuj1))
            coord_joueurs.append((self.case_max, milieuj2))
        print(coord_joueurs)
        nb_murets = ((nb_cases + 1) * 2) // nb_joueurs
        self.joueurs = [Joueur(i, coord, nb_murets, self.plateau) for i, coord in enumerate(coord_joueurs)]

        self.nb_tours = -1
        self.joueur_en_cours = self.joueurs[0]
        self.joueurs[0].mon_tour = True

        self.interface = InterfaceCorridor(self)
        self.tour_suivant()
        self.interface.fenetre.mainloop()

    def message(self, message):
        self.interface.message(message)

    def tour_suivant(self):
        if self.joueur_en_cours.victorieux():
            self.joueur_en_cours.mon_tour = False
            self.joueur_en_cours = None
            self.interface.partie_terminee()
            return
        self.nb_tours += 1
        self.joueur_en_cours.mon_tour = False
        self.joueur_en_cours = self.joueurs[self.nb_tours % len(self.joueurs)]
        self.joueur_en_cours.mon_tour = True
        self.interface.tour_suivant()
        self.message(f"tour {self.nb_tours}: tour du {self.joueur_en_cours}")


    def bloquer(self, coords):
        if not self.joueur_en_cours:
            self.message("La partie est terminée.")
            return
        if not self.joueur_en_cours.nb_murets:
            self.message(f"{self.joueur_en_cours} n'a plus de murets")
            return
        x, y = coords
        if x % 2 and y % 2:
            self.message(f"{coords} est un interstice! Impossible à jouer")
            return

        if not self.plateau.ajouter_muret(coords):
            self.message('Blocage non autorisé')
            return
        self.message(f"{self.joueur_en_cours} pose muret en {coords}")
        self.joueur_en_cours.nb_murets -= 1

        x, y = coords

        for supp in range(self.largeur_muret * 2 - 1):
            if x % 2:  # muret vertical
                coord_muret = (x, y + supp)
            else:
                coord_muret = (x + supp, y)
            self.interface.bloquer_muret(coord_muret)
        self.tour_suivant()

    def avancer_pion(self, coords):
        if not self.joueur_en_cours:
            self.message("La partie est terminée.")
            return
        #  if coords in self.plateau.coord_voisins(joueur.coords):
        x_move = self.joueur_en_cours.x - coords[0]
        y_move = self.joueur_en_cours.y - coords[1]
        if coords not in self.plateau.coord_voisins_immediats(self.joueur_en_cours.coords):
            self.message(f"Déplacement en {coords} non autorisé pour {self.joueur_en_cours}")
            return
        # Vérifications terminées, on applique les modifs
        self.message(f"{self.joueur_en_cours} se déplace en {coords}")
        self.joueur_en_cours.coords = coords
        self.interface.deplacer_pion(self.joueur_en_cours, coords)
        self.tour_suivant()


Partie(4, nb_cases=9, largeur_muret=2)
