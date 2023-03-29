from database import save_score, get_scores

def update_high_scores(score):
    # Save score
    player_name = "player1"  # Replace this with the actual player's name or a placeholder name
    save_score(player_name, score)

    # Retrieve scores
    scores = get_scores()
    print("High Scores:")
    for name, score in scores.items():
        print(f"{name}: {score}")


def asteroid_game():
    # Paste your entire game code here


    import sys
    import random
    import pygame.font
    import pygame.mixer


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


    spaceship_images = [
        pygame.image.load('assets/spaceships/spaceship.png'),
        pygame.image.load('assets/spaceships/spaceship2.png'),
        pygame.image.load('assets/spaceships/spaceship3.png'),
        pygame.image.load('assets/spaceships/spaceship4.png')
    ]


    game_over_font = pygame.font.Font(None, 50)
    background_music = 'assets/music.mp3'
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
        background_img = pygame.image.load('background2.png')
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

    def character_selector():
        global spaceship_img
        screen.fill((0, 0, 0))
        font_prompt = pygame.font.Font(None, 40)
        prompt_text = font_prompt.render("Select a Character", True, (255, 255, 255))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2))

        for i, spaceship_image in enumerate(spaceship_images, 1):
            scaled_image = pygame.transform.scale(spaceship_image, (100, 100))
            x = WIDTH // 5 * i - scaled_image.get_width() // 2
            y = HEIGHT // 2 + 50
            screen.blit(scaled_image, (x, y))
            num_text = score_font.render(str(i), True, (255, 255, 255))
            screen.blit(num_text, (x + scaled_image.get_width() // 2 - num_text.get_width() // 2, y + 110))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        spaceship_img = spaceship_images[0]
                        waiting = False
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        spaceship_img = spaceship_images[1]
                        waiting = False
                    elif event.key in (pygame.K_3, pygame.K_KP3):
                        spaceship_img = spaceship_images[2]
                        waiting = False
                    elif event.key in (pygame.K_4, pygame.K_KP4):
                        spaceship_img = spaceship_images[3]
                        waiting = False

        
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
                update_high_scores(score)

                spaceship.kill()
                pygame.mixer.music.stop()
                game_over_sound.play()

        if game_over:
            screen.blit(game_over_img, (WIDTH // 2 - game_over_img.get_width() // 2, HEIGHT // 2 - game_over_img.get_height() // 2))
            final_score_text = game_over_font.render(f"Your Score: {score}", True, (255, 255, 255))
            screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 100))

        else:
            all_sprites.draw(screen)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    return score  # Return the player's score after the game ends
