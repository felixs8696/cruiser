# http://richard.cgpublisher.com/product/pub.84/prod.11
# INTIALISATION
import pygame, math, sys
from pygame.locals import *

TURN_SPEED = 8
ACCELERATION = .2
MAX_FORWARD_SPEED = 5
MAX_REVERSE_SPEED = -5
MAX_SPEED = 5
BG= (0,0,0)
MAX_Y = 768
MAX_X = 1024

def gradient_surface(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1,height), pygame.SRCALPHA).convert_alpha()
    dd = 1.0/height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(height):
        bigSurf.set_at((0,y),
                        (int(sr + rm*y),
                         int(sg + gm*y),
                         int(sb + bm*y),
                         int(sa + am*y))
                      )
    return pygame.transform.scale(bigSurf, size)

screen = pygame.display.set_mode((MAX_X, MAX_Y))
car = gradient_surface((10, 20), (255, 255, 255, 255), (0, 255, 255, 255))

clock = pygame.time.Clock() # load clock
k_up = k_down = k_left = k_right = 0 # init key values
speed = direction = 0 # start speed & direction
position = (350, 500) # start position

play = True
while play:
    clock.tick(30)
    x, y = position
    for event in pygame.event.get():

        if not hasattr(event, 'key'):
            continue

        down = event.type == KEYDOWN
        up = event.type == KEYUP
        if down:
            if event.key == K_RIGHT:
                # k_right = down * TURN_SPEED
                go_E = True
                speed = MAX_SPEED
            if event.key == K_LEFT:
                # k_left = down * TURN_SPEED
                go_W = True
                speed = MAX_SPEED
            if event.key == K_UP:
                # k_up = down * ACCELERATION
                go_N = True
                speed = MAX_SPEED
            if event.key == K_DOWN:
                # k_down = down * ACCELERATION
                go_S = True
                speed = MAX_SPEED
            if event.key == K_ESCAPE:
                play = False
                speed = MAX_SPEED

    screen.fill(BG)

    if speed > MAX_FORWARD_SPEED:
        speed = MAX_FORWARD_SPEED
    if speed < MAX_REVERSE_SPEED:
        speed = MAX_REVERSE_SPEED

    if go_E:
        x += speed
    elif go_W:
        x -= speed
    elif go_N:
        y += speed
    elif go_S:
        y -= speed

    # make sure the car doesn't exit the screen
    if y < 0:
        y = 0 # TODO is there another way to treat this?
    elif y > MAX_Y:
        y = MAX_Y
    if x < 0:
        x = 0
    elif x > MAX_X:
        x = MAX_X        
    position = (x, y)
    
    rect = car.get_rect()
    rect.center = position
    print(position)
    
    screen.blit(car, rect)
    pygame.display.flip()

sys.exit(0) # quit the game