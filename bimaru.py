# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 103796 Tomás Sobral Teixeira
# 103378 Bernardo Cunha Meireles

from sys import stdin
from search import (
    Problem,
    Node,
    depth_first_tree_search
)

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
            de abertos nas procuras informadas. """
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self):
        self.cells = [[" " for i in range(10)] for j in range(10)]
        self.row_info = []
        self.col_info = []
        self.unplaced_ones = 4
        self.unplaced_twos = 3
        self.unplaced_threes = 2
        self.unplaced_fours = 1
        self.to_run_m_hints = []
        self.unknown_boats = []
        self.middle_pieces = []

    def copy_board(self):
        new_board = Board()
        new_board.cells = [row[:] for row in self.cells]
        new_board.row_info = list(self.row_info)
        new_board.col_info = list(self.col_info)
        new_board.unplaced_ones = self.unplaced_ones
        new_board.unplaced_twos = self.unplaced_twos
        new_board.unplaced_threes = self.unplaced_threes
        new_board.unplaced_fours = self.unplaced_fours
        new_board.to_run_m_hints = list(self.to_run_m_hints)
        new_board.unknown_boats = list(self.unknown_boats)
        new_board.middle_pieces = list(self.middle_pieces)
        
        return new_board

    def set_value(self, row: int, col: int, value: str):
        """Atribui o valor na respetiva posição do tabuleiro."""   
        if row >= 0 and row <= 9 and col >= 0 and col <= 9:
            if self.get_value(row, col) in ["t", "T", "b", "B", "c", "C", "m", "M", "l", "L", "r", "R", "W"]:
                return
            if value not in ["W", "."] and self.get_value(row, col) not in "?":
                self.row_info[row] = self.row_info[row] - 1
                self.col_info[col] = self.col_info[col] - 1
            self.cells[row][col] = value
            if value == "?":
                self.unknown_boats.append((row, col))
            elif value in ["m", "M"]:
                self.middle_pieces.append((row, col))
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row >= 0 and row <= 9 and col >= 0 and col <= 9:
            return self.cells[row][col]

    def is_empty(self, row: int, col: int) -> bool:
        """Devolve True se a posição estiver vazia."""
        if row > 9 or row < 0 or col > 9 or col < 0:
            return False
        return self.cells[row][col] == " "
    
    def is_water(self, row: int, col: int) -> bool:
        """Devolve True se a posição estiver vazia."""
        if row > 9 or row < 0 or col > 9 or col < 0:
            return False
        return self.cells[row][col] in ["W", "."]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.cells[row - 1][col] if row != 0 else None, self.cells[row + 1][col] if row != 9 else None)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.cells[row][col - 1] if col != 0 else None, self.cells[row][col + 1] if col != 9 else None)

    def get_surroundings(self, row: int, col: int) -> list:
        surroundings = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(row + surrounding[0], col + surrounding[1]) for surrounding in surroundings if (row + surrounding[0] >= 0 and row + surrounding[0] <= 9) and (col + surrounding[1] >= 0 and col + surrounding[1] <= 9)]

    def c_hint(self, row: int, col: int):
        self.unplaced_ones -= 1
        surroundings = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        for coordinate in surroundings:
            self.set_value(row + coordinate[0], col + coordinate[1], ".")

    def m_hint(self, row: int, col: int):
        if self.is_water(row + 1, col) or self.is_water(row - 1, col):
            # barco é horizontal
            if self.unplaced_fours == 0:
                self.unplaced_threes -= 1
                self.set_value(row, col - 1, "l")
                self.set_value(row, col + 1, "r")

                self.set_value(row, col - 2, ".")
                self.set_value(row, col + 2, ".")

            else:
                self.set_value(row, col - 1, "?")
                self.set_value(row, col + 1, "?")

            self.set_value(row - 1, col -2, ".")
            self.set_value(row - 1, col - 1, ".")
            self.set_value(row - 1, col, ".")
            self.set_value(row - 1, col + 1, ".")
            self.set_value(row - 1, col + 2, ".")

            self.set_value(row + 1, col -2, ".")
            self.set_value(row + 1, col - 1, ".")
            self.set_value(row + 1, col, ".")
            self.set_value(row + 1, col + 1, ".")
            self.set_value(row + 1, col + 2, ".")

        elif self.is_water(row, col + 1) or self.is_water(row, col - 1):
            if self.unplaced_fours == 0:
                self.unplaced_threes -= 1
                self.set_value(row - 1, col, "t")
                self.set_value(row + 1, col, "b")

                self.set_value(row - 2, col, ".")
                self.set_value(row + 2, col, ".")
            else:
                self.set_value(row - 1, col, "?")
                self.set_value(row + 1, col, "?")

            self.set_value(row - 2, col - 1, ".")
            self.set_value(row - 1, col - 1, ".")
            self.set_value(row, col - 1, ".")
            self.set_value(row + 1, col - 1, ".")
            self.set_value(row + 2, col - 1, ".")

            self.set_value(row - 2, col + 1, ".")
            self.set_value(row - 1, col + 1, ".")
            self.set_value(row, col + 1, ".")
            self.set_value(row + 1, col + 1, ".")
            self.set_value(row + 2, col + 1, ".")

    def t_hint(self, row: int, col: int):
        water_surroundings = [(2, -1), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1)]
        for coordinate in water_surroundings:
            self.set_value(row + coordinate[0], col + coordinate[1], ".")
        self.set_value(row + 1, col, "?")

    def b_hint(self, row: int, col: int):
        water_surroundings = [(-2, -1), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-2, 1)]
        for coordinate in water_surroundings:
            self.set_value(row + coordinate[0], col + coordinate[1], ".")
        self.set_value(row - 1, col, "?")

    def r_hint(self, row: int, col: int):
        water_surroundings = [(-1, -2), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (1, -2)]
        for coordinate in water_surroundings:
            self.set_value(row + coordinate[0], col + coordinate[1], ".")
        self.set_value(row, col - 1, "?")

    def l_hint(self, row: int, col: int):
        water_surroundings = [(-1, 2), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (1, 2)]
        for coordinate in water_surroundings:
            self.set_value(row + coordinate[0], col + coordinate[1], ".")
        self.set_value(row, col + 1, "?")

    def fill_water(self):
        for row in range(len(self.row_info)):
            if self.row_info[row] == 0:
                self.cells[row] = [x if x != " " else "." for x in self.cells[row]]

        for col in range(len(self.col_info)):
            if self.col_info[col] == 0:
                for row in range(len(self.cells)):
                    if self.cells[row][col] == " ":
                        self.cells[row][col] = "."

        for row_index, row in enumerate(self.cells):
            for col_index, cell in enumerate(row):
                if cell in ["t", "b", "l", "r", "m"]:
                    for x in self.get_surroundings(row_index, col_index):
                        if self.is_empty(x[0], x[1]):
                            self.set_value(x[0], x[1], ".")

        self.check_boat_spots(True)

    def check_boat_spots(self, from_fill_water=False):
        changed = False
        for row_index, row in enumerate(self.cells):
            if self.row_info[row_index] == self.cells[row_index].count(" ") > 0:
                    
                    for col_index, col in enumerate(row): # AQUI
                        if self.get_value(row_index, col_index) == " " and self.col_info[col_index] > 0:
                            changed = True
                            #print("[1] Placed ? at ", row_index, col_index)
                            self.set_value(row_index, col_index, "?")

        for col_index in range(len(self.cells[0])):
            col_values = [self.get_value(row_index, col_index) for row_index in range(len(self.cells))]
            if self.col_info[col_index] == col_values.count(" ") > 0:
                
                for row_index in range(len(self.cells)):
                    if self.get_value(row_index, col_index) == " " and self.col_info[col_index] > 0:
                        changed = True
                        #print("[2] Placed ? at ", row_index, col_index)
                        self.set_value(row_index, col_index, "?")

        if changed:
            self.check_boat_spots()

        if not from_fill_water:
            self.fill_water()

    def handle_boats(self):
        if self.unplaced_threes > 0:
            for middle in self.middle_pieces:
                adjacent_verticals = self.adjacent_vertical_values(middle[0], middle[1])
                if all([x == "?" for x in adjacent_verticals]) and \
                        self.get_value(middle[0] - 2, middle[1]) in [".", "W", None] and \
                        self.get_value(middle[0] + 2, middle[1]) in [".", "W", None]:
                    
                    self.place_three(middle[0] - 1, middle[1], True)
                
                adjacent_horizontals = self.adjacent_horizontal_values(middle[0], middle[1])
                if all([x == "?" for x in adjacent_horizontals]) and \
                        self.get_value(middle[0], middle[1] - 2) in [".", "W", None] and \
                        self.get_value(middle[0], middle[1] + 2) in [".", "W",None]:
                    
                    self.place_three(middle[0], middle[1] - 1, False)
                    
        for boat in self.unknown_boats:
            if self.get_value(boat[0], boat[1]) == "?":
                if self.unplaced_ones > 0:
                    if all([self.is_water(x[0], x[1]) for x in self.get_surroundings(boat[0], boat[1])]):
                        self.place_one(boat[0], boat[1])

                if self.unplaced_fours > 0:
                    # top piece
                    if self.get_value(boat[0] - 1, boat[1]) in [".", "W", None] and \
                        self.get_value(boat[0] + 1, boat[1]) in ["m", "M", "?"] and \
                        self.get_value(boat[0] + 2, boat[1]) in ["m", "M", "?"] and \
                        self.get_value(boat[0] + 3, boat[1]) in ["b", "B", "?"]:

                        self.place_four(boat[0], boat[1], True)
                    
                    # bottom piece
                    elif self.get_value(boat[0] + 1, boat[1]) in [".", "W", None] and \
                            self.get_value(boat[0] - 1, boat[1]) in ["m", "M", "?"] and \
                            self.get_value(boat[0] - 2, boat[1]) in ["m", "M", "?"] and \
                            self.get_value(boat[0] - 3, boat[1]) in ["t", "T", "?"]:

                        self.place_four(boat[0] - 3, boat[1], True)

                    # top middle piece
                    elif self.get_value(boat[0] - 1, boat[1]) in ["t", "T", "?"] and \
                            self.get_value(boat[0] + 1, boat[1]) in ["m", "M", "?"] and \
                            self.get_value(boat[0] + 2, boat[1]) in ["b", "B", "?"]:
                        
                        self.place_four(boat[0] - 1, boat[1], True)

                    # bottom middle piece
                    elif self.get_value(boat[0] + 1, boat[1]) in ["b", "B", "?"] and \
                            self.get_value(boat[0] - 1, boat[1]) in ["m", "M", "?"] and \
                            self.get_value(boat[0] - 2, boat[1]) in ["t", "T", "?"]:

                        self.place_four(boat[0] - 2, boat[1], True)

                    # left piece
                    if self.get_value(boat[0], boat[1] - 1) in [".", "W", None] and \
                            self.get_value(boat[0], boat[1] + 1) in ["m", "M", "?"] and \
                            self.get_value(boat[0], boat[1] + 2) in ["m", "M", "?"] and \
                            self.get_value(boat[0], boat[1] + 3) in ["r", "R", "?"]:

                        self.place_four(boat[0], boat[1], False)

                    # left middle piece
                    elif self.get_value(boat[0], boat[1] - 1) in ["l", "L", "?"] and \
                            self.get_value(boat[0], boat[1] + 1) in ["m", "M", "?"] and \
                            self.get_value(boat[0], boat[1] + 2) in ["r", "R", "?"]:

                        self.place_four(boat[0], boat[1] - 1, False)

                    # middle right piece
                    elif self.get_value(boat[0], boat[1] + 1) in ["r", "R", "?"] and \
                            self.get_value(boat[0], boat[1] - 1) in ["m", "M", "?"] and \
                            self.get_value(boat[0], boat[1] - 2) in ["l", "L", "?"]:

                        self.place_four(boat[0], boat[1] - 2, False)

                    # right piece
                    elif self.get_value(boat[0], boat[1] + 1) in [".", "W", None] and \
                            self.get_value(boat[0], boat[1] - 1) in ["m", "M", "?"] and \
                            self.get_value(boat[0], boat[1] - 2) in ["m", "M", "?"] and \
                            self.get_value(boat[0], boat[1] - 3) in ["l", "L", "?"]:

                        self.place_four(boat[0], boat[1] - 3, False)                                    

                if self.unplaced_threes > 0:
                    
                    if self.get_value(boat[0] - 1, boat[1]) in ["t", "T", "?"] and \
                        self.get_value(boat[0] + 1, boat[1]) in ["b", "B", "?"] and \
                        self.get_value(boat[0] - 2, boat[1]) in [".", "W", None] and \
                        self.get_value(boat[0] + 2, boat[1]) in [".", "W", None]:


                        self.place_three(boat[0] - 1, boat[1], True)

                    elif self.get_value(boat[0], boat[1] - 1) in ["l", "L", "?"] and \
                        self.get_value(boat[0], boat[1] + 1) in ["r", "R", "?"] and \
                        self.get_value(boat[0], boat[1] - 2) in [".", "W", None] and \
                        self.get_value(boat[0], boat[1] + 2) in [".", "W", None]:

                        self.place_three(boat[0], boat[1] - 1, False)

                if self.unplaced_twos > 0:
                    if self.get_value(boat[0] + 1, boat[1]) in ["b", "B"] and self.get_value(boat[0] - 1, boat[1]) in [".", "W", None]:
                        self.place_two(boat[0], boat[1], True)

                    elif self.get_value(boat[0] - 1, boat[1]) in ["t", "T"] and self.get_value(boat[0] + 1, boat[1]) in [".", "W", None]:
                        self.place_two(boat[0] - 1, boat[1], True)

                    elif self.get_value(boat[0], boat[1] + 1) in ["r", "R"] and self.get_value(boat[0], boat[1] - 1) in [".", "W", None]:
                        self.place_two(boat[0], boat[1], False)

                    elif self.get_value(boat[0], boat[1] - 1) in ["l", "L"] and self.get_value(boat[0], boat[1] + 1) in [".", "W", None]:
                        self.place_two(boat[0], boat[1] - 1, False)

                    elif self.get_value(boat[0] + 1, boat[1]) == "?" and self.get_value(boat[0] - 1, boat[1]) in [".", "W", None] and self.get_value(boat[0] + 2, boat[1]) in [".", "W", None]:
                        self.place_two(boat[0], boat[1], True)

                    elif self.get_value(boat[0] - 1, boat[1]) == "?" and self.get_value(boat[0] + 1, boat[1]) in [".", "W", None] and self.get_value(boat[0] - 2, boat[1]) in [".", "W", None]:
                        self.place_two(boat[0] - 1, boat[1], True)

                    elif self.get_value(boat[0], boat[1] + 1) == "?" and self.get_value(boat[0], boat[1] - 1) in [".", "W", None] and self.get_value(boat[0], boat[1] + 2) in [".", "W", None]:
                        self.place_two(boat[0], boat[1], False)

                    elif self.get_value(boat[0], boat[1] - 1) == "?" and self.get_value(boat[0], boat[1] + 1) in [".", "W", None] and self.get_value(boat[0], boat[1] - 2) in [".", "W", None]:
                        self.place_two(boat[0], boat[1] - 1, False)

    def handle_m_queue(self):
        for hint in board.to_run_m_hints:
            board.m_hint(hint[0], hint[1])

    def print_board(self):
        print("  " + " ".join([str(x) for x in self.col_info]))
        for i in range(len(self.cells)):
            print(str(self.row_info[i]) + " " + " ".join(self.cells[i]))

        #for i in range(len(self.cells)):
        #    print("".join(self.cells[i]), sep="")

    def place_one(self, row: int, col: int):
        self.set_value(row, col, "c")
        for surround in self.get_surroundings(row, col):
            self.set_value(surround[0], surround[1], ".")
        self.unplaced_ones -= 1

    def place_two(self, row: int, col: int, vertical: bool):
        if vertical:
            self.set_value(row, col, "t")
            self.set_value(row + 1, col, "b")

            for surround in [(-1 , -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 1), (2, -1), (2, 0), (2, 1)]:
                self.set_value(row + surround[0], col + surround[1], ".")
        else:
            self.set_value(row, col, "l")
            self.set_value(row, col + 1, "r")

            for surround in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, 2), (1, 2), (1, 1), (1, 0), (1, -1)]:
                self.set_value(row + surround[0], col + surround[1], ".")

        self.unplaced_twos -= 1

    def place_three(self, row: int, col: int, vertical: bool):
        if vertical:
            self.set_value(row, col, "t")
            self.set_value(row + 1, col, "m")
            self.set_value(row + 2, col, "b")

            for surround in [(-1 , -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 1), (2, -1), (2, 1), (3, -1), (3, 0), (3, 1)]:
                self.set_value(row + surround[0], col + surround[1], ".")
        else:
            self.set_value(row, col, "l")
            self.set_value(row, col + 1, "m")
            self.set_value(row, col + 2, "r")

            for surround in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, 3), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1)]:
                self.set_value(row + surround[0], col + surround[1], ".")

        self.unplaced_threes -= 1

    def place_four(self, row: int, col: int, vertical: bool):
        if vertical:
            self.set_value(row, col, "t")
            self.set_value(row + 1, col, "m")
            self.set_value(row + 2, col, "m")
            self.set_value(row + 3, col, "b")

            for surround in [(-1 , -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (4, 0), (4, -1), (3, -1), (2, -1), (1, -1), (0, -1)]:
                self.set_value(row + surround[0], col + surround[1], ".")
        else:
            self.set_value(row, col, "l")
            self.set_value(row, col + 1, "m")
            self.set_value(row, col + 2, "m")
            self.set_value(row, col + 3, "r")

            for surround in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4), (0, 4), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1)]:
                self.set_value(row + surround[0], col + surround[1], ".")

        self.unplaced_fours -= 1

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        
        board = Board()

        board.row_info = [int (x) for x in stdin.readline().split()[1:]]
        board.col_info = [int(x) for x in stdin.readline().split()[1:]]

        hint_info = stdin.readline().split()

        for hint in range(int(hint_info[0])):
            hintLine = stdin.readline().split()

            board.set_value(int(hintLine[1]), int(hintLine[2]), hintLine[3])

            if hintLine[3] == "C":
                board.c_hint(int(hintLine[1]), int(hintLine[2]))
            elif hintLine[3] == "T":
                board.t_hint(int(hintLine[1]), int(hintLine[2]))
            elif hintLine[3] == "B":
                board.b_hint(int(hintLine[1]), int(hintLine[2]))
            elif hintLine[3] == "R":
                board.r_hint(int(hintLine[1]), int(hintLine[2]))
            elif hintLine[3] == "L":
                board.l_hint(int(hintLine[1]), int(hintLine[2]))
            elif hintLine[3] == "M":
                board.to_run_m_hints.append((int(hintLine[1]), int(hintLine[2])))
        

        return board



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        board = state.board

        cells = board.cells
        row_info = board.row_info
        col_info = board.col_info

        if any(x < 0 for x in row_info + col_info):
            return []

        possibleActions = []

        #board.print_board()

        piece_positions_in_column = [0 for i in range(10)]

        for row_index, row in enumerate(cells):
            for col_index, cell in enumerate(row):
                if cell == "?":
                    piece_positions_in_column[col_index] += 1
        
        #print(piece_positions_in_column)

        for row_index, row in enumerate(cells):
            for col_index, cell in enumerate(row):
                if cell in ["?", " ", "m", "M"]:
                    if board.unplaced_fours > 0:
                        if cell in ["m", "M"]:
                            counter = 3
                        else:
                            counter = 4

                        #vertical
                        # top piece
                        
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (4, 0), (4, -1), (3, -1), (2, -1), (1, -1), (0, -1), (-1, -1)]]) \
                            and board.get_value(row_index + 1, col_index) in [" ", "?", "m", "M"] and board.get_value(row_index + 2, col_index) in [" ", "?", "m", "M"] and board.get_value(row_index + 3, col_index) in [" ", "?", "r", "R"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= 4 and all([row_info[row_index + add] + row.count("?") >= 1 for add in [1, 2, 3]]):
                                if (row_index, col_index, "4V") not in possibleActions:
                                    possibleActions.append((row_index, col_index, "4V"))

                        # top middle piece
                        if all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-2, -1), (-2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (3, 0), (3, -1), (2, -1), (1, -1), (0, -1), (-1, -1)]]) \
                            and board.get_value(row_index - 1, col_index) in [" ", "?", "t", "T"] and board.get_value(row_index + 1, col_index) in [" ", "?", "m", "M"] and board.get_value(row_index + 2, col_index) in [" ", "?", "b", "B"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= counter and all([row_info[row_index + add] + row.count("?") >= 1 for add in [-1, 1, 2]]):
                                if (row_index - 1, col_index, "4V") not in possibleActions:
                                    possibleActions.append((row_index - 1, col_index, "4V"))

                        # bottom middle piece
                        if all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-3, -1), (-3, 0), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (2, 0), (2, -1), (1, -1), (0, -1), (-1, -1), (-2, -1)]]) \
                            and board.get_value(row_index - 2, col_index) in [" ", "?", "t", "T"] and board.get_value(row_index - 1, col_index) in [" ", "?", "m", "M"] and board.get_value(row_index + 1, col_index) in [" ", "?", "b", "B"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= counter and all([row_info[row_index + add] + row.count("?") >= 1 for add in [-2, -1, 1]]):
                            if (row_index - 2, col_index, "4V") not in possibleActions:
                                possibleActions.append((row_index - 2, col_index, "4V"))
                        
                        # bottom piece
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-4, -1), (-4, 0), (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-2, -1), (-3, -1)]]) \
                            and board.get_value(row_index - 3, col_index) in [" ", "?", "t", "T"] and board.get_value(row_index - 2, col_index) in [" ", "?", "m", "M"] and board.get_value(row_index - 1, col_index) in [" ", "?", "b", "B"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= 4 and all([row_info[row_index + add] + row.count("?") >= 1 for add in [-3, -2, -1]]):
                            if (row_index - 3, col_index, "4V") not in possibleActions:
                                possibleActions.append((row_index - 3, col_index, "4V"))
                        
                        # horizontal
                        # left piece
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4), (0, 4), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1), (0, -1)]]) \
                            and board.get_value(row_index, col_index + 1) in [" ", "?", "m", "M"] and board.get_value(row_index, col_index + 2) in [" ", "?", "m", "M"] and board.get_value(row_index, col_index + 3) in [" ", "?", "r", "R"] \
                            and row_info[row_index] + row.count("?") >= 4 and all([col_info[col_index + add] + piece_positions_in_column[col_index + add] >= 1 for add in [1, 2, 3]]):
                            if (row_index, col_index, "4H") not in possibleActions:
                                possibleActions.append((row_index, col_index, "4H"))

                        # left middle piece
                        if all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, 3), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1), (1, -2), (0, -2)]]) \
                            and board.get_value(row_index, col_index - 1) in [" ", "?", "l", "L"] and board.get_value(row_index, col_index + 1) in [" ", "?", "m", "M"] and board.get_value(row_index, col_index + 2) in [" ", "?", "r", "R"] \
                            and row_info[row_index] + row.count("?") >= counter and all([col_info[col_index + add] + piece_positions_in_column[col_index + add] >= 1 for add in [-1, 1, 2]]):
                            if (row_index, col_index - 1, "4H") not in possibleActions:
                                possibleActions.append((row_index, col_index - 1, "4H"))

                        # right middle piece
                        if all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, 2), (1, 2), (1, 1), (1, 0), (1, -1), (1, -2), (1, -3), (0, -3)]]) \
                            and board.get_value(row_index, col_index - 2) in [" ", "?", "l", "L"] and board.get_value(row_index, col_index - 1) in [" ", "?", "m", "M"] and board.get_value(row_index, col_index + 1) in [" ", "?", "r", "R"] \
                            and row_info[row_index] + row.count("?") >= counter and all([col_info[col_index + add] + piece_positions_in_column[col_index + add] >= 1 for add in [-2, -1, 1]]):
                            if (row_index, col_index - 2, "4H") not in possibleActions:
                                possibleActions.append((row_index, col_index - 2, "4H"))

                        # right piece
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -4), (-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (1, -2), (1, -3), (1, -4), (0, -4)]]) \
                            and board.get_value(row_index, col_index - 3) in [" ", "?", "l", "L"] and board.get_value(row_index, col_index - 2) in [" ", "?", "m", "M"] and board.get_value(row_index, col_index - 1) in [" ", "?", "m", "M"] \
                            and row_info[row_index] + row.count("?") >= 4 and all([col_info[col_index + add] + piece_positions_in_column[col_index + add] >= 1 for add in [-3, -2, -1]]):
                            if (row_index, col_index - 3, "4H") not in possibleActions:
                                possibleActions.append((row_index, col_index - 3, "4H"))

                        
                    
                    if board.unplaced_threes > 0:
                        #vertical
                        # top piece
                        if cell in ["m", "M"]:
                            counter = 2
                        else:
                            counter = 3

                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (3, 0), (3, -1), (2, -1), (1, -1), (0, -1)]]) \
                            and board.get_value(row_index + 1, col_index) in [" ", "?", "m", "M"] and board.get_value(row_index + 2, col_index) in [" ", "?", "b", "B"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= 3 and all([row_info[row_index + add] + row.count("?") >= 1 for add in [1, 2]]):
                            if (row_index, col_index, "3V") not in possibleActions:
                                possibleActions.append((row_index, col_index, "3V"))

                        # middle piece
                        if all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-2, -1), (-2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (2, 0), (2, -1), (1, -1), (0, -1), (-1, -1)]]) \
                            and board.get_value(row_index - 1, col_index) in [" ", "?", "t", "T"] and board.get_value(row_index + 1, col_index) in [" ", "?", "b", "B"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= counter and all([row_info[row_index + add] + row.count("?") >= 1 for add in [-1, 1]]):
                            if (row_index - 1, col_index, "3V") not in possibleActions:
                                possibleActions.append((row_index - 1, col_index, "3V"))

                        # bottom piece
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-3, -1), (-3, 0), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-2, -1)]]) \
                            and board.get_value(row_index - 2, col_index) in [" ", "?", "t", "T"] and board.get_value(row_index - 1, col_index) in [" ", "?", "m", "M"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= 3 and all([row_info[row_index + add] + row.count("?") >= 1 for add in [-2, -1]]):
                            if (row_index - 2, col_index, "3V") not in possibleActions:
                                possibleActions.append((row_index - 2, col_index, "3V"))


                        #horizontal
                        # left piece
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, 3), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1), (0, -1)]]) \
                            and board.get_value(row_index, col_index + 1) in [" ", "?", "m", "M"] and board.get_value(row_index, col_index + 2) in [" ", "?", "r", "R"] \
                            and row_info[row_index] + row.count("?") >= 3 and all([col_info[col_index + add] + piece_positions_in_column[col_index + add] >= 1 for add in [1, 2]]):
                            if (row_index, col_index, "3H") not in possibleActions:
                                possibleActions.append((row_index, col_index, "3H"))

                        # middle piece
                        if all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, 2), (1, 2), (1, 1), (1, 0), (1, -1), (1, -2), (0, -2)]]) \
                            and board.get_value(row_index, col_index - 1) in [" ", "?", "l", "L"] and board.get_value(row_index, col_index + 1) in [" ", "?", "r", "R"] \
                            and row_info[row_index] + row.count("?") >= counter and all([col_info[col_index + add] + piece_positions_in_column[col_index + add] >= 1 for add in [-1, 1]]):
                            if (row_index, col_index - 1, "3H") not in possibleActions:
                                possibleActions.append((row_index, col_index - 1, "3H"))

                        # right piece
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -3), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (1, -2), (1, -3), (0, -3)]]) \
                            and board.get_value(row_index, col_index - 2) in [" ", "?", "l", "L"] and board.get_value(row_index, col_index - 1) in [" ", "?", "m", "M"] \
                            and row_info[row_index] + row.count("?") >= 3 and all([col_info[col_index + add] + piece_positions_in_column[col_index + add] >= 1 for add in [-2, -1]]):
                            if (row_index, col_index - 2, "3H") not in possibleActions:
                                possibleActions.append((row_index, col_index - 2, "3H"))

                    if board.unplaced_twos > 0:
                        # vertical 
                        # top
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1 , 1), (2, 1), (2, 0), (2, -1), (1, -1), (0, -1)]]) \
                                and board.get_value(row_index + 1, col_index) in [" ", "?", "b", "B"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= 2 and row_info[row_index] + 1 >= 1:
                            if (row_index, col_index, "2V") not in possibleActions:
                                possibleActions.append((row_index, col_index, "2V"))

                        # bottom
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1 , 1), (2, 1), (2, 0), (2, -1), (1, -1)]]) \
                                and board.get_value(row_index - 1, col_index) in [" ", "?", "t", "T"] \
                            and col_info[col_index] + piece_positions_in_column[col_index] >= 2 and row_info[row_index] - 1 >= 1:
                            if (row_index - 1, col_index, "2V") not in possibleActions:
                                possibleActions.append((row_index - 1, col_index, "2V"))
                        
                        #horizontal
                        # left
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(0, -1), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, 2), (1, 2), (1, 1), (1, 0), (1, -1)]]) \
                                and board.get_value(row_index, col_index + 1) in [" ", "?", "r", "R"] \
                            and row_info[row_index] + row.count("?") >= 2 and col_info[col_index] + piece_positions_in_column[col_index] >= 1:
                            if (row_index, col_index, "2H") not in possibleActions:
                                possibleActions.append((row_index, col_index, "2H"))

                        # right
                        if cell not in ["m", "M"] and all([board.get_value(row_index + check[0], col_index + check[1]) in [".", " ", None, "W"] for check in [(0, 1), (-1, 1), (-1, 0), (-1, -1), (-1, -2), (0, -2), (1, -2), (1, -1), (1, 0), (1, 1)]]) \
                                and board.get_value(row_index, col_index - 1) in [" ", "?", "l", "L"] \
                            and row_info[row_index] + row.count("?") >= 2 and col_info[col_index] + piece_positions_in_column[col_index - 1] >= 1:
                            if (row_index, col_index - 1, "2H") not in possibleActions:
                                possibleActions.append((row_index, col_index - 1, "2H"))


                    if cell not in ["m", "M"] and board.unplaced_ones > 0:
                        if all([board.get_value(x[0], x[1]) in [".", " ", None, "W"] for x in board.get_surroundings(row_index, col_index)]):
                            if (row_index, col_index, "1") not in possibleActions:
                                possibleActions.append((row_index, col_index, "1"))
                    
                    if cell not in ["m", "M"] and row_info[row_index] < row.count(" "):
                        if (row_index, col_index, ".") not in possibleActions:
                            possibleActions.append((row_index, col_index, "."))

        def priority(x):
            if x == '4V' or x == '4H':
                return 1
            elif x == '3V' or x == '3H':
                return 2
            elif x == '2V' or x =='2H':
                return 3
            elif x =='1':
                return 4
            else: # when it is '.'
                return 5
            
        if len(possibleActions) == 0:
            return []

        min_priority = min(priority(tup[2]) for tup in possibleActions)

        filtered_list = [tup for tup in possibleActions if priority(tup[2]) == min_priority]

        ordered_filtered_list = sorted(filtered_list, key=lambda tup: tup[1])

        #print(possibleActions)

        return ordered_filtered_list

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        board = state.board
        
        
        newState = BimaruState(board.copy_board())
        #newState.board.set_value(action[0], action[1], action[2])
        if action[2] == ".":
            newState.board.set_value(action[0], action[1], ".")
        elif action[2] == "1":
            newState.board.place_one(action[0], action[1])
        elif action[2] == "2V":
            newState.board.place_two(action[0], action[1], True)
        elif action[2] == "2H":
            newState.board.place_two(action[0], action[1], False)
        elif action[2] == "3V":
            newState.board.place_three(action[0], action[1], True)
        elif action[2] == "3H":
            newState.board.place_three(action[0], action[1], False)
        elif action[2] == "4V":
            newState.board.place_four(action[0], action[1], True)
        elif action[2] == "4H":
            newState.board.place_four(action[0], action[1], False)

        newState.board.fill_water()
        newState.board.handle_boats()

        return newState


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        ones_left_count = 4
        twos_left_count = 3
        threes_left_count = 2
        fours_left_count = 1
        cells = state.board.cells
        board = state.board

        if any(x != 0 for x in state.board.row_info) or any(x != 0 for x in state.board.col_info):
            #print("1")
            return False
        
        for row_index, row in enumerate(cells):
            for col_index, cell in enumerate(row):
                if cell == "?":
                    #print("2")
                    return False
                if cell in ["c", "C"]:
                    ones_left_count -= 1
                    if not all([board.get_value(x[0], x[1]) in [".", "W", None] for x in board.get_surroundings(row_index, col_index)]):
                        #print("3")
                        return False
                elif cell in ["t", "T"]:
                    if cells[row_index + 1][col_index] in ["b", "B"]:
                        twos_left_count -= 1
                        if not all([board.get_value(row_index + x[0], col_index + x[1]) in [".", "W", None] for x in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (2, 0), (2, -1), (1, -1), (0, -1)]]):
                            #print("4")
                            return False
                    elif cells[row_index + 1][col_index] in ["m", "M"] and cells[row_index + 2][col_index] in ["b", "B"]:
                        threes_left_count -= 1
                        if not all([board.get_value(row_index + x[0], col_index + x[1]) in [".", "W", None] for x in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (3, 0), (3, -1), (2, -1), (1, -1), (0, -1)]]):
                            #print("5")
                            return False
                    elif cells[row_index + 1][col_index] in ["m", "M"] and cells[row_index + 2][col_index] in ["m", "M"] and cells[row_index + 3][col_index] in ["b", "B"]:
                        fours_left_count -= 1
                        if not all([board.get_value(row_index + x[0], col_index + x[1]) in [".", "W", None] for x in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (4, 0), (4, -1), (3, -1), (2, -1), (1, -1), (0, -1)]]):
                            #print("6")
                            return False
                elif cell in ["l", "L"]:
                    if cells[row_index][col_index + 1] in ["r", "R"]:
                        twos_left_count -= 1
                        if not all([board.get_value(row_index + x[0], col_index + x[1]) in [".", "W", None] for x in [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (1, 2), (0, 2), (-1, 2), (-1, 1), (-1, 0)]]):
                            #print("7")
                            return False
                    elif cells[row_index][col_index + 1] in ["m", "M"] and cells[row_index][col_index + 2] in ["r", "R"]:
                        threes_left_count -= 1
                        if not all([board.get_value(row_index + x[0], col_index + x[1]) in [".", "W", None] for x in [(-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (0, 3), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1), (0, -1)]]):
                            #print("8")
                            return False
                    elif cells[row_index][col_index + 1] in ["m", "M"] and cells[row_index][col_index + 2] in ["m", "M"] and cells[row_index][col_index + 3] in ["r", "R"]:
                        fours_left_count -= 1
                        if not all([board.get_value(row_index + x[0], col_index + x[1]) in [".", "W", None] for x in [(-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3), (-1, 4), (0, 4), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0), (1, -1), (0, -1)]]):
                            #print("9")
                            return False
                        
        return ones_left_count == twos_left_count == threes_left_count == fours_left_count == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board().parse_instance()
    board.fill_water()
    board.handle_m_queue()
    board.fill_water()
    board.handle_boats()
    #board.print_board()

    problem = Bimaru(board)
    s0 = problem.initial

    solution = depth_first_tree_search(problem)
    solution.state.board.print_board()

    # s0.board.print_board()
    # print(problem.actions(s0))
    # print(len(problem.actions(s0)))
    # print(problem.goal_test(s0))

    # s1 = problem.result(s0, (0, 4, '4V'))
    # s1.board.print_board()
    # print(problem.actions(s1))
    # print(problem.goal_test(s1))

    # s2 = problem.result(s1, (3, 0, '3H'))
    # s2.board.print_board()
    # print(problem.actions(s2))
    # print(problem.goal_test(s2))

    # [(7, 2, '3V')] why not [(7, 5, '3V')]

    # s0.board.print_board()
    # print(problem.actions(s0))
    # print(len(problem.actions(s0)))
    # print(problem.goal_test(s0))
    # # 
    # s1 = problem.result(s0, (0, 2, '4V'))
    # s1.board.print_board()
    # print(problem.actions(s1))
    # print(len(problem.actions(s1)))
    # print(problem.goal_test(s1))
    

    # s2 = problem.result(s1, (1, 4, '3H'))
    # s2.board.print_board()
    # print(problem.actions(s2))
    # print(problem.goal_test(s2))

    # s3 = problem.result(s2, (1, 4, '3H'))
    # s3.board.print_board()
    # print(problem.actions(s3))
    # print(problem.goal_test(s3))

    # s4 = problem.result(s3, (3, 4, '2H'))
    # s4.board.print_board()
    # print(problem.actions(s4))
    # print(problem.goal_test(s4))

    # s5 = problem.result(s4, (8, 7, '2H'))
    # s5.board.print_board()
    # print(problem.actions(s5))
    # print(problem.goal_test(s5))

    # s6 = problem.result(s5, (5, 1, '.'))
    # s6.board.print_board()
    # print(problem.actions(s6))
    # print(problem.goal_test(s6))