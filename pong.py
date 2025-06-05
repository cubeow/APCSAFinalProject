import pygame
import sys
import random
import math
import time

# Constants
SCREENWIDTH = 800
SCREENHEIGHT = 400
PADDLEHEIGHT = 50
PADDLEWIDTH = 10
PADDINGFORPADDLE = 50
STARTBUTTONX = 350
STARTBUTTONY = 200
RESTARTBUTTONX = 400
RESTARTBUTTONY = 0
PAUSERESUMEBUTTONX = 355
PAUSERESUMEBUTTONY = -4

# Variables
velocity = 0
circle_x = SCREENWIDTH/2
circle_y = SCREENHEIGHT/2
circleDirection = random.randint(155, 205)
circle_speed = 5
speed_influence = 5
player1Score = 0
player2Score = 0
gameStart = False
robotSpeed = 2

# Initialization + basic settings
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Create objects
paddle1 = pygame.Rect(PADDINGFORPADDLE, SCREENHEIGHT/2 - PADDLEHEIGHT/2, PADDLEWIDTH, PADDLEHEIGHT)
paddle2 = pygame.Rect(SCREENWIDTH - PADDINGFORPADDLE, SCREENHEIGHT/2 - PADDLEHEIGHT/2, PADDLEWIDTH, PADDLEHEIGHT)
circle_rect = pygame.Rect(circle_x - 5, circle_y - 5, 10, 10)
text_font1 = pygame.font.Font(None, 50)
text_font2 = pygame.font.Font(None, 50)
button_text = pygame.font.Font(None, 50)
title_text = pygame.font.Font(None, 50)
button = pygame.Rect(STARTBUTTONX, STARTBUTTONY, 118, 40)
restart_img = pygame.image.load("restart.png").convert_alpha()
restart_img = pygame.transform.scale(restart_img, (50, 50))  # Resize if needed
pause_and_resume_img = pygame.image.load("pause.png").convert_alpha()
pause_and_resume_img = pygame.transform.scale(pause_and_resume_img, (70, 70))
pause_and_resume_rect = pause_and_resume_img.get_rect(topleft=(PAUSERESUMEBUTTONX, PAUSERESUMEBUTTONY))
restart_button_rect = restart_img.get_rect(topleft=(RESTARTBUTTONX, RESTARTBUTTONY))
lastHit = 0
randDirection = random.choice([-2, 2])

state = "resumed"

startedGame = False

cycles = 0
while True:
    cycles += 1
    if cycles % 60 == 0:
        randDirection = random.choice([-2, 2])
        print(cycles)
    # Quit logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not startedGame and button.collidepoint(event.pos):
                startedGame = True
            if startedGame and restart_button_rect.collidepoint(event.pos):
                # Reset the game state
                startedGame = False
                player1Score = 0
                player2Score = 0
                circle_x = SCREENWIDTH / 2
                circle_y = SCREENHEIGHT / 2
                circleDirection = random.randint(155, 205)
                paddle1.y = SCREENHEIGHT / 2 - PADDLEHEIGHT / 2
                paddle2.y = SCREENHEIGHT / 2 - PADDLEHEIGHT / 2
                gameStart = False
            if startedGame and pause_and_resume_rect.collidepoint(event.pos) and state == "resumed" and gameStart == True:
                gameStart = False
                state = "paused"
                pause_and_resume_img = pygame.image.load("resume.png").convert_alpha()
                pause_and_resume_img = pygame.transform.scale(pause_and_resume_img, (70, 70))
                pause_and_resume_rect = pause_and_resume_img.get_rect(topleft=(PAUSERESUMEBUTTONX, PAUSERESUMEBUTTONY))
            elif startedGame and pause_and_resume_rect.collidepoint(event.pos) and state == "paused" and gameStart == False:
                gameStart = True
                state = "resumed"
                pause_and_resume_img = pygame.image.load("pause.png").convert_alpha()
                pause_and_resume_img = pygame.transform.scale(pause_and_resume_img, (70, 70))
                pause_and_resume_rect = pause_and_resume_img.get_rect(topleft=(PAUSERESUMEBUTTONX, PAUSERESUMEBUTTONY))

    # Able to start game with space pressed
    if startedGame == True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            gameStart = True
    
    # Moving paddle and circle logic
    if gameStart == True:

        if keys[pygame.K_UP] and paddle1.y > 0:
            velocity = -circle_speed
        elif keys[pygame.K_DOWN] and paddle1.y + PADDLEHEIGHT < SCREENHEIGHT:
            velocity = circle_speed
        else:
            velocity =  0
        circle_x += math.cos(math.radians(circleDirection))*circle_speed
        circle_y -= math.sin(math.radians(circleDirection))*circle_speed
        circle_rect = pygame.Rect(circle_x - 5, circle_y - 5, 10, 10)

        paddle1.y += velocity

        # Robot paddle logic
        if abs(paddle2.y + PADDLEHEIGHT/2 - circle_y) > 4 and circle_x > SCREENWIDTH/2:
            if paddle2.y + PADDLEHEIGHT/2 < circle_y:
                paddle2.y += 2
            if paddle2.y + PADDLEHEIGHT/2 > circle_y:
                paddle2.y -= 2
        if circle_x < SCREENWIDTH/2 and paddle2.y > 0 and paddle2.y + PADDLEHEIGHT < SCREENHEIGHT:
            paddle2.y += randDirection
        

    # Paddle collision logic
    if paddle1.colliderect(circle_rect) and time.time() - lastHit > 1:
        circleDirection = 180 - circleDirection - velocity*speed_influence
        lastHit = time.time()

    if paddle2.colliderect(circle_rect) and time.time() - lastHit > 1:
        circleDirection = 180 - circleDirection
        lastHit = time.time()
    
    # Side collision logic
    if circle_x > SCREENWIDTH-10:
        player1Score += 1
        circle_x = SCREENWIDTH/2
        circle_y = SCREENHEIGHT/2
        circleDirection = random.randint(155, 205)
        gameStart = False
        paddle1.x = PADDINGFORPADDLE
        paddle1.y = SCREENHEIGHT/2 - PADDLEHEIGHT/2
        paddle2.x = SCREENWIDTH - PADDINGFORPADDLE
        paddle2.y = SCREENHEIGHT/2 - PADDLEHEIGHT/2
    if circle_y > SCREENHEIGHT-10:
        circleDirection = -circleDirection
    if circle_x < 10:
        player2Score += 1
        circle_x = SCREENWIDTH/2
        circle_y = SCREENHEIGHT/2
        circleDirection = random.randint(155, 205)
        gameStart = False
        paddle1.x = PADDINGFORPADDLE
        paddle1.y = SCREENHEIGHT/2 - PADDLEHEIGHT/2
        paddle2.x = SCREENWIDTH - PADDINGFORPADDLE
        paddle2.y = SCREENHEIGHT/2 - PADDLEHEIGHT/2
    if circle_y < 10:
        circleDirection = -circleDirection

    # Drawing logic
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), paddle1)
    pygame.draw.rect(screen, (255, 255, 255), paddle2)
    pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), 5)

    text_surface1 = text_font1.render(str(player1Score), False, 'White')
    text_rect1 = text_surface1.get_rect(topleft=(360, 50))
    text_surface2 = text_font2.render(str(player2Score), False, 'White')
    text_rect2 = text_surface1.get_rect(topleft=(440, 50))

    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

    if startedGame == False:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), button)
        button_text_surface = button_text.render("START", False, 'Black')
        button_rect = button_text_surface.get_rect(topleft=(STARTBUTTONX+3, STARTBUTTONY+3))
        button_text_surface = button_text.render("START", False, 'Black')
        button_rect = button_text_surface.get_rect(topleft=(STARTBUTTONX+3, STARTBUTTONY+3))
        title_surface = title_text.render("Pong", False, 'White')
        title_rect = title_surface.get_rect(topleft=(362, 70))
        
        screen.blit(button_text_surface, button_rect)
        screen.blit(title_surface, title_rect)

    if startedGame:
        screen.blit(restart_img, (RESTARTBUTTONX, RESTARTBUTTONY))
        screen.blit(pause_and_resume_img, (PAUSERESUMEBUTTONX, PAUSERESUMEBUTTONY))
    # Update + Framerate
    pygame.display.update()
    clock.tick(60)
