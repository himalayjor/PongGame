# Implementation of classic arcade game Pong

import pygame, sys
import random
from pygame.locals import *

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HPD = PAD_WIDTH / 2
HPH = PAD_HEIGHT / 2

# helper function that spawns a ball by updating the
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH/2, HEIGHT/2]
    x = random.randrange(2, 4)
    y = random.randrange(1, 3)
    if right:
        ball_vel = [x,-y]
    else:
        ball_vel = [-x, -y]

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints

    score1 = 0
    score2 = 0
    paddle1_pos = [HPD, HEIGHT/2]
    paddle2_pos = [WIDTH - HPD, HEIGHT/2]
    paddle1_vel = 0
    paddle2_vel = 0
    ball_init(True)

def draw(screen):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    color = (255, 255, 255)
    # update paddle's vertical position, keep paddle on the screen

    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel

    if (paddle1_pos[1] + HPH > HEIGHT or paddle1_pos[1] - HPH < 0):
        paddle1_pos[1] -= paddle1_vel
    if (paddle2_pos[1] + HPH > HEIGHT or paddle2_pos[1] - HPH < 0):
        paddle2_pos[1] -= paddle2_vel

    # draw mid line and gutters


    pygame.draw.line(screen, color, (WIDTH / 2, 0),(WIDTH / 2, HEIGHT), 1)
    pygame.draw.line(screen, color, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(screen, color, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)



    # draw paddles


    pygame.draw.line(screen, color, [0, paddle1_pos[1] + HPH] , [PAD_WIDTH, paddle1_pos[1] + HPH])
    pygame.draw.line(screen, color, [0, paddle1_pos[1] - HPH] , [PAD_WIDTH, paddle1_pos[1] - HPH])
    pygame.draw.line(screen, color, [WIDTH - PAD_WIDTH, paddle2_pos[1] + HPH] , [WIDTH, paddle2_pos[1] + HPH])
    pygame.draw.line(screen, color, [WIDTH - PAD_WIDTH, paddle2_pos[1] - HPH] , [WIDTH, paddle2_pos[1] - HPH])

    # update ball
    ball_pos[0] +=  ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ( (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH) ):
        if (ball_pos[1] < HPH + paddle1_pos[1] and paddle1_pos[1] - HPH < ball_pos[1]):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += 0.1 * ball_vel[0]
            ball_vel[1] += 0.1 * ball_vel[1]
        else:
            score2 += 1
            ball_init(True)
    elif (ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH - 1):
        if (ball_pos[1] < HPH + paddle2_pos[1] and paddle2_pos[1] - HPH < ball_pos[1]):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += 0.1 * ball_vel[0]
            ball_vel[1] += 0.1 * ball_vel[1]
        else:
            score1 += 1
            ball_init(False)

    if ( (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS - PAD_WIDTH - 1) ):
        ball_vel[1] = -ball_vel[1]

     # draw ball and scores
    pygame.draw.circle(screen, (255, 0, 0), ( int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    font=pygame.font.Font(None,48)
    scoretext=font.render(str(score1), 1,(255,0,0))
    screen.blit(scoretext, (200, 50))
    scoretext=font.render(str(score2), 1,(255,0,0))
    screen.blit(scoretext, (400, 50))




def keydown(key):
    global paddle1_vel, paddle2_vel

    if (key == K_UP):
        paddle2_vel = -2
    elif (key == K_DOWN):
        paddle2_vel = 2
    elif (key == K_w):
        paddle1_vel = -2
    elif (key == K_s):
        paddle1_vel = 2


def keyup(key):
    global paddle1_vel, paddle2_vel

    if (key == K_UP):
        paddle2_vel = 0
    elif (key == K_DOWN):
        paddle2_vel = 0
    elif (key == K_w):
        paddle1_vel = 0
    elif (key == K_s):
        paddle1_vel = 0

def handler():
    new_game()



def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    background = pygame.image.load('bg1.jpg').convert()
    clock = pygame.time.Clock()
    milli = clock.tick()

    pygame.display.set_caption('PONG')
    new_game()

    while True:

         screen.blit(background, (0,0))
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keydown(event.key)
            elif event.type == pygame.KEYUP:
                keyup(event.key)

         milli = clock.tick(milli*10)

         draw(screen)
         pygame.display.update()

if __name__ == '__main__':
    main()
