import pygame
import sys
# Initialize
pygame.init()

# Display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Portal 2D")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Create buttons
def draw_button(x, y, width, height, text, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, white, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, blue, (x, y, width, height))

    button_text = font.render(text, True, black)
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)

# Start the game
def start_game():
    print("starting game...")
    #import ___
    #___.main

# Exit the program
def exit_game():
    pygame.quit()
    sys.exit()

# Main
clock = pygame.time.Clock()
FPS = 60

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    # Draw buttons
    button_width, button_height = 200, 50
    start_button_x, start_button_y = (width - button_width) // 2, height // 2 - 50
    exit_button_x, exit_button_y = (width - button_width) // 2, height // 2 + 50

    draw_button(start_button_x, start_button_y, button_width, button_height, "Start", start_game)
    draw_button(exit_button_x, exit_button_y, button_width, button_height, "Exit", exit_game)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()