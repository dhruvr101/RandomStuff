from typing import List, Tuple

# Unit 3 Project: Wolves and Dens Puzzle Solver
# **************************************
# Wolves and Dens is a grid logic puzzle where a user is presented with a grid of dens, and players
# use counts of wolves in each row and column to determine how to place wolves next to each den.
# 
# Here are the puzzle rules:
#   -Each wolf must be adjacent to a den horizontally or vertically. 
#   -Each den supports one wolf, so you should assume a 1:1 mapping between wolf and den.
#   -Wolves cannot touch each other in any direction (horizontally, vertically, or diagonally).(They get
#    a little territorial;))
#   -Users are given the number of wolves that exist in each row or column.
#
# Use recursive backtracking to implement a solver that determines the solution to a given puzzle.

class WolvesAndDens():

    EMPTY_SPACE = " "
    WOLF = "W"
    DEN = "D"

    def __init__(self, row_wolf_count: List[int], column_wolf_count: List[int], dens: List[Tuple[int, int]]) -> None:
        self.row_wolf_count = row_wolf_count[:]
        self.column_wolf_count = column_wolf_count[:]
        self.dens = dens
        self.size = len(self.row_wolf_count)
        self.board = [[self.EMPTY_SPACE for _ in range(self.size)] for _ in range(self.size)]

        for row, col in self.dens:
            self.board[row][col] = self.DEN

    
    def check_if_passes(self) -> bool:
        for count in self.row_wolf_count:
            if count != 0:
                return False
        for count in self.column_wolf_count:
            if count != 0:
                return False
        return True

    def can_you_place_wolf(self,row: int, col: int) -> bool:
        if row >= len(self.row_wolf_count) or col >= len(self.column_wolf_count):
            return False

        if self.board[row][col] != self.EMPTY_SPACE:
            return False
        
        if self.row_wolf_count[row] <= 0 or self.column_wolf_count[col] <= 0:
            return False

        all_Next_Den_Positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        valid_Next_Den_Positions = [(r, c) for r, c in all_Next_Den_Positions if 0 <= r < self.size and 0 <= c < self.size]

        if not any(self.board[r][c] == self.DEN for r, c in valid_Next_Den_Positions):
            return False


        next_To_Wolf_Positions = [
            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
            (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)
        ]
        if any(0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.WOLF for r, c in next_To_Wolf_Positions):
            return False

        return True

    def place_Wolf(self,row: int, col: int) -> None:
        self.board[row][col] = self.WOLF
        self.row_wolf_count[row] = self.row_wolf_count[row] -1
        self.column_wolf_count[col] = self.column_wolf_count[col] - 1

    def remove_Wolf(self,row: int, col: int) -> None:
        self.board[row][col] = self.EMPTY_SPACE
        self.row_wolf_count[row] = self.row_wolf_count[row] + 1
        self.column_wolf_count[col] = self.column_wolf_count[col] + 1



    def solve(self) -> List[List[str]]:
        def backtrack_Function(den_index: int) -> bool:
            if den_index == len(self.dens):
                return self.check_if_passes()

            row, col = self.dens[den_index]
            wolf_placements = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            valid_wolf_placements = [(r, c) for r, c in wolf_placements if 0 <= r < self.size and 0 <= c < self.size]

            for r, c in valid_wolf_placements:
                if self.can_you_place_wolf(r, c):
                    self.place_Wolf(r, c)
                    if backtrack_Function(den_index + 1):
                        return True
                    self.remove_Wolf(r, c)

            return False

        if backtrack_Function(0):
            final_board = self.board
            return final_board
        else:
            return None
