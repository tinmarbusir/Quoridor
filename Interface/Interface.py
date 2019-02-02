from tkinter import Tk, Canvas, Label, StringVar
from itertools import product
from random import randint

from pprint import pprint

from .pion import Pion
from .muret import Muret
from .grille import Grille

DIMS = {"total": 720,
        "carre": 80,
        "pion": .85,
        "muret": .15
        }


class InterfaceCorridor:
    def __init__(self, partie):
        self.partie = partie

        self.DIMS = {"total": 720}
                #"carre": 80,
                #"pion": .85,
                #"muret": .15


        self.fenetre = Tk()
        self.fenetre.title("KORRRIDOR")

        # label
        self.v = StringVar(value="la stringVar")
        Label(self.fenetre, textvariable=self.v, anchor='n').pack()
        self.canevas = Canvas(
                self.fenetre,
                width=DIMS["total"],
                height=DIMS["total"],
                bg='grey')

        ###################
        # le plateau   ####
        ###################

        self.plateau = self.partie.plateau
        self.nb_cases = self.plateau.nb_cases  # 9 par defaut
        self.cote = self.plateau.cote  # 16 par defaut : 9 pour pion + 8 muret...index à 0
        self.DIMS['carre'] = self.DIMS["total"] // self.nb_cases
        self.DIMS['pion'] = int(self.DIMS['carre'] * .85)
        self.DIMS['muret'] = self.DIMS['carre'] - self.DIMS['pion']
        self.objets = {}
        self.murets = {}
        self.grille = {}
        for i, j in product(range(0, self.cote + 2, 2), range(0, self.cote + 2, 2)):
            # parcourt toutes les cases paires (=cases de pion) de la grille
            coords_I = self.calcul_coords_interface((i, j))
            num = self.canevas.create_rectangle(*coords_I, fill='white', tags="grille")
            self.objets[num] = Grille(id_canevas=num, x_grille=i, y_grille=j)
            self.grille[i, j] = num

        for i, j in product(range(0, self.cote + 2, 2), range(1, self.cote + 1, 2)):  # de 0 à 16, 1 à 15
            # murets horizontaux
            coords_I = self.calcul_coords_interface((i, j))
            num = self.canevas.create_rectangle(*coords_I, fill="white", tags="muret")
            self.objets[num] = Muret(id_canevas=num, x_grille=i, y_grille=j)
            self.murets[i, j] = num

        for i, j in product(range(1, self.cote + 1, 2), range(0, self.cote + 2, 2)):  # de 1 à 15, 0 à 16
            # murets verticaux
            coords_I = self.calcul_coords_interface((i, j))
            num = self.canevas.create_rectangle(*coords_I, fill="white", tags="muret")
            self.objets[num] = Muret(id_canevas=num, x_grille=i, y_grille=j)
            self.murets[i, j] = num

        for i, j in product(range(1, self.cote + 1, 2), range(1, self.cote + 1, 2)):  # de 1 à 15, 1 à 15
            # interstice entre les murets
            coords_I = self.calcul_coords_interface((i, j))
            num = self.canevas.create_rectangle(*coords_I, fill="grey", tags="interstice")
            self.objets[num] = Muret(id_canevas=num, x_grille=i, y_grille=j)
            self.murets[i, j] = num

        ###################
        # les joueurs  ####
        ###################
        self.joueurs = partie.joueurs
        self.id_pions = {}
        self.pions = {}
        if len(self.joueurs) == 2:
            couleur_pions = ('white', 'black')  # "#{:0>6x}".format(randint(0, 256 ** 3 - 1))
        else:
            couleur_pions = ('white', 'grey', 'black', 'brown')  # "#{:0>6x}".format(randint(0, 256 ** 3 - 1))
        for i, joueur in enumerate(self.joueurs):
            coords_I = self.calcul_coords_interface(joueur.coords)
            num = self.canevas.create_oval(*coords_I, fill=couleur_pions[i], tags="pion")
            x, y = joueur.coords
            self.objets[num] = Pion(id_canevas=num, x_grille=x, y_grille=y, joueur=joueur)
            self.id_pions[joueur] = num
            self.pions[joueur] = self.objets[num]



        #self.PION_SELECT = None  # Si un pion est cliqué

        self.canevas.bind(sequence='<Button-1>', func=self.clic_grille)
        # self.canevas.bind(sequence='<B1-ButtonRelease>', func=self.clic_grille)
        self.canevas.focus_set()
        self.canevas.pack(padx=10, pady=10)



    ##########################################################################
    #### De l'interface vers la partie
    ##########################################################################
    def clic_grille(self, event):
        coords = event.x, event.y, event.x, event.y
        id_objs = self.canevas.find_overlapping(*coords)
        if event.type == "4":  # Clic
            self.PION_SELECT = None
            for id_obj in id_objs:
                objet_clic = self.objets[id_obj]
                if id_obj in self.id_pions.values():
                    print(objet_clic) #--> pion du joueur en (x,y)
                    self.PION_SELECT = objet_clic.joueur
                    print(f"mvts possibles: {self.partie.plateau.coord_voisins_immediats(objet_clic.coords)}")
                    return

            for id_obj in id_objs:
                if id_obj in self.grille.values():
                    coords_deplacement = self.objets[id_obj].coords
                    self.message(f"INTERFACE-OUT: self.partie.avancer_pion({self.PION_SELECT}, {coords_deplacement})")
                    self.partie.avancer_pion(coords_deplacement)
                elif id_obj in self.murets.values():
                    # print(objet_clic) #--> muret H/V en (x, y)
                    self.message(f"INTERFACE-OUT: self.partie.bloquer{objet_clic.coords}")
                    self.partie.bloquer(objet_clic.coords)
                    return
                # else:
                #   self.canevas.itemconfig(id_obj, fill="#{:0>6x}".format(randint(0, 256 ** 3 - 1)))
        """elif event.type == "5":  # Release
            if not self.PION_SELECT:
                return
            for id_obj in id_objs:
                if isinstance(self.objets[id_obj], Grille):
                    coords_deplacement = self.objets[id_obj].coords
                    if self.PION_SELECT.coords == coords_deplacement:
                        break
                    self.message(f"INTERFACE-OUT: self.partie.avancer_pion({self.PION_SELECT}, {coords_deplacement})")
                    self.partie.avancer_pion(self.PION_SELECT, coords_deplacement)
                break
            self.PION_SELECT = None
"""
    ##########################################################################
    #### De la partie vers l'interface
    ##########################################################################
    def message(self, message):
        self.v.set(message)
        print(message)

    def bloquer_muret(self, coords):
        self.canevas.itemconfig(self.murets[coords], fill="black")

    def deplacer_pion(self, joueur, coordonnees):
        le_pion = self.pions[joueur]
        if le_pion.deplacer(coordonnees):
            coords = self.calcul_coords_interface(le_pion.coords)
            self.canevas.coords(le_pion.id_canevas, *coords)

    def tour_suivant(self):
        for num in self.grille:
            self.canevas.itemconfig(self.grille[num], fill="white")

        joueur = self.partie.joueur_en_cours
        coord_j = joueur.coords
        coords_possible = self.partie.plateau.coord_voisins_immediats(coord_j)
        self.canevas.itemconfig(self.grille[coord_j], fill="blue")
        for coord in joueur.zone_arrivee:
            self.canevas.itemconfig(self.grille[coord], fill="pink")
        for coord in coords_possible:
            self.canevas.itemconfig(self.grille[coord], fill="grey")

    def partie_terminee(self):
        for num in self.grille:
            self.canevas.itemconfig(self.grille[num], fill="white")
        self.message('partie terminée')

    ##########################################################################
    #### Fonctions internes
    ##########################################################################
    def calcul_coords_interface(self, coord):
        x, y = coord
        x1 = (x // 2) * self.DIMS['carre']
        y1 = (y // 2) * self.DIMS['carre']

        if x % 2:  # Impair, C'est un muret Vertical ou un interstice
            x1 += self.DIMS['pion']
            x2 = x1 + self.DIMS['muret']
            if y % 2:  # Impair et Impair, c'est un interstice entre 2 murets
                y1 += self.DIMS['pion']
                y2 = y1 + self.DIMS['muret']
            else:
                y2 = y1 + self.DIMS['pion']
        elif y % 2:  # Impair, C'est un muret Horizontal
            y1 += self.DIMS['pion']
            x2 = x1 + self.DIMS['pion']
            y2 = y1 + self.DIMS['muret']
        else:  # C'est une case de pion
            x2 = x1 + self.DIMS['pion']
            y2 = y1 + self.DIMS['pion']
        return x1, y1, x2, y2
