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

    def set_value(self, row: int, col: int, value: str):
        """Atribui o valor na respetiva posição do tabuleiro."""
        if row >= 0 and row <= 9 and col >= 0 and col <= 9:
            if value not in ["W", "."]:
                self.row_info[row] = self.row_info[row] - 1
                self.col_info[col] = self.col_info[col] - 1
            self.cells[row][col] = value

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
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
        print("a")
        
        print(self.get_value(row, col - 1))

        print(self.get_value(row + 1, col))
        print(self.get_value(row - 1, col))
        print(self.get_value(row, col + 1))
        print(self.get_value(row, col - 1))


        if self.is_water(row + 1, col) or self.is_water(row - 1, col):
            print("horziontal")
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
            print("vertical")
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

        self.check_boats(True)

    def check_boats(self, from_fill_water=False):
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
            self.check_boats()

        if not from_fill_water:
            self.fill_water()

    def handle_m_queue(self):
        for hint in board.to_run_m_hints:
            board.m_hint(hint[0], hint[1])

    def print_board(self):
        print("  " + " ".join([str(x) for x in self.col_info]))
        for i in range(len(self.cells)):
            print(str(self.row_info[i]) + " " + " ".join(self.cells[i]))

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

        if int(hint_info[0]) < 1:
            return "no hints"

        for hint in range(int(hint_info[0])):
            hintLine = stdin.readline().split()
            print("hint #" + str(hint) + "   " + " ".join(hintLine))
            print(hintLine[1])
            print(hintLine[2])
            print(hintLine[3])
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
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

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
    board.print_board()
    
    # print(board.adjacent_vertical_values(3, 3))
    # print(board.adjacent_horizontal_values(3, 3))

    # print(board.adjacent_vertical_values(1, 0))
    # print(board.adjacent_horizontal_values(1, 0))
