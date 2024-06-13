import copy as cp

c = 0

Plat = [
    [2, 2, 1, 1, 1, 2, 2],
    [2, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 2],
    [2, 2, 1, 1, 1, 2, 2],
]

Plat3 = [
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2],
]

Plat2 = [
    [2, 1, 1, 1, 2],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1],
    [2, 1, 1, 1, 2],
]

# Were using a CaleyTable to compute an invariant phi for the board.
# This allows to find potential candidates for solutions, although it does not prove that a solution exists,
# even among these candidates.
# This rule is known as the "rule of three".
# More about this on http://eternitygames.free.fr/Solitaire.html#La%20r%C3%A8gle%20de%20trois

CaleyTable = [
    [0, 1, 2, 3],
    [1, 0, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0],
]


def phi(board):
    phi = [0, 0]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                phi_ = phi_ij(i, j)
                phi = add_phi(phi, phi_)
    return phi


def phi_ij(i, j):
    return [(i + j) % 3 + 1, (i - j) % 3 + 1]


def add_phi(phi1, phi2):
    return [CaleyTable[phi1[0]][phi2[0]], CaleyTable[phi1[1]][phi2[1]]]


def full_board(board):
    fullboard = cp.deepcopy(board)
    for i in range(len(fullboard)):
        for j in range(len(fullboard[i])):
            if fullboard[i][j] == 0:
                fullboard[i][j] = 1
    return fullboard


def check_one_possible_solution(board):
    phi_board = phi(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                if phi_board == phi_ij(i, j):
                    return True
    return False


def check_all_possible_solutions(board):
    fullboard = full_board(board)
    phi_board = phi(fullboard)
    coords = []
    init_positions_phi = []
    last_positions_phi = []
    for i in range(len(fullboard)):
        for j in range(len(fullboard[i])):
            if fullboard[i][j] == 1:
                coords.append([i, j])
                # This is phi for a board with one missing marble at ij
                init_positions_phi.append(add_phi(phi_board, phi_ij(i, j)))
                # This is phi for a board with only one marble at ij
                last_positions_phi.append(phi_ij(i, j))

    for k, init_phi in enumerate(init_positions_phi):
        write_file = False
        coord = coords[k]
        this_board = cp.deepcopy(fullboard)
        this_board[coord[0]][coord[1]] = 0
        file_content = "Starting board :\n"
        for ligne in this_board:
            for el in ligne:
                if el == 2:
                    file_content += " "
                if el == 1:
                    file_content += "0"
                if el == 0:
                    file_content += "."
            file_content += "\n"
        file_content += "\nPossible endings :\n"
        for l, last_phi in enumerate(last_positions_phi):
            if init_phi == last_phi:
                write_file = True
                print("Starting Position {:d} with last position {:d}".format(k, l))
                coord = coords[l]
                this_board = cp.deepcopy(fullboard)
                this_board[coord[0]][coord[1]] = 0
                for ligne in this_board:
                    for el in ligne:
                        if el == 2:
                            file_content += " "
                        if el == 0:  # we invert the board for end position
                            file_content += "0"
                        if el == 1:
                            file_content += "."
                    file_content += "\n"
                file_content += "\n"
        if write_file:
            write_file = open("PotentialSolutions%d.txt" % (k), "w")
            write_file.write(file_content)
            write_file.close()


if __name__ == "__main__":
    check_all_possible_solutions(Plat)
