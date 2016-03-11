#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from PathFinder import PathFinder as PF
from GridMap import GridMap as GM
from MapDrawer import MapDrawer as MD
from MazeMaker import MazeMaker as MM

from PFAlgorithmAStar import PFAlgorithmAStar as PFAAS
from PFAlgorithmJPS import PFAlgorithmJPS as PFAJPS
from PFAlgorithmDijkstra import PFAlgorithmDijkstra as PFAD

####################################################### 

class local_tag(object):
	tag_curr_fill_node_type = GM.NODE_TYPE_START

	tag_curr_init_grid_map_type = GM.INIT_TYPE_EMPTY

	tag_should_init_grid_map = False
	tag_should_run_algorithm = False

	PFA_TYPE_ASTAR = 1
	PFA_TYPE_JPS = 2
	PFA_TYPE_DIJKSTRA = 3
	tag_curr_pfa_type = PFA_TYPE_ASTAR

	TEXT_COLOR = (18,180,18)
	CIRCLE_COLOR = (14,140,14)

	NO_COLOR = (0,0,0)

	CIRCLE_RADIUS = 5

#######################################################

def keyProc(key, mod):
	if key == K_e:
		if mod & KMOD_SHIFT:
			local_tag.tag_curr_init_grid_map_type = GM.INIT_TYPE_EMPTY
			local_tag.tag_should_init_grid_map = True
		else:
			local_tag.tag_curr_fill_node_type = GM.NODE_TYPE_END

	elif key == K_s:
		local_tag.tag_curr_fill_node_type = GM.NODE_TYPE_START
	elif key == K_w:
		local_tag.tag_curr_fill_node_type = GM.NODE_TYPE_WALL
	elif key == K_r:
		if mod & KMOD_SHIFT:
			local_tag.tag_curr_init_grid_map_type = GM.INIT_TYPE_RANDOM
			local_tag.tag_should_init_grid_map = True
		else:
			local_tag.tag_should_run_algorithm = True
	elif key == K_m:
		if mod & KMOD_SHIFT:
			local_tag.tag_curr_init_grid_map_type = GM.INIT_TYPE_MAZE
			local_tag.tag_should_init_grid_map = True
	elif key == K_a:
		if mod & KMOD_CTRL:
			local_tag.tag_curr_pfa_type = local_tag.PFA_TYPE_ASTAR
	elif key == K_j:
		if mod & KMOD_CTRL:
			local_tag.tag_curr_pfa_type = local_tag.PFA_TYPE_JPS
	elif key == K_d:
		if mod & KMOD_CTRL:
			local_tag.tag_curr_pfa_type = local_tag.PFA_TYPE_DIJKSTRA

def _fillNodeUI(screen, font):

	tabStartCirclePos = (20,409)
	tabEndCirclePos = (20,434)
	tabWallCirclePos = (20,459)

	tabStart = uiFont.render("s - set Start node", False, local_tag.TEXT_COLOR)
	tabEnd = uiFont.render("e - set End node", False, local_tag.TEXT_COLOR)
	tabWall = uiFont.render("w - set Wall node", False, local_tag.TEXT_COLOR)

	pygame.draw.circle(screen, local_tag.NO_COLOR, tabStartCirclePos, local_tag.CIRCLE_RADIUS)
	pygame.draw.circle(screen, local_tag.NO_COLOR, tabEndCirclePos, local_tag.CIRCLE_RADIUS)
	pygame.draw.circle(screen, local_tag.NO_COLOR, tabWallCirclePos, local_tag.CIRCLE_RADIUS)

	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabStartCirclePos, local_tag.CIRCLE_RADIUS,1)
	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabEndCirclePos, local_tag.CIRCLE_RADIUS,1)
	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabWallCirclePos, local_tag.CIRCLE_RADIUS,1)

	if local_tag.tag_curr_fill_node_type == GM.NODE_TYPE_START:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabStartCirclePos, local_tag.CIRCLE_RADIUS)
	elif local_tag.tag_curr_fill_node_type == GM.NODE_TYPE_END:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabEndCirclePos, local_tag.CIRCLE_RADIUS)
	elif local_tag.tag_curr_fill_node_type == GM.NODE_TYPE_WALL:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabWallCirclePos, local_tag.CIRCLE_RADIUS)

	screen.blit(tabStart, (30,400))
	screen.blit(tabEnd, (30,425))
	screen.blit(tabWall, (30,450))	

def _initGridMapUI(screen, font):
	tabEmptyCirclePos = (180,409)
	tabRandomCirclePos = (180,434)
	tabMazeCirclePos = (180,459)

	tabEmpty = uiFont.render("SHIFT+e - create an Empty grid", False, local_tag.TEXT_COLOR)
	tabRandom = uiFont.render("SHIFT+r - create a Random grid", False, local_tag.TEXT_COLOR)
	tabMaze = uiFont.render("SHIFT+m - create a Maze grid", False, local_tag.TEXT_COLOR)

	pygame.draw.circle(screen, local_tag.NO_COLOR, tabEmptyCirclePos, local_tag.CIRCLE_RADIUS)
	pygame.draw.circle(screen, local_tag.NO_COLOR, tabRandomCirclePos, local_tag.CIRCLE_RADIUS)
	pygame.draw.circle(screen, local_tag.NO_COLOR, tabMazeCirclePos, local_tag.CIRCLE_RADIUS)

	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabEmptyCirclePos, local_tag.CIRCLE_RADIUS,1)
	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabRandomCirclePos, local_tag.CIRCLE_RADIUS,1)
	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabMazeCirclePos, local_tag.CIRCLE_RADIUS,1)

	if local_tag.tag_curr_init_grid_map_type == GM.INIT_TYPE_EMPTY:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabEmptyCirclePos, local_tag.CIRCLE_RADIUS)
	elif local_tag.tag_curr_init_grid_map_type == GM.INIT_TYPE_RANDOM:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabRandomCirclePos, local_tag.CIRCLE_RADIUS)
	elif local_tag.tag_curr_init_grid_map_type == GM.INIT_TYPE_MAZE:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabMazeCirclePos, local_tag.CIRCLE_RADIUS)

	screen.blit(tabEmpty, (190,400))
	screen.blit(tabRandom, (190,425))
	screen.blit(tabMaze, (190,450))
def _pfalgorithmTypeUI(screen, font):
	tabAStarCirclePos = (420,409)
	tabJPSCirclePos = (420,434)
	tabDijkstraCirclePos = (420,459)

	tabAStar = uiFont.render("CTRL+a - A*", False, local_tag.TEXT_COLOR)
	tabJPS = uiFont.render("CTRL+j - Jump Point Search", False, local_tag.TEXT_COLOR)
	tabDijkstra = uiFont.render("CTRL+d - Dijkstra", False, local_tag.TEXT_COLOR)

	pygame.draw.circle(screen, local_tag.NO_COLOR, tabAStarCirclePos, local_tag.CIRCLE_RADIUS)
	pygame.draw.circle(screen, local_tag.NO_COLOR, tabJPSCirclePos, local_tag.CIRCLE_RADIUS)
	pygame.draw.circle(screen, local_tag.NO_COLOR, tabDijkstraCirclePos, local_tag.CIRCLE_RADIUS)

	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabAStarCirclePos, local_tag.CIRCLE_RADIUS,1)
	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabJPSCirclePos, local_tag.CIRCLE_RADIUS,1)
	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabDijkstraCirclePos, local_tag.CIRCLE_RADIUS,1)

	if local_tag.tag_curr_pfa_type == local_tag.PFA_TYPE_ASTAR:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabAStarCirclePos, local_tag.CIRCLE_RADIUS)
	elif local_tag.tag_curr_pfa_type == local_tag.PFA_TYPE_JPS:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabJPSCirclePos, local_tag.CIRCLE_RADIUS)
	elif local_tag.tag_curr_pfa_type == local_tag.PFA_TYPE_DIJKSTRA:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabDijkstraCirclePos, local_tag.CIRCLE_RADIUS)

	screen.blit(tabAStar, (430,400))
	screen.blit(tabJPS, (430,425))
	screen.blit(tabDijkstra, (430,450))
def _runUI(screen, font):
	tabRun = uiFont.render("r - run", False, local_tag.TEXT_COLOR)
	screen.blit(tabRun, (10, 30))


def UIProc(screen, font):
	# print(tag_curr_fill_node_type)
	if not screen or not font:
		return
	_fillNodeUI(screen, font)
	_initGridMapUI(screen, font)
	_pfalgorithmTypeUI(screen, font)
	_runUI(screen, font)

def getAlgorithm(atype):
	if atype == local_tag.PFA_TYPE_ASTAR:
		return PFAAS()
	elif atype == local_tag.PFA_TYPE_JPS:
		return PFAJPS()
	elif atype == local_tag.PFA_TYPE_DIJKSTRA:
		return PFAD()
	else:
		return None

if __name__ == "__main__":

	# pygame init
	pygame.init()
		# pygame.event.set_blocked([KEYDOWN,KEYUP])
	pygame.event.set_blocked(KEYDOWN)

 	SCREEN_SIZE = (640, 480)
	screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF, 32)
	screen.fill((0,0,0))

	pygame.display.set_caption("PathFinder - v1.0 @ ShannonXu")

	#init font
	uiFont = pygame.font.SysFont("arial", 14)
	# testSur = uiFont.render("s - set START node", False, (18,180,18))

	# path finder init
	gridMap = GM(31,56)

	# gridMap.printMap()

	# map drawer
	mapDrawer = MD(pygame, screen, SCREEN_SIZE, gridMap)
	mapDrawer.draw()

	#path finder
	pathFinder = PF()

	#maze maker
	mazeMaker = MM()
	gridMap.setMazeMaker(mazeMaker)

	UIProc(screen, uiFont)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			elif event.type == MOUSEBUTTONUP:
				x, y = pygame.mouse.get_pos()
				# print("%d,%d" % (x,y))
				coord = mapDrawer.getCoordFromPos(x, y)
				if coord is not None:
					row, col = coord[0], coord[1]
					if local_tag.tag_curr_fill_node_type == GM.NODE_TYPE_WALL:
						if gridMap.isWallNode(row, col):
							gridMap.setFloorGridNode(row, col)
						else:
							gridMap.setWallGridNode(row, col)
					elif local_tag.tag_curr_fill_node_type == GM.NODE_TYPE_START:
						gridMap.setStartGridNode(row, col)
					elif local_tag.tag_curr_fill_node_type == GM.NODE_TYPE_END:
						gridMap.setEndGridNode(row, col)
				mapDrawer.draw()
			elif event.type == KEYUP:
				keyProc(event.key, event.mod)
				UIProc(screen, uiFont)

				if local_tag.tag_should_init_grid_map:
					gridMap.resetGridMap(local_tag.tag_curr_init_grid_map_type)
					local_tag.tag_should_init_grid_map = False
					mapDrawer.draw()

				if local_tag.tag_should_run_algorithm:
					mapDrawer.draw()
					algorithm = getAlgorithm(local_tag.tag_curr_pfa_type)
					if algorithm is not None:
						pathFinder.work(gridMap, algorithm, mapDrawer)
					local_tag.tag_should_run_algorithm = False

		# screen.blit(testSur, (10,10))

		pygame.display.flip()