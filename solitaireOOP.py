import copy as cp
import time

t0 = time.time()

Plat = [
    [" ", " ", "0", "0", "0", " ", " "],
    [" ", " ", "0", "0", "0", " ", " "],
    ["0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", ".", ".", "0"],
    ["0", "0", "0", "0", "0", "0", "0"],
    [" ", " ", "0", "0", "0", " ", " "],
    [" ", " ", "0", "0", "0", " ", " "],
]


class Plateau:
    def __init__(self, cases):
        self.mesCases = [x for line in cases for x in line]
        self.maHauteur = len(cases)
        self.maLargeur = len(cases[0])

    def __getitem__(self, i):
        return self.mesCases[i[0] * self.maLargeur + i[1]]

    def __setitem__(self, i, k):
        self.mesCases[i[0] * self.maLargeur + i[1]] = k
        return

    def __eq__(self, p2):
        return self.maHauteur == p2.maHauteur and self.maLargeur == p2.maLargeur and self.mesCases == p2.mesCases

    def __lt__(self, p2):
        return self.mesCases < p2.mesCases

    def __str__(self):
        laStr = ""
        for i in range(len(self.mesCases)):
            if i % self.maLargeur == 0:
                laStr += "\n"
            laStr += self.mesCases[i]
        return laStr

    def nbVides(self):
        c = 0
        for i in self.mesCases:
            if i == ".":
                c += 1
        return c

    def nbBilles(self):
        c = 0
        for i in self.mesCases:
            if i == "0":
                c += 1
        return c


def heur(p):
    s1 = 0
    si = 0
    sj = 0
    sij2 = 0
    for i in range(p.maHauteur):
        for j in range(p.maLargeur):
            if p[i, j] == "0":
                s1 += 1
                si += i
                sj += j
                sij2 += i * i + j * j
    return sij2 * s1 - si * si - sj * sj


class Noeud:
    def __init__(self, heur, plateau):
        self.heur = heur
        self.plat = plateau
        self.chem = [cp.deepcopy(plateau)]

    def __lt__(self, n2):
        return self.heur < n2.heur or (self.heur == n2.heur and self.plat < n2.plat)

    def __eq__(self, n2):
        return self.plat == n2.plat  # and self.heur == n2.heur  # and self.chem == n2.chem

    def __str__(self):
        return str(self.heur) + "\n" + str(self.plat)


class Beam:
    def __init__(self, t):
        self.noeuds = []
        self.taille = t
        self.debord = False

    def __getitem__(self, i):
        return self.noeuds[i]

    def __len__(self):
        return len(self.noeuds)

    def __repr__(self):
        myStr = "["
        for noeud in self.noeuds:
            myStr += str(noeud) + "\n"
        myStr += "]"
        return myStr

    def insert(self, noeud):
        if noeud not in self.noeuds:
            if len(self.noeuds) >= self.taille:
                if noeud < self.noeuds[-1]:
                    del self.noeuds[-1]
                    self.noeuds.append(noeud)
                    self.noeuds = sorted(self.noeuds)
                    self.debord = True
                else:
                    self.debord = True
                    return False
            else:
                self.noeuds.append(noeud)
                self.noeuds = sorted(self.noeuds)
            return True
        return False

    def deb(self):
        return self.debord


def suivant(noeudsSuivants: Beam, noeudprec: Noeud, i0, j0, i1, j1, i2, j2):
    if noeudprec.plat[i0, j0] == "0" and noeudprec.plat[i2, j2] == ".":
        noeud = cp.deepcopy(noeudprec)

        noeud.plat[i0, j0] = "."
        noeud.plat[i1, j1] = "."
        noeud.plat[i2, j2] = "0"

        noeud.heur = heur(noeud.plat)

        noeud.chem.append(cp.deepcopy(noeud.plat))

        noeudsSuivants.insert(noeud)


class Solveur:
    def __init__(self):
        self.maSol = []

    def recherche(self, p1):
        taille = 2
        while self.beamsearch(p1, taille):
            print("Beam width : ", taille)
            print("Time : ", time.time() - t0, "\n")
            taille *= 2
        return self.maSol

    def beamsearch(self, p1, taille):
        encore = False
        noeudsPrec = Beam(taille)
        noeud = Noeud(heur(p1), p1)
        noeudsPrec.insert(noeud)

        n1 = p1.nbBilles()
        n2 = 1
        n = n1
        while n >= n2:
            n -= 1
            noeudsSuivants = Beam(taille)
            for t in range(len(noeudsPrec)):
                it = noeudsPrec[t]
                if it.plat.nbBilles() == 1:
                    self.maSol = it.chem
                    encore = False
                    return encore
                for i in range(it.plat.maHauteur):
                    for j in range(it.plat.maLargeur):
                        if it.plat[i, j] == "0":

                            # Coups horiz
                            if j > 0 and j + 1 < it.plat.maLargeur:
                                suivant(noeudsSuivants, it, i, j - 1, i, j, i, j + 1)
                                suivant(noeudsSuivants, it, i, j + 1, i, j, i, j - 1)

                            # Coups vertic
                            if i > 0 and i + 1 < it.plat.maHauteur:
                                suivant(noeudsSuivants, it, i - 1, j, i, j, i + 1, j)
                                suivant(noeudsSuivants, it, i + 1, j, i, j, i - 1, j)
            if noeudsSuivants.deb():
                encore = True
            noeudsPrec = cp.deepcopy(noeudsSuivants)
        return encore


def rechercheSol(tab):
    p1 = Plateau(tab)
    solv = Solveur()
    ok = solv.recherche(p1)
    if ok:
        for i in range(len(solv.maSol)):
            print(solv.maSol[i])
        return
    else:
        print("Pas de sol :/")
        return


rechercheSol(Plat)
