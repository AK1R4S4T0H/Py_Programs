import pygame
import random

pygame.init()

window_width = 400
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


white = (255, 255, 255)
black = (0, 0, 0)

snake_x = 200
snake_y = 200
snake_speed = 2


snake_size = 10
snake_direction = "RIGHT"

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN:
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                snake_direction = "RIGHT"

    # Move the snake
    if snake_direction == "UP":
        snake_y -= snake_speed
    elif snake_direction == "DOWN":
        snake_y += snake_speed
    elif snake_direction == "LEFT":
        snake_x -= snake_speed
    elif snake_direction == "RIGHT":
        snake_x += snake_speed


    window.fill(white)
    pygame.draw.rect(window, black, [snake_x, snake_y, snake_size, snake_size])

    pygame.display.update()

    clock.tick(60)
