import sys
import time
import multiprocessing


#create a multiprocessing Queue object for sending messages to an input process
queueToInputProcess = multiprocessing.Queue()

#create a multiprocessing Queue object for receiving messages from an input process
queueFromInputProcess = multiprocessing.Queue()

#define a function to run continuously in a seperate process that monitors the pygame event queue for keypress events
def inputProcessLoop(queueToInputProcess,queueFromInputProcess):
	import pygame
	pygame.init()
	done = False
	while not done:
		now = time.time()
		pygame.event.pump()
		for event in pygame.event.get() :
			if event.type == pygame.KEYDOWN :
				response = event.unicode
				response_time = now
				queueFromInputProcess.put([response,response_time])
		if not queueToInputProcess.empty():
			from_queue = queueToInputProcess.get()
			if from_queue == 'quit':
				done = True


#start up the input detector in a separate process
inputProcess = multiprocessing.Process(target=inputProcessLoop, args=(queueToInputProcess,queueFromInputProcess,))
inputProcess.start()


#create a multiprocessing Queue object for sending messages to an output process
queueToOutputProcess = multiprocessing.Queue()

#define a function to run continuously in a seperate process that monitors the output queue for messages and writes data as necessary
def outputProcessLoop(queueToOutputProcess):
	outfile = open('outfile.txt','w')
	done = False
	while not done:
		if not queueToOutputProcess.empty():
			from_queue = queueToOutputProcess.get()
			if from_queue == 'quit':
				outfile.close()
				done = True
			else:
				outfile.write(from_queue+'\n')


#start up the output process in a separate process
outputProcess = multiprocessing.Process(target=outputProcessLoop, args=(queueToOutputProcess,))
outputProcess.start()

if __name__ == "__main__":

	#initialize pygame
	import pygame
	pygame.init()
	
	#initialize a font
	defaultFontName = pygame.font.get_default_font()
	feedbackFont = pygame.font.Font(defaultFontName, 100)

	#start the diaplay loop
	done = False
	updateDisplay = False
	while not done:
		if not queueFromInputProcess.empty():
			from_queue = queueFromInputProcess.get()
			if from_queue[0]=='\x1b':
				queueToInputProcess.put('quit')
				queueToOutputProcess.put('quit')
				inputProcess.join()
				outputProcess.join()
				pygame.quit()
				sys.exit()
			elif from_queue[0]=='i':
				screen = pygame.display.set_mode((1366,768),pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
				# screen = pygame.display.set_mode((400,400))
				screen.fill((0,0,0))
				pygame.display.flip()				
			else:
				toDisplay = from_queue[0]
				updateDisplay = True
		if updateDisplay:
			updateDisplay = False
			thisRender = feedbackFont.render(toDisplay, True, (255,255,255))
			x = screen.get_width()/2-thisRender.get_width()/2
			y = screen.get_height()/2-thisRender.get_height()/2
			screen.fill((0,0,0))
			screen.blit(thisRender,(x,y))
			pygame.display.flip()
			flipLatency = str(time.time()-from_queue[1])
			queueToOutputProcess.put(flipLatency)