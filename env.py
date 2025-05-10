"We create the general game enviornment for tracking the state"

from board import PaiShoBoard
from move import Move


class Game:
    "This creates the actual game state"

    def __init__(self):
        self.board = PaiShoBoard()
        self.host_pieces = []
        self.guest_pieces = []
        self.geust_to_play = True
        self.move_log = []

    def play_move(self, move):
        if move.is_placement:
            self.board.board[move.end_row][move.end_col] = move.piece_moved
            move.piece_moved.position = (move.end_row, move.end_col)
        else:
            print(move.piece_moved)
            print(move.start_col, move.start_row)
            print(f"end_col { move.end_col} and end_row: {move.end_row}")
            self.board.board[move.end_row][move.end_col] = move.piece_moved
            self.board.board[move.start_row][move.start_col] = 0
            if move.harmony:
                self.board.board[move.accent_pos[1]][
                    move.accent_pos[0]
                ] = move.accent_tile
            move.piece_moved.position = (move.end_row, move.end_col)

    def generate_legal_moves(self):
        pass
