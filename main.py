#main.py

import pygame as pg
import sys
import map
import game

# Initialize
pg.init()

# Display
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Portal 2D")

# Create the map
game_map = map.Map(width, height)  # Adjust as needed


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Fonts
font = pg.font.Font(None, 36)

# Create buttons
def draw_button(x, y, width, height, text, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pg.draw.rect(screen, white, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pg.draw.rect(screen, blue, (x, y, width, height))

    button_text = font.render(text, True, black)
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)

# Start the game
def start_game():
    print("starting game...")
    main_game = game.Game()
    main_game.loop()

# Exit the program
def exit_game():
    pg.quit()
    sys.exit()

# Main
clock = pg.time.Clock()
FPS = 60

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(black)

    # Draw buttons
    button_width, button_height = 200, 50
    start_button_x, start_button_y = (width - button_width) // 2, height // 2 - 50
    exit_button_x, exit_button_y = (width - button_width) // 2, height // 2 + 50

    draw_button(start_button_x, start_button_y, button_width, button_height, "Start", start_game)
    draw_button(exit_button_x, exit_button_y, button_width, button_height, "Exit", exit_game)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()