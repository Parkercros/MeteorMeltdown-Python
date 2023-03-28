import pygame
import sys
from asteroid_game import asteroid_game
from painting_program import painting_program
from moviepy.editor import VideoFileClip


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 1600, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('App Menu')


video_clip = VideoFileClip("assets/rocks.mp4")
video_clip = video_clip.resize((WIDTH, HEIGHT))


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
    clock = pygame.time.Clock()
    video_duration = video_clip.duration  # Get the duration of the video
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Calculate the current video frame based on elapsed time
        elapsed_time = (pygame.time.get_ticks() / 1000) % video_duration
        video_frame = video_clip.get_frame(elapsed_time)

        # Convert the video frame to a pygame surface
        background_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))

        # Draw the video frame as the background
        screen.blit(background_surface, (0, 0))

        # Draw buttons
        button_width = 250
        button_height = 50
        button_spacing = 50

        button_x_start = (WIDTH - button_width * 2 - button_spacing) / 2
 
        # Active and inactive white shades
        active_color = (255, 255, 255)
        inactive_color = (200, 200, 200)

        if draw_button("Start Game", button_x_start, 500, button_width, button_height, active_color, inactive_color):
            asteroid_game()
        
        if draw_button("Create Character", button_x_start + button_width + button_spacing, 500, button_width, button_height, active_color, inactive_color):
            painting_program()

        # if draw_button("Exit", button_x_start + (button_width + button_spacing) / 2, 700, button_width, button_height, active_color, inactive_color):
        #     pygame.quit()
        #     sys.exit()

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()

