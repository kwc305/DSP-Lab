import pygame
from pygame.locals import *
from sys import exit
 
size = (800, 600)
p1 = (0, 0)
p2 = (800, 0)
p3 = (0, 600)
p4 = (800, 600)
title = "The coordinate of 800*600 screen"
black = (0, 0, 0)
white = (255, 255, 255)
 
def run():
    pygame.init()
 
    screen = pygame.display.set_mode(size, 0, 32)
    pygame.display.set_caption(title)
 
    font = pygame.font.SysFont("times", 40)
    text1 = font.render(str(p1), True, white)
    text2 = font.render(str(p2), True, white)
    text3 = font.render(str(p3), True, white)
    text4 = font.render(str(p4), True, white)
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
 
        screen.fill(black)
 
        screen.blit(text1, (0, 0))
        screen.blit(text2, (p2[0]-text2.get_width(), 0))
        screen.blit(text3, (0, p3[1]-text3.get_height()))
        screen.blit(text4, (p4[0]-text4.get_width(), p4[1]-text4.get_height()))
 
        pygame.display.update()
 
if __name__ == "__main__":
    run()
