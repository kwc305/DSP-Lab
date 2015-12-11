
import pygame, sys
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((640,600))

YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,40)



FONT = pygame.font.SysFont('monospace',20)
SURFACEFONT = FONT.render('I am salty lad!',True,RED) #True is for anti-aliasing, looks better when true 
SURFACER=SURFACEFONT.get_rect() #meaning SURFACER will gain rectangular values
SURFACER.center=(320,300)
window.fill(GREEN)

while True: 
	window.blit(SURFACEFONT, SURFACER) 
	for event in pygame.event.get(): 
		if event.type == QUIT: 
			pygame.quit() 
			sys.exit() 
		pygame.display.update()