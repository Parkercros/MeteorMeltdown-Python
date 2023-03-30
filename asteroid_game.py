from database import HighScore
from database import HighScore
import sys
import random
import pygame.font
import pygame.mixer
from pygame.locals import *
import os
import pygame.surfarray
from database import HighScore, Player


def asteroid_game():

# Initialize Pygame
    pygame.init()
    pygame.mixer.init()

# display
    WIDTH, HEIGHT = 1600, 1000
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("asteroids")

# Load assets

    asteroid_img = pygame.image.load('assets/asteroid.png').convert_alpha()
    game_over_img = pygame.image.load('assets/game_over.png')
    game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
    shoot_sound = pygame.mixer.Sound('assets/laser.mp3')
    background_img = pygame.image.load('assets/gamebackground.jpg')
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


    spaceship_directory = 'assets/spaceships/'
    fixed_width, fixed_height = 85, 75
    spaceship_images = [pygame.transform.scale(pygame.image.load(os.path.join(spaceship_directory, img)), (fixed_width, fixed_height)) for img in os.listdir(spaceship_directory) if img.endswith('.png')]



    game_over_font = pygame.font.Font(None, 50)
    background_music = 'assets/music2.mp3'
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)
    projectile_img = pygame.image.load('assets/projectile.png')
    game_over_sound = pygame.mixer.Sound('assets/gameover.mp3')


# Score and level system
    score = 0
    level = 1
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = score_font.render(f"Level: {level}", True, (255, 255, 255))

    def update_level(score):
        return 1 + score // 10

    def update_asteroid_speed(level):
        return random.randint(2, 6) * level

# Spaceship
    class Spaceship(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = spaceship_img
        
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH // 2, HEIGHT - 60)

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                
    def opening_screen():
        background_img = pygame.image.load('assets/background2.png')  # Replace with the correct path
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        font_title = pygame.font.Font(None, 80)
        font_prompt = pygame.font.Font(None, 40)
        title_text = font_title.render("", True, (255, 255, 255))
        prompt_text = font_prompt.render("Press Enter To Start Game", True, (255, 255, 255))

        screen.blit(background_img, (0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    waiting = False

    def draw_back_button():
        back_button_width = 150
        back_button_height = 50
        back_button_x = WIDTH // 2 - back_button_width // 2
        back_button_y = HEIGHT - 100
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if back_button_x < mouse[0] < back_button_x + back_button_width and back_button_y < mouse[1] < back_button_y + back_button_height:
            pygame.draw.rect(screen, (255, 255, 255), (back_button_x, back_button_y, back_button_width, back_button_height))
            if click[0] == 1:
                main_menu()
        else:
            pygame.draw.rect(screen, (200, 200, 200), (back_button_x, back_button_y, back_button_width, back_button_height))
        

    def character_selector():
        global spaceship_img
        screen.fill((0, 0, 0))
        font_prompt = pygame.font.Font(None, 40)
        prompt_text = font_prompt.render("Select a Character", True, (255, 255, 255))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2))
        spaceship_positions = []

        for i, spaceship_image in enumerate(spaceship_images, 1):
            scaled_image = pygame.transform.scale(spaceship_image, (100, 100))
            x = WIDTH // (len(spaceship_images) + 1) * i - scaled_image.get_width() // 2
            y = HEIGHT // 2 + 50
            screen.blit(scaled_image, (x, y))

            spaceship_positions.append((scaled_image, x, y))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    for index, (image, x, y) in enumerate(spaceship_positions):
                        rect = pygame.Rect(x, y, image.get_width(), image.get_height())
                        if rect.collidepoint(mouse_pos):
                            spaceship_img = spaceship_images[index]
                            waiting = False


    def get_player_name():
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill((0, 0, 0))
            screen.blit(game_over_img, (WIDTH // 2 - game_over_img.get_width() // 2, HEIGHT // 2 - game_over_img.get_height() // 2))
            screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 100))

            txt_surface = font.render(text, True, color)
            input_box.w = max(200, txt_surface.get_width() + 10)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.flip()
            pygame.time.Clock().tick(30)
            
        return text
        
    class Projectile(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = projectile_img
            self.image = pygame.transform.scale(projectile_img, (20, 40))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            self.rect.y -= 10
            if self.rect.y < 0:
                self.kill()

    class Asteroid(pygame.sprite.Sprite):
        def __init__(self, level):
            super().__init__()
            self.image = pygame.transform.scale(asteroid_img, (90, 65))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = update_asteroid_speed(level)

        def update(self):
            self.rect.y += self.speed
            if self.rect.y > HEIGHT:
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
                self.rect.y = random.randint(-100, -40)
                self.speed = update_asteroid_speed(level)

# game objects
    all_sprites = pygame.sprite.Group()
    character_selector()
    spaceship = Spaceship()
    all_sprites.add(spaceship)
    projectiles = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    for _ in range(8):
        asteroid = Asteroid(level)
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

# Game loop
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectile = Projectile(spaceship.rect.centerx, spaceship.rect.top)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)
                    shoot_sound.play()

        all_sprites.update()

# Check for collisions
        collisions = pygame.sprite.groupcollide(projectiles, asteroids, True, True)
        for collision in collisions:
            score += 1
            level = update_level(score)
            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
            level_text = score_font.render(f"Level: {level}", True, (255, 255, 255))
            asteroid = Asteroid(level)
            all_sprites.add(asteroid)
            asteroids.add(asteroid)

# Draw background image
        screen.blit(background_img, (0, 0))

# Check for collisions between spaceship and asteroids
        if not game_over:
            hits = pygame.sprite.spritecollide(spaceship, asteroids, False)
            if hits:
                game_over = True

                spaceship.kill()
                pygame.mixer.music.stop()
                game_over_sound.play()

        if game_over:
            screen.blit(game_over_img, (WIDTH // 2 - game_over_img.get_width() // 2, HEIGHT // 2 - game_over_img.get_height() // 2))
            final_score_text = game_over_font.render(f"Your Score: {score}", True, (255, 255, 255))
            screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 100))
            player_name = get_player_name()
            Player.create(player_name) 
            high_score = HighScore.create(player_name, score)
            top_scores = HighScore.get_top_scores()
            print("Top 10 High Scores:")
            for idx, high_score in enumerate(top_scores, start=1):
                print(f"{idx}. {high_score.player_name}: {high_score.score}")

        else:
            all_sprites.draw(screen)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    return score 