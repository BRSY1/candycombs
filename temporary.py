# import pygame
# import sys
# import math

# # Initialize Pygame
# pygame.init()

# # Screen dimensions
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Scrolling Map with Restricted Vision")

# # Colors
# WHITE = (255, 255, 255)
# TILE_COLOR = (200, 200, 200)

# # Tile setup
# TILE_SIZE = 50  # Size of each tile
# MAP_WIDTH = 1600  # Width of the entire map in pixels
# MAP_HEIGHT = 1200  # Height of the entire map in pixels

# # Load character image with transparency
# character_image = pygame.image.load("MCnew.png").convert_alpha()
# character_image.set_alpha(150)  # Adjust transparency if needed
# character_rect = character_image.get_rect()
# character_speed = 5

# # Center character on the screen
# character_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# # Vision radius
# VISION_RADIUS = 150  # Radius around the character that is visible

# # Character position on the map
# character_map_x = MAP_WIDTH // 2
# character_map_y = MAP_HEIGHT // 2

# # Main game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     # Key handling for movement
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         character_map_x -= character_speed
#     if keys[pygame.K_RIGHT]:
#         character_map_x += character_speed
#     if keys[pygame.K_UP]:
#         character_map_y -= character_speed
#     if keys[pygame.K_DOWN]:
#         character_map_y += character_speed

#     # Set boundaries so the character can't go off the map
#     character_map_x = max(VISION_RADIUS, min(character_map_x, MAP_WIDTH - VISION_RADIUS))
#     character_map_y = max(VISION_RADIUS, min(character_map_y, MAP_HEIGHT - VISION_RADIUS))

#     # Calculate the top-left corner of the visible area
#     visible_x = character_map_x - SCREEN_WIDTH // 2
#     visible_y = character_map_y - SCREEN_HEIGHT // 2

#     # Draw tiled map background
#     screen.fill(WHITE)
#     for row in range(0, MAP_HEIGHT, TILE_SIZE):
#         for col in range(0, MAP_WIDTH, TILE_SIZE):
#             # Only draw tiles within the visible area
#             tile_x = col - visible_x
#             tile_y = row - visible_y
#             if 0 <= tile_x < SCREEN_WIDTH and 0 <= tile_y < SCREEN_HEIGHT:
#                 pygame.draw.rect(screen, TILE_COLOR, (tile_x, tile_y, TILE_SIZE, TILE_SIZE), 1)

#     # Draw the character
#     screen.blit(character_image, character_rect)

#     # Apply the vision radius mask
#     vision_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#     vision_surface.fill((0, 0, 0, 180))  # Dark overlay outside the vision radius
#     pygame.draw.circle(vision_surface, (0, 0, 0, 0), character_rect.center, VISION_RADIUS)
#     screen.blit(vision_surface, (0, 0))

#     pygame.display.flip()
#     pygame.time.Clock().tick(30)

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Centered Character with Map Array")

# Colors
TILE_COLORS = {
    0: (255, 255, 255),  # Empty tile (white)
    1: (0, 255, 0),      # Grass (green)
    2: (0, 0, 255),      # Water (blue)
}

# Define the map (2D array)
myMap = [
    [0, 1, 1, 0, 0],
    [1, 1, 1, 0, 2],
    [0, 0, 1, 1, 1],
    [0, 2, 0, 0, 0],
    [0, 1, 1, 1, 0],
]

# Tile size
TILE_SIZE = 100  # Each tile is 100x100 pixels

# Character position on the map
character_map_x = 2  # Starting column index
character_map_y = 2  # Starting row index

# Character speed
character_speed = 1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key handling for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and character_map_x > 0:
        character_map_x -= character_speed
    if keys[pygame.K_RIGHT] and character_map_x < len(myMap[0]) - 1:
        character_map_x += character_speed
    if keys[pygame.K_UP] and character_map_y > 0:
        character_map_y -= character_speed
    if keys[pygame.K_DOWN] and character_map_y < len(myMap) - 1:
        character_map_y += character_speed

    # Calculate visible area based on character position
    visible_x = character_map_x * TILE_SIZE - SCREEN_WIDTH // 2
    visible_y = character_map_y * TILE_SIZE - SCREEN_HEIGHT // 2

    # Draw the map based on the array
    screen.fill((0, 0, 0))  # Clear the screen with black
    for row in range(len(myMap)):
        for col in range(len(myMap[row])):
            # Calculate where to draw each tile
            tile_x = col * TILE_SIZE - visible_x
            tile_y = row * TILE_SIZE - visible_y

            # Draw only tiles that are visible
            if 0 <= tile_x < SCREEN_WIDTH and 0 <= tile_y < SCREEN_HEIGHT:
                color = TILE_COLORS.get(myMap[row][col], (255, 255, 255))  # Default to white if not found
                pygame.draw.rect(screen, color, (tile_x, tile_y, TILE_SIZE, TILE_SIZE))

    # Draw the character (as a simple rectangle for now)
    character_rect = pygame.Rect(SCREEN_WIDTH // 2 - TILE_SIZE // 2, SCREEN_HEIGHT // 2 - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (255, 0, 0), character_rect)  # Draw the character in red

    pygame.display.flip()  # Update the display
    pygame.time.Clock().tick(30)  # Control the frame rate
