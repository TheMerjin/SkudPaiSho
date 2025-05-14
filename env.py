"We create the general game enviornment for tracking the state"

from board import PaiShoBoard
from move import Move
from tile import PaiShoTile, FlowerTile, AccentTile, SpecialTile


class Game:
    "This creates the actual game state"

    def __init__(self):
        self.board = PaiShoBoard()
        self.guest_normal_tiles = (
            [FlowerTile("guest_red_three", 0) for _ in range(3)]
            + [FlowerTile("guest_red_four", 0) for _ in range(3)]
            + [FlowerTile("guest_red_five", 0) for _ in range(3)]
            + [FlowerTile("guest_white_three", 1) for _ in range(3)]
            + [FlowerTile("guest_white_four", 1) for _ in range(3)]
            + [FlowerTile("guest_white_five", 1) for _ in range(3)]
        )

        # Guest Normal Tiles
        self.host_normal_tiles = (
            [FlowerTile("host_red_three", 0) for _ in range(3)]
            + [FlowerTile("host_red_four", 0) for _ in range(3)]
            + [FlowerTile("host_red_five", 0) for _ in range(3)]
            + [FlowerTile("host_white_three", 1) for _ in range(3)]
            + [FlowerTile("host_white_four", 1) for _ in range(3)]
            + [FlowerTile("host_white_five", 1) for _ in range(3)]
        )
        self.host_accent_tiles = [AccentTile("host_boat", None)]

        # Guest Accent Tiles
        self.guest_accent_tiles = [AccentTile("guest_boat", None)]

        self.host_special_tiles = [
            PaiShoTile("host_lotus", None),
            PaiShoTile("host_orchid", None),
        ]

        # Guest Special Tiles
        self.guest_special_tiles = [
            PaiShoTile("guest_lotus", None),
            PaiShoTile("guest_orchid", None),
        ]

        self.host_pieces = (
            self.host_normal_tiles + self.host_accent_tiles + self.host_special_tiles
        )
        self.guest_pieces = (
            self.guest_normal_tiles + self.guest_accent_tiles + self.guest_special_tiles
        )
        self.guest_to_play = True
        self.move_log = []
        self.generate_legal_moves(self.board, self.guest_to_play)
        self.base_harmony_map = {
            "red_three": ["red_four", "white_five"],
            "red_four": ["red_three", "red_five"],
            "red_five": ["red_four", "white_three", "white_four"],
            "white_three": ["red_five", "white_four"],
            "white_four": ["white_three", "white_five"],
            "white_five": ["white_four", "red_three"],
        }
        self.harmony_map = {}

        for base_color, harmonies in self.base_harmony_map.items():
            for prefix in ["host_", "guest_"]:
                key = prefix + base_color
                self.harmony_map[key] = [prefix + h for h in harmonies]

        self.base_disharmony_map = {
            "red_three": ["white_three"],
            "red_four": ["white_four"],
            "red_five": ["white_five"],
            "white_three": ["red_three"],
            "white_four": ["red_four"],
            "white_five": ["red_five"],
        }

        self.disharmony_map = {}

        for base_color, disharmonies in self.base_disharmony_map.items():
            for prefix in ["host_", "guest_"]:
                key = prefix + base_color
                self.disharmony_map[key] = [
                    ("host_" if prefix == "guest_" else "guest_") + d
                    for d in disharmonies
                ]

    def play_move(self, move):
        self.move_log.append(move)
        if move.is_placement:
            self.board.board[move.end_row][move.end_col] = move.piece_moved
            move.piece_moved.position = (move.end_row, move.end_col)
            self.guest_to_play = not self.guest_to_play
        else:
            self.board.board[move.end_row][move.end_col] = move.piece_moved
            self.board.board[move.start_row][move.start_col] = self.board.copy_of_board[
                move.start_row
            ][move.start_col]
            if move.harmony:
                self.board.board[move.accent_pos[0]][
                    move.accent_pos[1]
                ] = move.accent_tile
            move.piece_moved.position = (move.end_row, move.end_col)
            self.guest_to_play = not self.guest_to_play

    def undo_move(self):
        move = self.move_log.pop()
        self.geust_to_play = not self.guest_to_play

        if move.is_placement:
            move.piece_moved.position = (None, None)
            self.board.board[move.end_row][move.end_col] = self.board.copy_of_board[
                move.end_row
            ][move.end_col]

        else:
            self.board.board[move.end_row][move.end_col] = self.board.copy_of_board[
                move.start_row
            ][move.start_col]
            self.board.board[move.start_row][move.start_col] = move.piece_moved
            if move.harmony:
                self.board.board[move.accent_pos[0]][move.accent_pos[1]] = (
                    self.board.copy_of_board[move.accent_pos[0]][move.accent_pos[1]]
                )
            move.piece_moved.position = (move.start_row, move.start_col)

    def generate_legal_moves(self, board, guest_to_play):
        legal_moves = []
        pieces = self.guest_pieces if guest_to_play else self.host_pieces
        normal_pieces = (
            self.guest_normal_tiles if guest_to_play else self.host_normal_tiles
        )
        gardens = self.board.get_gardens()
        print(
            f"The move log {self.move_log} and mt of previous moves : {len(self.move_log)}"
        )
        for i, j in gardens.items():
            if isinstance(j, int):
                for piecej in normal_pieces:
                    legal_moves.append(
                        Move(
                            start=None,
                            end=i,
                            board=board,
                            piece=piecej,
                        )
                    )

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        opposite_colors = {0: None, 1: 2, 2: 1}
        for row in self.board.board:
            for current_piece in row:
                if isinstance(current_piece, FlowerTile):
                    if current_piece.is_guest == guest_to_play:
                        move_distance = current_piece.move_distance
                        color = current_piece.color
                        opposite_color = opposite_colors[color]
                        piece_pos = current_piece.position
                        opposite_tile_type = self.disharmony_map[
                            current_piece.tile_type
                        ]
                        x, y = piece_pos
                        paths = []
                        for i in range(1, move_distance + 1):
                            paths.extend(
                                generate_all_cardinal_paths(
                                    x,
                                    y,
                                    self.board.board,
                                    max_steps=i,
                                    opposite_color=opposite_color,
                                    opposite_tile_type=opposite_tile_type,
                                )
                            )
                        unique_paths = self.get_unique_paths(paths)
                        legal_moves.extend(
                            [
                                Move(
                                    start=piece_pos,
                                    end=i[-1],
                                    board=self.board,
                                    piece=current_piece,
                                )
                                for i in unique_paths
                            ]
                        )
        return legal_moves

    def get_unique_paths(self, paths):
        seen_end_pts = []
        unique_paths = []
        for path in paths:
            if path[-1] not in seen_end_pts:
                seen_end_pts.append(path[-1])
                unique_paths.append(path)
        return unique_paths


def generate_all_cardinal_paths(
    start_x, start_y, board, max_steps=3, opposite_color=None, opposite_tile_type=None
):
    board_size = len(board)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # U, D, L, R
    all_paths = []

    def dfs(x, y, path, depth):
        if depth == max_steps:
            final_pos = path[-1]
            row, col = final_pos
            for piece in board[row]:
                if (
                    isinstance(piece, FlowerTile)
                    and piece.tile_type in opposite_tile_type
                ):
                    return

            for row in board:
                piece = row[col]
                if isinstance(piece, FlowerTile):
                    if piece.tile_type in opposite_tile_type:
                        return

            all_paths.append(path[:])

            return

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < board_size
                and 0 <= ny < board_size
                and board[nx][ny] != -1
                and (nx, ny) not in path
                and not isinstance(board[nx][ny], PaiShoTile)
                and board[nx][ny] != opposite_color
            ):
                path.append((nx, ny))
                dfs(nx, ny, path, depth + 1)
                path.pop()

    dfs(start_x, start_y, [], 0)
    return all_paths
