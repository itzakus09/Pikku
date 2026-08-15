import pygame
import sys

# -------- SETTINGS --------
WIDTH, HEIGHT = 800, 500
ROBOT_SIZE = 40
SPEED = 4

# -------- INIT --------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PHASE 4 - Virtual Robot Simulator")
clock = pygame.time.Clock()

# -------- COLORS --------
WHITE = (255,255,255)
BLUE = (0,120,255)
RED = (255,0,0)
BLACK = (0,0,0)

# -------- ROBOT --------
robot_x = WIDTH//2
robot_y = HEIGHT//2
direction = "STOP"

font = pygame.font.SysFont(None, 32)

# -------- MAIN LOOP --------
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        robot_y -= SPEED
        direction = "FORWARD"
    elif keys[pygame.K_s]:
        robot_y += SPEED
        direction = "BACKWARD"
    elif keys[pygame.K_a]:
        robot_x -= SPEED
        direction = "LEFT"
    elif keys[pygame.K_d]:
        robot_x += SPEED
        direction = "RIGHT"
    else:
        direction = "STOP"

    # Draw robot
    pygame.draw.rect(screen, BLUE, (robot_x, robot_y, ROBOT_SIZE, ROBOT_SIZE))

    # Direction text
    text = font.render(f"DIR: {direction}", True, RED)
    screen.blit(text, (20,20))

    pygame.display.update()
    clock.tick(60)