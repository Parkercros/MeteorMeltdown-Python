import pygame
import sys
from asteroid_game import asteroid_game
from painting_program import painting_program

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 1600, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('App Menu')

# Load background image
background_image = pygame.image.load("background2.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Fonts
pygame.font.init()
font = pygame.font.Font(None, 36)

def draw_button(text, x, y, width, height, active_color, inactive_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))

        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the screen with the background image
        screen.blit(background_image, (0, 0))

        # Draw buttons
        button_width = 250
        button_height = 50
        button_spacing = 50

        button_x_start = (WIDTH - button_width * 2 - button_spacing) / 2

        if draw_button("Start Game", button_x_start, 340, button_width, button_height, (75, 119, 190), (98, 164, 229)):
            asteroid_game()

        if draw_button("Create Character", button_x_start + button_width + button_spacing, 340, button_width, button_height, (75, 119, 190), (98, 164, 229)):
            painting_program()

        if draw_button("Exit", button_x_start + (button_width + button_spacing) / 2, 900, button_width, button_height, (75, 119, 190), (98, 164, 229)):
            pygame.quit()
            sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
