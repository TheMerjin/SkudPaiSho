"We create the general game enviornment for tracking the state"

from board import PaiShoBoard
from move import Move
from tile import PaiShoTile


class Game:
    "This creates the actual game state"

    def __init__(self):
        self.board = PaiShoBoard()
        self.guest_normal_tiles = (
            [PaiShoTile("geust_red_three", 1) for _ in range(3)]
            + [PaiShoTile("geust_red_four", 1) for _ in range(3)]
            + [PaiShoTile("geust_red_five", 1) for _ in range(3)]
            + [PaiShoTile("geust_white_three", 1) for _ in range(3)]
            + [PaiShoTile("geust_white_four", 1) for _ in range(3)]
            + [PaiShoTile("geust_white_five", 1) for _ in range(3)]
        )

        # Guest Normal Tiles
        self.host_normal_tiles = (
            [PaiShoTile("host_red_three", 1) for _ in range(3)]
            + [PaiShoTile("host_red_four", 1) for _ in range(3)]
            + [PaiShoTile("host_red_five", 1) for _ in range(3)]
            + [PaiShoTile("host_white_three", 1) for _ in range(3)]
            + [PaiShoTile("host_white_four", 1) for _ in range(3)]
            + [PaiShoTile("host_white_five", 1) for _ in range(3)]
        )
        self.host_accent_tiles = [PaiShoTile("host_boat", 1)]

        # Guest Accent Tiles
        self.guest_accent_tiles = [PaiShoTile("guest_boat", 1)]

        self.host_special_tiles = [
            PaiShoTile("host_lotus", 1),
            PaiShoTile("host_orchid", 1),
        ]

        # Guest Special Tiles
        self.guest_special_tiles = [
            PaiShoTile("guest_lotus", 1),
            PaiShoTile("guest_orchid", 1),
        ]

        self.host_pieces = (
            self.host_normal_tiles + self.host_accent_tiles + self.host_special_tiles
        )
        self.guest_pieces = (
            self.guest_normal_tiles + self.guest_accent_tiles + self.guest_special_tiles
        )
        self.geust_to_play = True
        self.move_log = []
        self.generate_legal_moves(self.board, self.geust_to_play)

    def play_move(self, move):
        if move.is_placement:
            self.board.board[move.end_row][move.end_col] = move.piece_moved
            move.piece_moved.position = (move.end_row, move.end_col)
            self.geust_to_play = not self.geust_to_play
            self.generate_legal_moves(self.board, self.geust_to_play)
        else:
            self.board.board[move.end_row][move.end_col] = move.piece_moved
            self.board.board[move.start_row][move.start_col] = self.board.copy_of_board[
                move.start_row
            ][move.start_col]
            if move.harmony:
                self.board.board[move.accent_pos[1]][
                    move.accent_pos[0]
                ] = move.accent_tile
            move.piece_moved.position = (move.end_row, move.end_col)
            self.geust_to_play = not self.geust_to_play
            self.generate_legal_moves(self.board, self.geust_to_play)

    def generate_legal_moves(self, board, guest_to_play):
        legal_moves = []
        pieces = self.guest_pieces if self.geust_to_play else self.host_pieces
        normal_pieces = (
            self.guest_normal_tiles if self.geust_to_play else self.host_normal_tiles
        )
        gardens = self.board.get_gardens()
        print(gardens)
        for i, j in gardens.items():
            if j == -1:
                for piecej in normal_pieces:
                    legal_moves.append(
                        Move(
                            start=None,
                            end=(9, 18),
                            board=board,
                            piece=piecej,
                        )
                    )
        print("legal moves: ", len(legal_moves))
