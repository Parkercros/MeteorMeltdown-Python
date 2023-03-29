import pygame
import sys
from asteroid_game import asteroid_game
from painting_program import painting_program
from moviepy.editor import VideoFileClip
from asteroid_game import asteroid_game
from database import HighScore

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/music2.mp3")
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 1600, 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('App Menu')

video_clip = VideoFileClip("assets/rocks.mp4")
video_clip = video_clip.resize((WIDTH, HEIGHT))
video_clip_highscore = VideoFileClip("assets/77.mp4")
video_clip_highscore = video_clip_highscore.resize((WIDTH, HEIGHT))


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
    video_duration = video_clip.duration
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed_time = (pygame.time.get_ticks() / 1000) % video_duration
        video_frame = video_clip.get_frame(elapsed_time)

        background_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))

        screen.blit(background_surface, (0, 0))

        button_width = 250
        button_height = 50
        button_spacing = 50

        button_x_start = (WIDTH - button_width * 3 - button_spacing * 2) / 2

        active_color = (255, 255, 255)
        inactive_color = (200, 200, 200)

        if draw_button("Start Game", button_x_start, 500, button_width, button_height, active_color, inactive_color):
            player_score = asteroid_game()
            player_name = input("Enter your name: ")
            if player_name:
                HighScore.create(player_name, player_score)
            scores = HighScore.get_top_scores()

        if draw_button("Create Character", button_x_start + button_width + button_spacing, 500, button_width, button_height, active_color, inactive_color):
            painting_program()

        if draw_button("High Scores", button_x_start + button_width * 2 + button_spacing * 2, 500, button_width, button_height, active_color, inactive_color):
            high_scores_menu(HighScore.get_top_scores())

        pygame.display.update()
        clock.tick(30)


def high_scores_menu(scores):
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 80)
    score_font = pygame.font.Font(None, 50)
    video_duration = video_clip_highscore.duration

    num_scores_to_display = 10
    screen_margin = 150
    score_spacing = (HEIGHT - 2 * screen_margin) // num_scores_to_display

    name_x = WIDTH // 2 - 150 + 40  
    score_x = WIDTH // 2 + 150 + 40  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                return

        elapsed_time = (pygame.time.get_ticks() / 1000) % video_duration
        video_frame = video_clip_highscore.get_frame(elapsed_time)
        background_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))
        screen.blit(background_surface, (0, 0))

        title_surface = title_font.render("High Scores", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, screen_margin // 2))
        screen.blit(title_surface, title_rect)

        y = screen_margin
        for index, score in enumerate(scores[:num_scores_to_display]):
            rank_text = f"{index + 1}."
            name_text = score.player_name
            score_text = f"{score.score}"

            rank_surface = score_font.render(rank_text, True, (255, 255, 255))
            name_surface = score_font.render(name_text, True, (255, 255, 255))
            score_surface = score_font.render(score_text, True, (255, 255, 255))

            rank_rect = rank_surface.get_rect(midleft=(name_x - 100, y))
            name_rect = name_surface.get_rect(midleft=(name_x, y))
            score_rect = score_surface.get_rect(midright=(score_x, y))

            screen.blit(rank_surface, rank_rect)
            screen.blit(name_surface, name_rect)
            screen.blit(score_surface, score_rect)

            y += score_spacing

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()