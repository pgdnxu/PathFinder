#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

import time

import pygame
from pygame.locals import *

from PathFinder import PathFinder as PF
from GridMap import GridMap as GM
from MapDrawer import MapDrawer as MD
from MazeMaker import MazeMaker as MM

from RTSSim import RTSSim as RTSS

from PFAlgorithmAStar import PFAlgorithmAStar as PFAAS
from PFAlgorithmJPS import PFAlgorithmJPS as PFAJPS
from PFAlgorithmDijkstra import PFAlgorithmDijkstra as PFAD

####################################################### 

class local_tag(object):
	tag_curr_pf_fill_node_type = GM.NODE_TYPE_START
	tag_curr_rts_fill_node_type = GM.NODE_TYPE_END

	tag_curr_init_grid_map_type = GM.INIT_TYPE_EMPTY

	tag_should_init_grid_map = False
	tag_should_run_algorithm = False

	tag_should_run_rts_sim = False

	SIM_TYPE_PF = 1
	SIM_TYPE_RTS = 2
	tag_curr_sim_type = SIM_TYPE_PF

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
			local_tag.tag_curr_pf_fill_node_type = GM.NODE_TYPE_END
			local_tag.tag_curr_rts_fill_node_type = GM.NODE_TYPE_END
	elif key == K_s:
		if mod & KMOD_CTRL:
			local_tag.tag_should_run_rts_sim = False
		else:
			local_tag.tag_curr_pf_fill_node_type = GM.NODE_TYPE_START
	elif key == K_w:
		local_tag.tag_curr_pf_fill_node_type = GM.NODE_TYPE_WALL
		local_tag.tag_curr_rts_fill_node_type = GM.NODE_TYPE_WALL
	elif key == K_r:
		if mod & KMOD_SHIFT:
			local_tag.tag_curr_init_grid_map_type = GM.INIT_TYPE_RANDOM
			local_tag.tag_should_init_grid_map = True
		else:
			local_tag.tag_should_run_algorithm = True
			local_tag.tag_should_run_rts_sim = True
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
	elif key == K_p:
		if local_tag.tag_curr_sim_type != local_tag.SIM_TYPE_PF:
			local_tag.tag_curr_sim_type = local_tag.SIM_TYPE_PF
			_simTypeChangeTo(local_tag.SIM_TYPE_PF)
	elif key == K_t:
		if local_tag.tag_curr_sim_type != local_tag.SIM_TYPE_RTS:
			local_tag.tag_curr_sim_type = local_tag.SIM_TYPE_RTS
			_simTypeChangeTo(local_tag.SIM_TYPE_RTS)
	elif key == K_o:
		local_tag.tag_curr_rts_fill_node_type = GM.NODE_TYPE_SEL_OBJ
	elif key == K_b:
		local_tag.tag_curr_rts_fill_node_type = GM.NODE_TYPE_NSEL_OBJ

def _simTypeChangeTo(simType):
	gridMap.resetGridMap()
	pathFinder.clean()
	rtss.reset()
	pass

def _fillNodeUI(screen, font):

	if local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_PF:
		
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

		if local_tag.tag_curr_pf_fill_node_type == GM.NODE_TYPE_START:
			pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabStartCirclePos, local_tag.CIRCLE_RADIUS)
		elif local_tag.tag_curr_pf_fill_node_type == GM.NODE_TYPE_END:
			pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabEndCirclePos, local_tag.CIRCLE_RADIUS)
		elif local_tag.tag_curr_pf_fill_node_type == GM.NODE_TYPE_WALL:
			pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabWallCirclePos, local_tag.CIRCLE_RADIUS)

		screen.blit(tabStart, (30,400))
		screen.blit(tabEnd, (30,425))
		screen.blit(tabWall, (30,450))

	elif local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_RTS:
		
		tabEndCirclePos = (20, 409)
		tabSelCirclePos = (20, 434)
		tabNSelCirclePos = (20, 459)
		tabWallCirclePos = (20, 484)

		tabEnd = uiFont.render("e - set End node", False, local_tag.TEXT_COLOR)
		tabSel = uiFont.render("o - set Sel obj node", False, local_tag.TEXT_COLOR)
		tabNSel = uiFont.render("b - set NSel obj node", False, local_tag.TEXT_COLOR)
		tabWall = uiFont.render("w - set Wall node", False, local_tag.TEXT_COLOR)

		pygame.draw.circle(screen, local_tag.NO_COLOR, tabEndCirclePos, local_tag.CIRCLE_RADIUS)
		pygame.draw.circle(screen, local_tag.NO_COLOR, tabSelCirclePos, local_tag.CIRCLE_RADIUS)
		pygame.draw.circle(screen, local_tag.NO_COLOR, tabNSelCirclePos, local_tag.CIRCLE_RADIUS)
		pygame.draw.circle(screen, local_tag.NO_COLOR, tabWallCirclePos, local_tag.CIRCLE_RADIUS)

		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabEndCirclePos, local_tag.CIRCLE_RADIUS,1)
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabSelCirclePos, local_tag.CIRCLE_RADIUS,1)
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabNSelCirclePos, local_tag.CIRCLE_RADIUS,1)
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabWallCirclePos, local_tag.CIRCLE_RADIUS,1)

		if local_tag.tag_curr_rts_fill_node_type == GM.NODE_TYPE_END:
			pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabEndCirclePos, local_tag.CIRCLE_RADIUS)
		elif local_tag.tag_curr_rts_fill_node_type == GM.NODE_TYPE_SEL_OBJ:
			pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabSelCirclePos, local_tag.CIRCLE_RADIUS)
		elif local_tag.tag_curr_rts_fill_node_type == GM.NODE_TYPE_NSEL_OBJ:
			pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabNSelCirclePos, local_tag.CIRCLE_RADIUS)
		elif local_tag.tag_curr_rts_fill_node_type == GM.NODE_TYPE_WALL:
			pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabWallCirclePos, local_tag.CIRCLE_RADIUS)

		screen.blit(tabEnd, (30,400))
		screen.blit(tabSel, (30,425))
		screen.blit(tabNSel, (30,450))
		screen.blit(tabWall, (30,475))


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

def _rtsTypeUI(screen, font):
	pass

def _simulatorUI(screen, font):
	tabPFCirclePos = (250, 35)
	tabRTSCirclePos = (450, 35)

	tabPF = uiFont.render("p - PathFinder simulator", False, local_tag.TEXT_COLOR)
	tabRTS = uiFont.render("t - RTS simulator", False, local_tag.TEXT_COLOR)

	pygame.draw.circle(screen, local_tag.NO_COLOR, tabPFCirclePos, local_tag.CIRCLE_RADIUS)
	pygame.draw.circle(screen, local_tag.NO_COLOR, tabRTSCirclePos, local_tag.CIRCLE_RADIUS)

	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabPFCirclePos, local_tag.CIRCLE_RADIUS, 1)
	pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabRTSCirclePos, local_tag.CIRCLE_RADIUS, 1)

	if local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_PF:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabPFCirclePos, local_tag.CIRCLE_RADIUS)
	elif local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_RTS:
		pygame.draw.circle(screen, local_tag.CIRCLE_COLOR, tabRTSCirclePos, local_tag.CIRCLE_RADIUS)

	screen.blit(tabPF, (260, 27))
	screen.blit(tabRTS, (460, 27))

def _runUI(screen, font):
	tabRun = uiFont.render("r - run", False, local_tag.TEXT_COLOR)
	screen.blit(tabRun, (10, 30))

	if local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_RTS:
		tabStop = uiFont.render("ctrl+s - stop", False, local_tag.TEXT_COLOR)
		screen.blit(tabStop, (70, 30))

def UIProc(screen, font):
	if not screen or not font:
		return

	_initGridMapUI(screen, font)
	
	_fillNodeUI(screen, font)

	if local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_PF:
		_pfalgorithmTypeUI(screen, font)
	elif local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_RTS:
		_rtsTypeUI(screen, font)
	
	_runUI(screen, font)
	_simulatorUI(screen, font)

def getAlgorithm(atype):
	if atype == local_tag.PFA_TYPE_ASTAR:
		return PFAAS()
	elif atype == local_tag.PFA_TYPE_JPS:
		return PFAJPS()
	elif atype == local_tag.PFA_TYPE_DIJKSTRA:
		return PFAD()
	else:
		return None

def _updatePF(screen, dt):

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == MOUSEBUTTONUP:
			x, y = pygame.mouse.get_pos()
			coord = mapDrawer.getCoordFromPos(x, y)
			if coord is not None:
				pathFinder.clean()

				row, col = coord[0], coord[1]
				if local_tag.tag_curr_pf_fill_node_type == GM.NODE_TYPE_WALL:
					if gridMap.isWallNode(row, col):
						gridMap.setFloorGridNode(row, col)
					else:
						gridMap.setWallGridNode(row, col)
				elif local_tag.tag_curr_pf_fill_node_type == GM.NODE_TYPE_START:
					gridMap.setStartGridNode(row, col)
				elif local_tag.tag_curr_pf_fill_node_type == GM.NODE_TYPE_END:
					gridMap.setEndGridNode(row, col)
		elif event.type == KEYUP:
			keyProc(event.key, event.mod)
			
			if local_tag.tag_should_init_grid_map:
				gridMap.resetGridMap(local_tag.tag_curr_init_grid_map_type)
				local_tag.tag_should_init_grid_map = False

			if local_tag.tag_should_run_algorithm:
				algorithm = getAlgorithm(local_tag.tag_curr_pfa_type)
				if algorithm is not None:
					pathFinder.work(algorithm)
				local_tag.tag_should_run_algorithm = False
	pathFinder.update(dt)


def _updateRTS(screen, dt):

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		elif event.type == MOUSEBUTTONUP:
			x, y = pygame.mouse.get_pos()
			coord = mapDrawer.getCoordFromPos(x, y)

			if coord is not None:
				row, col = coord[0], coord[1]
				rtss.setNode(local_tag.tag_curr_rts_fill_node_type, row, col)
				
		elif event.type == KEYUP:
			keyProc(event.key, event.mod)

			if local_tag.tag_should_init_grid_map:
				gridMap.resetGridMap(local_tag.tag_curr_init_grid_map_type)
				rtss.reset()
				local_tag.tag_should_init_grid_map = False

			if local_tag.tag_should_run_rts_sim:
				rtss.setCurrStatus(RTSS.STATUS_RUNNING)
			else:
				rtss.setCurrStatus(RTSS.STATUS_STOP)

	rtss.update(dt)

def update(screen, uiFont, dt):
	screen.fill((0,0,0))

	UIProc(screen, uiFont)

	if local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_PF:
		_updatePF(screen, dt)
	elif local_tag.tag_curr_sim_type == local_tag.SIM_TYPE_RTS:
		_updateRTS(screen, dt)

if __name__ == "__main__":

	# pygame init
	pygame.init()
	pygame.event.set_blocked(KEYDOWN)

	SCREEN_SIZE = (640, 520)
	screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF, 32)
	screen.fill((0,0,0))

	pygame.display.set_caption("PathFinder - v1.0 @ ShannonXu")

	#init font
	uiFont = pygame.font.SysFont("arial", 20)

	# path finder init
	gridMap = GM(31,56)

	# map drawer
	mapDrawer = MD(pygame, screen, SCREEN_SIZE, gridMap)

	#path finder
	pathFinder = PF()
	pathFinder.setMapDrawer(mapDrawer)

	#maze maker
	mazeMaker = MM()
	gridMap.setMazeMaker(mazeMaker)

	# rts sim
	rtss = RTSS()
	rtss.setMapDrawer(mapDrawer)

	lastTime = time.time()
	while True:
		currTime = time.time()
		update(screen, uiFont, int(round(currTime * 1000)) - int(round(lastTime * 1000)))
		lastTime = currTime
		# pygame.display.update()
		pygame.display.flip()