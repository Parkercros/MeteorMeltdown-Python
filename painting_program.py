import pygame
import sys
import colorsys
import os
from moviepy.editor import VideoFileClip
from art import insert_image_date, get_image_size
import datetime


images_dir = "assets/spaceships"
if not os.path.exists(images_dir):
    os.makedirs(images_dir)
    
WIDTH, HEIGHT = 1600, 1000
GRID_SIZE = 10
BACKGROUND_COLOR = (245, 245, 245)
COLOR_PALETTE_POS = (10, HEIGHT - 295)
COLOR_PALETTE_SIZE = 15
COLOR_PALETTE_GRID_SIZE = 16
PALETTE_CONTAINER_PADDING = 15
color = (0, 0, 255)

INITIAL_BRUSH_SIZE = 1

pygame.init()
font = pygame.font.Font(None, 36) 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((128, 128, 128))

# Set up the drawing surface
draw_width = WIDTH - COLOR_PALETTE_POS[0] - (COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 5)) - 30
draw_height = HEIGHT - 50
draw_surface = pygame.Surface((draw_width, draw_height))
draw_surface.fill(BACKGROUND_COLOR)

# Create a grid to hold the drawing
grid = []
for x in range(draw_width // GRID_SIZE):
    grid.append([BACKGROUND_COLOR] * (draw_height // GRID_SIZE))

# Create a color palette
color_palette = []
for i in range(256):
    hue = i / 256
    saturation = (i % 16) / 15
    value = 1 - (i // 16) / 15
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, saturation, value)]
    color_palette.append((r, g, b))

def draw_grid():
    draw_surface.fill(BACKGROUND_COLOR)

    for x, col in enumerate(grid):
        for y, color in enumerate(col):
            pygame.draw.rect(draw_surface, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_color_palette():

    for i, color in enumerate(color_palette):
        x = i % COLOR_PALETTE_GRID_SIZE
        y = i // COLOR_PALETTE_GRID_SIZE
        pygame.draw.rect(screen, color, (COLOR_PALETTE_POS[0] + x * (COLOR_PALETTE_SIZE + 1), COLOR_PALETTE_POS[1] + y * (COLOR_PALETTE_SIZE + 1), COLOR_PALETTE_SIZE, COLOR_PALETTE_SIZE), 0)

def draw_spaceship():
    save_image()
    filename = f"image_{len(os.listdir(images_dir)) - 1}.png"
    filepath = os.path.join(images_dir, filename)
    return filepath


def save_image():
    min_x, min_y, max_x, max_y = draw_width, draw_height, 0, 0

    for x, col in enumerate(grid):
        for y, color in enumerate(col):
            if color != BACKGROUND_COLOR:
                min_x = min(min_x, x * GRID_SIZE)
                min_y = min(min_y, y * GRID_SIZE)
                max_x = max(max_x, (x + 1) * GRID_SIZE)
                max_y = max(max_y, (y + 1) * GRID_SIZE)

    if min_x == draw_width and min_y == draw_height and max_x == 0 and max_y == 0:
        return

    cropped_width = max_x - min_x
    cropped_height = max_y - min_y
    surface = pygame.Surface((cropped_width, cropped_height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    for x, col in enumerate(grid):
        for y, color in enumerate(col):
            if color != BACKGROUND_COLOR:
                pygame.draw.rect(surface, color, ((x * GRID_SIZE) - min_x, (y * GRID_SIZE) - min_y, GRID_SIZE, GRID_SIZE), 0)

    filename = f"image_{len(os.listdir(images_dir))}.png"
    filepath = os.path.join(images_dir, filename)
    pygame.image.save(surface, filepath)

    width, height = surface.get_size()

    date_saved = datetime.date.today()
    insert_image_date(date_saved, filepath, width, height)

    return filepath

    
video_clip_painting = VideoFileClip("assets/rocks.mp4")
video_clip_painting = video_clip_painting.resize((WIDTH, HEIGHT))

def draw_back_button():
    back_button_text = font.render("Back To Menu", True, (255, 255, 255))
    back_button_rect = back_button_text.get_rect(center=(150, 45))

    pygame.draw.rect(screen, (75, 119, 190), (50, 20, 200, 50), 0)
    screen.blit(back_button_text, back_button_rect)
    
def reset_drawing_area():
    draw_surface.fill(BACKGROUND_COLOR)
    for x in range(draw_width // GRID_SIZE):
        for y in range(draw_height // GRID_SIZE):
            grid[x][y] = BACKGROUND_COLOR

def painting_program():
    drawing = False
    color = (160, 160, 160)
    brush_size = INITIAL_BRUSH_SIZE
    clock = pygame.time.Clock()

    video_clip_painting = VideoFileClip("assets/rocks.mp4")
    video_clip_painting = video_clip_painting.resize((WIDTH, HEIGHT))
    video_duration = video_clip_painting.duration
    saved_image_path = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    saved_image_path = save_image()
                    reset_drawing_area()
                    return saved_image_path

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        drawing = True
            
                    x, y = event.pos  # Add this line to define x and y before checking for back button click

                        # Check if the back button is clicked
                back_button_x, back_button_y, back_button_width, back_button_height = 50, 20, 200, 50
                if back_button_x <= x <= back_button_x + back_button_width and back_button_y <= y <= back_button_y + back_button_height:
                    return
                            
                        

                if event.button == 1:
                    x, y = event.pos
                    if COLOR_PALETTE_POS[0] <= x <= COLOR_PALETTE_POS[0] + (COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1)) and COLOR_PALETTE_POS[1] <= y <= COLOR_PALETTE_POS[1] + (COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1)):
                        palette_x = (x - COLOR_PALETTE_POS[0]) // (COLOR_PALETTE_SIZE + 1)
                        palette_y = (y - COLOR_PALETTE_POS[1]) // (COLOR_PALETTE_SIZE + 1)
                        color_index = palette_y * COLOR_PALETTE_GRID_SIZE + palette_x
                        if 0 <= color_index < len(color_palette):
                            color = color_palette[color_index]

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    x, y = event.pos
                    x -= COLOR_PALETTE_POS[0] + COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1) + 10
                    y -= 10

                    if 0 <= x < draw_width and 0 <= y < draw_height:
                        pygame.draw.circle(draw_surface, color, (x, y), brush_size)
                        grid_x = x // GRID_SIZE
                        grid_y = y // GRID_SIZE
                        for i in range(max(0, grid_x - brush_size), min(draw_width // GRID_SIZE, grid_x + brush_size + 1)):
                            for j in range(max(0, grid_y - brush_size), min(draw_height // GRID_SIZE, grid_y + brush_size + 1)):
                                grid[i][j] = color

 # Calculate the current video frame based on elapsed time
        elapsed_time = (pygame.time.get_ticks() / 1000) % video_duration
        video_frame = video_clip_painting.get_frame(elapsed_time)
        
# Convert the video frame to a pygame surface
        background_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))

# Draw the video frame as the background
        screen.blit(background_surface, (0, 0))

# Draw the color palette on the screen
        draw_color_palette()

# Draw the drawing surface on the screen
        screen.blit(draw_surface, (COLOR_PALETTE_POS[0] + COLOR_PALETTE_GRID_SIZE * (COLOR_PALETTE_SIZE + 1) + 10, 10))

        draw_grid()
        
# Draw the back button
        draw_back_button()

        pygame.display.flip()
        clock.tick(30)



if __name__ == "__main__":
    saved_image_path = painting_program()
    if saved_image_path:
        date_saved = datetime.date.today()
        insert_image_date(date_saved, saved_image_path)