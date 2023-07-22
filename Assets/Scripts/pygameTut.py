import pygame
import random
from pygame.constants import BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.time import Clock
from array import *

WIDTH, HEIGHT = 1000, 1000

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

maxFPS = 60

live_cell_color = [255,255,255]
dead_cell_color = [0,0,0]

CELL_COUNT_ALIVE = 0
CELL_COUNT_DEAD = 0



CELL_WIDTH = 10
CELL_HEIGHT = CELL_WIDTH



CELL_SIZE = round(CELL_HEIGHT * CELL_WIDTH)

CELL_DEAD = False
CELL_ALIVE = True

COLUMS = round(WIDTH / CELL_WIDTH)
ROWS = round(HEIGHT / CELL_HEIGHT)

GRID = []

for row in range(ROWS):
    GRID.append([])
    for colums in range(COLUMS):
        GRID[row].append(0)

def RandomizeGrid():
	for x in range(0,COLUMS):
		for y in range(0,ROWS):
			randBit = random.randint(0,1)
			GRID[x][y] = randBit

def drawSingleCell(x,y):
	pygame.draw.rect(WINDOW,(255,255,255),[x * CELL_WIDTH,y * CELL_HEIGHT,CELL_WIDTH,CELL_HEIGHT])
	GRID[x][y] = CELL_ALIVE

def fillGrid():
	for x in range(0,COLUMS):
		for y in range(0,ROWS):
			drawSingleCell(x,y)

def clearGrid():
	for x in range(0,COLUMS):
		for y in range(0,ROWS):
			destroySingleCell(x,y)

def destroySingleCell(x,y):
	pygame.draw.rect(WINDOW,(0,0,0),[x * CELL_WIDTH,y * CELL_HEIGHT,CELL_WIDTH,CELL_HEIGHT])
	GRID[x][y] = CELL_DEAD

def newDrawGrid():
	for row in range(ROWS):
		for column in range(COLUMS):
			if GRID[row][column] == CELL_ALIVE:
				pygame.draw.rect(WINDOW,(live_cell_color),[column * CELL_WIDTH,row * CELL_HEIGHT,CELL_WIDTH,CELL_HEIGHT])
			else:
				pygame.draw.rect(WINDOW,(dead_cell_color),[column * CELL_WIDTH,row * CELL_HEIGHT,CELL_WIDTH,CELL_HEIGHT])
			
					
def LiveNeighbourCount(x,y):
	bitSum = 0
	for i in range(-1,2):
		for j in range(-1,2):
			col = (x+i+COLUMS) % COLUMS
			row = (y+j+ROWS) % ROWS
			bitSum += GRID[row][col]
	bitSum -= GRID [x] [y]
	return bitSum			

def checkGrid(GRID):
	NEXT_GRID = GRID

	for x in range(ROWS):
		for y in range(COLUMS):
			neighbours = LiveNeighbourCount(x,y)
			CELL_STATE = GRID[x][y]
			#Rule 1#: If the cell has 3 neighbours, change to state 1 (live)
			if CELL_STATE == CELL_DEAD and neighbours == 3:
				NEXT_GRID[x] [y] = CELL_ALIVE
			##Rules 2 & 3#: If the cell has less than 2 or more than 3 neighbours, change to state 0 (dead)
			elif CELL_STATE == CELL_ALIVE and (neighbours < 2 or neighbours > 3):
				#print(str(x) + " , " + str(y))
				NEXT_GRID [x] [y] = CELL_DEAD
			else:
				NEXT_GRID [x] [y] = CELL_STATE
				
	GRID = NEXT_GRID

def drawCursor():
	mouseX, mouseY = pygame.mouse.get_pos()
	relPos_y, relPos_x = int(round(mouseY,-1)) / CELL_HEIGHT , int(round(mouseX,-1)) / CELL_WIDTH
	pygame.draw.rect(WINDOW,(235, 64, 52), [relPos_x * CELL_WIDTH,relPos_y * CELL_HEIGHT,CELL_WIDTH,CELL_HEIGHT])

def changeBrushSize():
	size = 1
	sizeMultiplier = 2
	mouseSizeIncrease = 0 #increase size by mouse scrolling (maybe while holding shift or control???)
	
	size = mouseSizeIncrease * sizeMultiplier


def main():
	
	RandomizeGrid()
	newDrawGrid()	
	pygame.display.update()

	Clock = pygame.time.Clock()
	run = True
	pause = False
	while run:
		Clock.tick(maxFPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					print("Pausing...")
					pause = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					print("Restarting...")
					RandomizeGrid()
					newDrawGrid()	
					pygame.display.update()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_i:
					print("Restarting...")
					

					RandomizeGrid()
					newDrawGrid()	
					pygame.display.update()
		if pause == False:
			checkGrid(GRID)
			newDrawGrid()
			#print("Updating Grid")
			pygame.display.update()
		else:
			while pause:
				#print("Paused!!!")
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.QUIT()
					if event.type == KEYDOWN:
						if event.key == pygame.K_f:
							pause = False
						if event.key == pygame.K_g:
							fillGrid()
						if event.key == pygame.K_h:
							clearGrid()
					if pygame.mouse.get_pressed()[0]:
						mouseX , mouseY = pygame.mouse.get_pos()
						drawSingleCell(round(int(round(mouseY,-1)) / CELL_HEIGHT),round(int(round(mouseX,-1)) / CELL_WIDTH))
						#print("Changing Cell!!!: " + str(int(round(mouseX,-1)) / CELL_WIDTH) + " , " + str(int(round(mouseY,-1)) / CELL_HEIGHT))
					if pygame.mouse.get_pressed()[1]:
						mouseX , mouseY = pygame.mouse.get_pos()
						destroySingleCell(int(round(mouseY,-1)) / CELL_HEIGHT,int(round(mouseX,-1)) / CELL_WIDTH)
						#print("Changing Cell!!!: " + str(int(round(mouseX,-1)) / CELL_WIDTH) + " , " + str(int(round(mouseY,-1)) / CELL_HEIGHT))
						

					
				newDrawGrid()
				drawCursor()
				pygame.display.update()
		
	pygame.quit()



if __name__ == "__main__":
	main()