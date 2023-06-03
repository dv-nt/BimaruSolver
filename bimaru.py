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
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np


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
        self.unknwon_boats = []
        self.middle_pieces = []

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
                self.unknwon_boats.append((row, col))
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
        surroundings = [(-1, -1), (-1, 0), (-1, -1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
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
            if self.row_info[row_index] == self.cells[row_index].count(" ") != 0:
                    changed = True
                    for col_index, col in enumerate(row):
                        if self.get_value(row_index, col_index) == " ":
                            self.set_value(row_index, col_index, "?")

        for col_index in range(len(self.cells[0])):
            col_values = [self.get_value(row_index, col_index) for row_index in range(len(self.cells))]
            if self.col_info[col_index] == col_values.count(" ") != 0:
                changed = True
                for row_index in range(len(self.cells)):
                    if self.get_value(row_index, col_index) == " ":
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
                    
        for boat in self.unknwon_boats:
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
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        board = state.board

        cells = board.cells
        row_info = board.row_info
        col_info = board.col_info

        possibleActions = []

        for row_index, row in enumerate(cells):
            for col_index, cell in enumerate(row):
                pass

        return possibleActions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        board = state.board
        board.set_value(action[0], action[1], action[2])
        
        newState = BimaruState(board)
        # newState.cells = board.cells
        # newState.row_info = board.row_info
        # newState.col_info = board.col_info
        # newState.unplaced_ones = board.unplaced_ones
        # newState.unplaced_twos = board.unplaced_twos
        # newState.unplaced_threes = board.unplaced_threes
        # newState.unplaced_fours = board.unplaced_fours
        # newState.to_run_m_hints = board.to_run_m_hints
        # newState.unknwon_boats = board.unknwon_boats
        # newState.middle_pieces = board.middle_pieces

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

        if any(x != 0 for x in state.board.row_info) or any(x != 0 for x in state.board.col_info):
            return False
        
        for row_index, row in enumerate(cells):
            for col_index, cell in enumerate(row):
                if cell == "?":
                    return False
                if cell in ["c", "C"]:
                    ones_left_count -= 1
                elif cell in ["t", "T"]:
                    if cells[row_index + 1][col_index] in ["b", "B"]:
                        twos_left_count -= 1
                    elif cells[row_index + 1][col_index] in ["m", "M"] and cells[row_index + 2][col_index] in ["b", "B"]:
                        threes_left_count -= 1
                    elif cells[row_index + 1][col_index] in ["m", "M"] and cells[row_index + 2][col_index] in ["m", "M"] and cells[row_index + 3][col_index] in ["b", "B"]:
                        fours_left_count -= 1
                elif cell in ["l", "L"]:
                    if cells[row_index][col_index + 1] in ["r", "R"]:
                        twos_left_count -= 1
                    elif cells[row_index][col_index + 1] in ["m", "M"] and cells[row_index][col_index + 2] in ["r", "R"]:
                        threes_left_count -= 1
                    elif cells[row_index][col_index + 1] in ["m", "M"] and cells[row_index][col_index + 2] in ["m", "M"] and cells[row_index][col_index + 3] in ["r", "R"]:
                        fours_left_count -= 1

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
    problem = Bimaru(Board)
    s0 = BimaruState(board)
    print(s0.board.print_board())
    print("Is goal?", problem.goal_test(s0))

    # board = Board.parse_instance()
    # problem = Bimaru(board)

    # s0 = BimaruState(board)

    # s1 = problem.result(s0, (0, 1, "w"))
    # s2 = problem.result(s1, (1, 1, "w"))
    # s3 = problem.result(s2, (1, 0, "b"))
    # s4 = problem.result(s3, (2, 0, "w"))
    # s5 = problem.result(s4, (2, 1, "w"))

    # print("Is goal?", problem.goal_test(s5))