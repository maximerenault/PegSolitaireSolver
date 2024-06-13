import copy as cp
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
from check_board import check_one_possible_solution
import time

t0 = time.time()
c = 0
nbilles_fin = 1
draw = False


board = [
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 1, 0, 0, 2, 2],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2],
]

french_board = [
    [2, 2, 1, 1, 1, 2, 2],
    [2, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 2],
    [2, 2, 1, 1, 1, 2, 2],
]

board = [
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2],
]

board3 = [
    [2, 1, 1, 1, 2],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1],
    [2, 1, 1, 1, 2],
]

if draw:
    fg, ax1 = plt.subplots(nrows=1, ncols=1)
    dess = ax1.imshow(board)

plt.tight_layout()

les_S = []


def les_trous(L):
    """Finds empty spots on the board.

    Args:
        L (list(list)): A board

    Returns:
        list(list): Coordinates of empty spots
    """
    les_coord_0 = []
    for i in range(len(L)):
        for j in range(len(L[0])):
            if L[i][j] == 0:
                les_coord_0.append([i, j])
    return les_coord_0


def les_1(L):
    """Counts number of marbles left.

    Args:
        L (list(list)): A board

    Returns:
        int: Number of marbles
    """
    les_1 = 0
    for i in range(len(L)):
        for j in range(len(L[0])):
            if L[i][j] == 1:
                les_1 += 1
    return les_1


def billes_mouvantes(L):
    """Finds marbles that could move on the current board.

    Args:
        L (list(list)): A board

    Returns:
        tuple(list(list), list(list)): Coordinates of potential marbles, with
    """
    les_coord_billes = []
    les_coord_0 = les_trous(L)
    for k in range(len(les_coord_0)):
        coord = les_coord_0[k]
        C = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        for cxy in C:
            if (
                coord[0] + 2 * cxy[0] < len(L)
                and coord[0] + 2 * cxy[0] >= 0
                and coord[1] + 2 * cxy[1] < len(L[0])
                and coord[1] + 2 * cxy[1] >= 0
                and L[coord[0] + cxy[0]][coord[1] + cxy[1]] == 1
                and L[coord[0] + 2 * cxy[0]][coord[1] + 2 * cxy[1]] == 1
            ):
                les_coord_billes.append([k, coord[0] + 2 * cxy[0], coord[1] + 2 * cxy[1]])
    return les_coord_billes, les_coord_0


def deplacer(L, le_0, le_1):
    """Creates a copy of the board L and edits it to correspond to the move 1 to 0.
    Removes the marble between the two positions (if it exists).

    Args:
        L (list(list)): A board
        le_0 (list): Position of arrival
        le_1 (list): Position of the marble

    Returns:
        list(list): A new board
    """
    L_new = cp.deepcopy(L)
    L_new[le_1[0]][le_1[1]] = 0
    L_new[le_0[0]][le_0[1]] = 1
    L_new[(le_0[0] + le_1[0]) // 2][(le_0[1] + le_1[1]) // 2] = 0
    return L_new


def heur(L):
    """Returns heuristic value for board L.
    It is defined as sum(i**2 + j**2) * n - sum(i)**2 - sum(j)**2
    with i, j the coordinates of marbles and n the number of marbles.
    It corresponds to the variance of positions.

    Args:
        L (list(list)): A board

    Returns:
        int: Value of heuristic
    """
    s1 = 0
    si = 0
    sj = 0
    sij2 = 0
    for i in range(len(L)):
        for j in range(len(L[0])):
            if L[i][j] == 1:
                s1 += 1
                si += i
                sj += j
                sij2 += i**2 + j**2
    return sij2 * s1 - si**2 - sj**2


def recu(Les_L_S, beam_width):
    """Recursively solves a list of board lineages. Performs a beam search to explore each lineage possibility.

    Args:
        Les_L_S (list[list[BOARD]]): All boards we went through in these lineages : BKxSTEPS, BK<=BEAM
        beam_width (int): Width of the beam search
    """
    global c
    global board
    global les_S
    global nbilles_fin
    global draw
    Les_L = []  # Next step boards
    Les_heur = []  # Score of next step boards
    Les_orig = []  # Index of lineage from which next boards come

    for m in range(len(Les_L_S)):
        S1 = Les_L_S[m]
        L1 = S1[-1]
        les_billes_mouvantes, les_0 = billes_mouvantes(L1)
        if draw:
            dess.set_data(L1)
            plt.draw(), plt.pause(1e-04)
        for k in range(len(les_billes_mouvantes)):
            Lk = deplacer(L1, les_0[les_billes_mouvantes[k][0]], les_billes_mouvantes[k][1:])
            if Lk not in Les_L:
                Les_L.append(Lk)
                Les_heur.append(heur(Lk))
                Les_orig.append(m)
        if les_1(L1) == nbilles_fin:
            c += 1
            print("Solution {:d}".format(c))
            file_content = ""
            for p in S1:
                for ligne in p:
                    for el in ligne:
                        if el == 2:
                            file_content += " "
                        if el == 1:
                            file_content += "0"
                        if el == 0:
                            file_content += "."
                    file_content += "\n"
                file_content += "\n"
            write_file = open("solution%d.txt" % (c), "w")
            write_file.write(file_content)
            write_file.close()
            les_S.append(S1)
            Les_L = []

    if len(Les_L) == 0:
        del Les_L_S, Les_L, Les_orig, Les_heur
        print(beam_width * 2)
        print(time.time() - t0)
        recu([[board]], beam_width * 2)
        return 0

    # Sort on heuristic and on boards to discriminate between identical scores
    Les_heur, Les_L, Les_orig = zip(*sorted(zip(Les_heur, Les_L, Les_orig), key=itemgetter(0, 1)))
    Les_L = Les_L[:beam_width]
    Les_orig = Les_orig[:beam_width]
    Les_L_S_new = []

    for k in range(len(Les_L)):
        S2 = cp.copy(Les_L_S[Les_orig[k]])  # Shallow copy if multiple paths use the same original lineage
        S2.append(Les_L[k])  # Add new step to each lineage of the beam
        Les_L_S_new.append(S2)
    del Les_L_S, Les_L, Les_orig, Les_heur

    recu(Les_L_S_new, beam_width)


if __name__ == "__main__":
    if not check_one_possible_solution(board):
        print("No solution for this board")
        exit()

    recu([[board]], 1)

    if len(les_S) != 0:
        for sol in range(len(les_S)):
            for etape in range(len(les_S[0])):
                for ligne in range(len(les_S[0][0])):
                    print(les_S[sol][etape][ligne])
                print("")
                if draw:
                    dess.set_data(les_S[sol][etape])
                    plt.draw(), plt.pause(1.5)
    print("Number of solutions : ", len(les_S))
