"here we initialize the board and allow for display using plot just to make sure"

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import tile

tile_type_to_images = {
    "host_boat": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HB.png",
    "geust_boat": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GB.png",
    "host_lotus": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HL.png",
    "guest_lotus": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GL.png",
    "host_orchid": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HO.png",
    "guest_orchid": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GO.png",
    "host_red_three": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HR3.png",
    "host_red_four": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HR4.png",
    "host_red_five": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HR5.png",
    "guest_red_three": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GR3.png",
    "guest_red_four": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GR4.png",
    "guest_red_five": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GR5.png",
    "host_white_three": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HW3.png",
    "host_white_four": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HW4.png",
    "host_white_five": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\HW5.png",
    "guest_white_three": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GW3.png",
    "guest_white_four": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GW4.png",
    "guest_white_five": r"C:\Users\Sreek\OneDrive\Pai-sho\images\tggproject\GW5.png",
}


class PaiShoBoard:
    """here is the actual board => the board can be printed
    and plotted it
    is 19 by 19 for all the
    intersections possible.
    The center is accesed by
    (row = 9, col = 9)
    the red intersections
    (where only red tiles can go are 1, white are 2 ;-1 is off board and 0
    is neutral board spaces)"""

    def __init__(self):
        # Create an 18x18 grid filled with periods (".")
        self.board = [[0 for _ in range(19)] for _ in range(19)]
        self.fix_board()
        self.copy_of_board = [row[:] for row in self.board]

    def fix_board(self):
        # We'll consider the center to be (8.5,8.5) in 0-based indexing
        # so that the "circle" is roughly centered. Adjust radius as needed.
        center = 9
        radius = 9

        for row in range(19):
            for col in range(19):
                # Distance from (row, col) to the center
                dist = math.sqrt((row - center) ** 2 + (col - center) ** 2)
                # If outside the circle boundary, set to -1
                if dist > radius:
                    self.board[row][col] = -1

        self.board[0][9] = -1
        self.board[9][0] = -1
        self.board[9][18] = -1
        self.board[18][9] = -1
        for row in range(19):
            for col in range(19):
                if row > 9 and col > 9:
                    if (row + col) < 25:
                        self.board[row][col] = 2
                if row < 9 and col < 9 and (row + col) > 11:
                    self.board[row][col] = 2
                if row < 9 and col > 9 and (col - row) < 7:
                    self.board[row][col] = 1
                if row > 9 and col < 9 and (row - col) < 7:
                    self.board[row][col] = 1

    def print_board(self, board):
        for row in board:
            print(" ".join([str(s) if s == -1 else str(s) + " " for s in row]))


def plot_board(board):

    fig, ax = plt.subplots(figsize=(6, 6))

    # Color mapping
    bg_colors = {
        0: "#B2C8BA",  # green-grey
        1: "#A23E48",  # deep red
        2: "#EADDC4",  # pale beige
    }

    # Draw colored tiles
    for i in range(19):
        for j in range(19):
            val = board.copy_of_board[i][j]
            if isinstance(val, tile.FlowerTile):
                print("problem")
            if val != -1:
                ax.add_patch(
                    plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color=bg_colors[val])
                )

    # Draw intersection points
    for i in range(19):
        for j in range(19):
            val = board.board[i][j]
            if val == 0:
                ax.plot(j, i, "o", color="black", markersize=4)
            elif val == 1:
                ax.plot(j, i, "o", color="red", markersize=4)
            elif val == 2:
                ax.plot(j, i, "o", color="white", markersize=4)
            elif val == -1:
                pass
            else:
                image = mpimg.imread(tile_type_to_images[val.tile_type])
                oi = OffsetImage(image, zoom=0.05)
                ab = AnnotationBbox(oi, (j, i), frameon=False)
                ax.add_artist(ab)

    # Grid lines
    for i in range(19):
        ax.plot([0, 18], [i, i], color="grey", linewidth=0.5)
        ax.plot([i, i], [0, 18], color="grey", linewidth=0.5)

    red_triangles = [
        # Top-right quadrant (red zone)
        # Bottom-left quadrant (red zone)
        [(2, 9), (9, 9), (9, 16)],
        [(9, 2), (9, 9), (16, 9)],
    ]
    white_triangles = [
        # Top-right quadrant (red zone)
        # Bottom-left quadrant (red zone)
        [(2, 9), (9, 9), (9, 2)],
        [(9, 16), (9, 9), (16, 9)],
    ]
    for triangle in white_triangles:
        patch = patches.Polygon(triangle, closed=True, color="grey", alpha=0.5)
        ax.add_patch(patch)

    for triangle in red_triangles:
        patch = patches.Polygon(triangle, closed=True, color="red", alpha=0.5)
        ax.add_patch(patch)

    ax.set_xlim(-1, 18)
    ax.set_ylim(-1, 18)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Skud Pai Sho Intersections (18x18)")
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    pai_sho_board = PaiShoBoard()
    pai_sho_board.print_board(pai_sho_board.copy_of_board)
    plot_board(pai_sho_board)
