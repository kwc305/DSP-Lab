import pyaudio,sys
import wave
import struct
import math
import numpy as np
import pygame
import random
import time
import multiprocessing
import scipy.signal as signal
import myfunctions
import sound
from graphGUI import Button_Example

def sound_process(Type):
	# do the random sound 
	print "***start***"
	sound.main(Type) # call sound.py


def graph(Type):
	print "gui...."
	# pygame.init()
	# button_ex = Button_Example(Type)
	# button_ex.main_func(button_ex,Type)
	pass



if __name__ == '__main__':
	effect_list = ['n', 'l', 'b', 'h', 'v']
	Type = random.choice(effect_list)


	sound_process = multiprocessing.Process(name = 'sound_process',
											target = sound_process,
											args = (Type))
	# graph = multiprocessing.Process(name = 'graph',
	# 								target = graph,
	# 								args = (Type,))

	# print "start sound_process"
	# sound_process.daemon = True
	sound_process.start()
	# time.sleep(1)
	# print "start graph"
	# graph.daemon = True
	# graph.start()

	# sound_process(Type)