"""Here we define our Move Class"""


class Move:
    def __init__(
        self,
        start,
        end,
        board,
        piece,
        harmony=False,
        accent_or_special_tile=None,
        accent_pos=None,
    ):
        self.is_placement = (
            start is None
        )  # If there's no start square, it's a placement
        if self.is_placement:
            self.start_pos = None
            self.start_col = None
            self.start_row = None
            self.end_pos = end
            self.end_col = self.end_pos[1]
            self.end_row = self.end_pos[0]
            self.piece_moved = piece
            self.piece_placed = board.board[end[0]][
                end[1]
            ]  # Assuming the board already has the tile there
        else:
            self.piece = piece
            self.start_pos = start
            self.start_col = start[1]
            self.start_row = start[0]
            self.end_pos = end
            self.end_col = self.end_pos[1]
            self.end_row = self.end_pos[0]
            self.piece_moved = board.board[start[0]][start[1]]
            self.piece_captured = board.board[end[0]][end[1]]
            self.harmony = harmony
            self.accent_tile = accent_or_special_tile
            self.accent_pos = accent_pos

        self.move_id = (start, end) if not self.is_placement else ("placement", end)

    def __eq__(self, other):
        return self.move_id == other.move_id
