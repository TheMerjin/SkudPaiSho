"We create the general game enviornment for tracking the state"

from board import PaiShoBoard
from move import Move
from tile import PaiShoTile


class Game:
    "This creates the actual game state"

    def __init__(self):
        self.board = PaiShoBoard()
        guest_normal_tiles = (
            [PaiShoTile("geust_red_three", 1) for _ in range(4)]
            + [PaiShoTile("geust_red_four", 1) for _ in range(4)]
            + [PaiShoTile("geust_red_five", 1) for _ in range(4)]
            + [PaiShoTile("geust_white_three", 1) for _ in range(4)]
            + [PaiShoTile("geust_white_four", 1) for _ in range(4)]
            + [PaiShoTile("geust_white_five", 1) for _ in range(4)]
        )

        # Guest Normal Tiles
        host_normal_tiles = (
            [PaiShoTile("host_red_three", 1) for _ in range(4)]
            + [PaiShoTile("host_red_four", 1) for _ in range(4)]
            + [PaiShoTile("host_red_five", 1) for _ in range(4)]
            + [PaiShoTile("host_white_three", 1) for _ in range(4)]
            + [PaiShoTile("host_white_four", 1) for _ in range(4)]
            + [PaiShoTile("host_white_five", 1) for _ in range(4)]
        )
        host_accent_tiles = [PaiShoTile("host_boat", 1)]

        # Guest Accent Tiles
        guest_accent_tiles = [PaiShoTile("boat", 1)]

        host_special_tiles = [
            PaiShoTile("host_lotus", 1),
            PaiShoTile("host_orchid", 1),
        ]

        # Guest Special Tiles
        guest_special_tiles = [
            PaiShoTile("guest_lotus", 1),
            PaiShoTile("guest_orchid", 1),
        ]
        self.host_pieces = host_normal_tiles + host_accent_tiles + host_special_tiles
        self.guest_pieces = (
            guest_normal_tiles + guest_accent_tiles + guest_special_tiles
        )
        self.geust_to_play = True
        self.move_log = []

    def play_move(self, move):
        if move.is_placement:
            self.board.board[move.end_row][move.end_col] = move.piece_moved
            move.piece_moved.position = (move.end_row, move.end_col)
            self.geust_to_play = not self.geust_to_play
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
            self.geust_to_play = not self.geust_to_play

    def generate_legal_moves(self, board, host_or_geust):
        legal_moves = []
