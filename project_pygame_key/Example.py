# -*- coding: cp1252 -*-
#/usr/bin/env python
#Simon H. Larsen
#Buttons.py - example
#Project startet: d. 28. august 2012
#Import pygame modules and Buttons.py(it must be in same dir)
import pygame, pygame.font, pygame.event, pygame.draw, string, Buttons
from pygame.locals import *
import time
#Initialize pygame
pygame.init()

class Button_Example:
    def __init__(self):
        self.main()
    
    #Create a display
    def display(self):
        self.screen = pygame.display.set_mode((650,370),0,32)
        pygame.display.set_caption("Buttons.py - example")

    #Update the display and show the button
    def update_display(self):
        self.screen.fill((30,144,255))
        length = 80
        height = 80
        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.Button1.create_button(self.screen, (107,142,35), 20,  135, length,    height,    0,        "Example1", (255,255,255))
        self.Button2.create_button(self.screen, (107,142,35), 120, 135, length,    height,    0,        "Example2", (255,255,255))
        self.Button3.create_button(self.screen, (107,142,35), 220, 135, length,    height,    0,        "Example3", (255,255,255))
        self.Button4.create_button(self.screen, (107,142,35), 320, 135, length,    height,    0,        "Example4", (255,255,255))
        self.Button5.create_button(self.screen, (107,142,35), 420, 135, length,    height,    0,        "Example5", (255,255,255))
        pygame.display.flip()

    def display_box(self,screen, message):
        fontobject=pygame.font.SysFont('Arial', 50)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (107, 142, 35)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()
        time.sleep(3)


    #Run the loop
    def main(self):
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        self.Button3 = Buttons.Button()
        self.Button4 = Buttons.Button()
        self.Button5 = Buttons.Button()

        self.display()
        while True:
            self.update_display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    window_size = (650,370)
                    surf = pygame.display.set_mode(window_size)
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!1"    
                        self.display_box(surf, "Example 1")

                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!2"
                        self.display_box(surf, "Example 2")

                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!3"
                        self.display_box(surf, "Example 3")
                    elif self.Button4.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!4"
                        self.display_box(surf, "Example 4")
                    elif self.Button5.pressed(pygame.mouse.get_pos()):
                        print "Give me a command!5"
                        self.display_box(surf, "Example 5")
                    

if __name__ == '__main__':
    obj = Button_Example()
