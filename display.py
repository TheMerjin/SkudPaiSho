import pygame
import tile
from env import Game
from move import Move
import random
from board import tile_type_to_images


# Constants
WIDTH, HEIGHT = 760, 760
ROWS, COLS = 19, 19
TILE_GAP = WIDTH // (COLS - 1)  # distance between intersections
DOT_RADIUS = 6

# Colors
NEUTRAL_COLOR = (178, 200, 186)
RED_COLOR = (162, 62, 72)
WHITE_COLOR = (234, 221, 196)
BG_COLOR = (40, 40, 40)

images = {
    i: pygame.transform.scale(pygame.image.load(v), (TILE_GAP // 1.5, TILE_GAP // 1.5))
    for i, v in tile_type_to_images.items()
}


def get_color(val):
    if val == 0:
        return NEUTRAL_COLOR
    elif val == 1:
        return RED_COLOR
    elif val == 2:
        return WHITE_COLOR
    else:
        return None  # Off-board


def scale_coords(coords):
    return [(x * TILE_GAP, y * TILE_GAP) for (x, y) in coords]


def draw_board(win, board_data):
    win.fill(BG_COLOR)
    red_triangles = [
        [(2, 9), (9, 9), (9, 16)],
        [(9, 2), (9, 9), (16, 9)],
    ]
    white_triangles = [
        [(2, 9), (9, 9), (9, 2)],
        [(9, 16), (9, 9), (16, 9)],
    ]
    for triangle in red_triangles:
        pygame.draw.polygon(win, (255, 0, 0), scale_coords(triangle))

    # Draw white triangles
    for triangle in white_triangles:
        pygame.draw.polygon(win, (255, 255, 255), scale_coords(triangle))
    # Draw grid lines
    for i in range(ROWS):
        x = i * TILE_GAP
        pygame.draw.line(win, (100, 100, 100), (x, 0), (x, HEIGHT))
        pygame.draw.line(win, (100, 100, 100), (0, x), (WIDTH, x))
    for row in range(ROWS):
        for col in range(COLS):
            val = board_data.copy_of_board[row][col]
            if val == -1:
                continue
            if isinstance(val, tile.PaiShoTile):
                pass
            color = get_color(val)

            if color:
                x = col * TILE_GAP
                y = row * TILE_GAP
                pygame.draw.circle(win, color, (x, y), DOT_RADIUS)

    # Draw intersections
    for row in range(ROWS):
        for col in range(COLS):
            val = board_data.board[row][col]
            if val == -1:
                continue
            if isinstance(val, tile.PaiShoTile):
                win.blit(
                    images[val.tile_type],
                    (col * TILE_GAP - TILE_GAP // 3, row * TILE_GAP - TILE_GAP // 3),
                )  # skip off-board


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pai Sho Intersections")
    game = Game()
    board = game.board
    piece1 = tile.AccentTile(tile_type="guest_wheel", color=0, position=(None, None))
    piece2 = tile.FlowerTile(tile_type="host_red_three", color=0, position=(None, None))
    move_index = -1
    legal_moves = []
    showing_moves = False
    running = True
    while running:
        draw_board(win, board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                game.play_move(
                    Move(
                        start=None,
                        end=(7, 12),
                        board=board,
                        piece=piece1,
                    )
                )
                game.play_move(
                    Move(
                        start=None,
                        end=(8, 4),
                        board=board,
                        piece=piece2,
                    )
                )

            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                legal_moves = game.generate_legal_moves(game.board, game.guest_to_play)
                game.play_move(random.choice(legal_moves))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                print("monkey")
                game.undo_move()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                piece3 = tile.AccentTile(
                    tile_type="guest_wheel", color=0, position=(None, None)
                )
                x = 5
                y = 8
                game.play_move(
                    Move(
                        start=(8, 4),
                        end=(8, 4),
                        board=board,
                        piece=piece1,
                        harmony=True,
                        accent_or_special_tile=piece3,
                        accent_pos=(y, x),
                    )
                )

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if not showing_moves:
                    legal_moves = game.generate_legal_moves(
                        game.board, game.guest_to_play
                    )
                    move_index = -1
                    showing_moves = True
                else:
                    if move_index >= 0:
                        game.undo_move()
                    move_index += 1
                    if move_index < len(legal_moves):
                        move = legal_moves[move_index]
                        game.play_move(move)
                        print("Showing move:", move)
                    else:
                        print("Finished showing all legal moves.")
                        showing_moves = False
                        move_index = -1

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
