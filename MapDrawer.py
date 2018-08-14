#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

import math

class MapDrawer(object):
	''' draw map UI on the screen'''
	GRID_SIDE_LEN = 10

	COLOR_FRAME = (12,120,12)
	COLOR_LINE = (3,30,3)
	COLOR_WALL = (8,80,8)
	COLOR_FLOOR = (0,0,0)
	COLOR_START = (150,30,10)
	COLOR_END = (10,30,150)
	COLOR_PATH_LINE = (150,150,150)
	COLOR_VIS_PATH_LINE = (50,50,50)

	def __init__(self, pygame, screen, screenSize, gridMap):
		self.pygame = pygame
		self.screen = screen
		# self.screenWidth = screenSize[0]
		# self.screenHeight = screenSize[1]
		self.screenSize = screenSize

		self.startPoint = (10,50)
		self.drawRect = (617,342)
		self.gridMap = gridMap

		self.sLineLen = self.drawRect[1] - 3
		self.hLineLen = self.drawRect[0] - 3

		self.sLineNum = self.gridMap.cols - 1
		self.hLineNum = self.gridMap.rows - 1


	def draw(self):
		if self.screen is None:
			return

		self.pygame.draw.rect(self.screen, MapDrawer.COLOR_FRAME,(self.startPoint,self.drawRect), 1)

		offsetY = MapDrawer.GRID_SIDE_LEN + 1
		for i in range(self.sLineNum):
			self.pygame.draw.line(self.screen, MapDrawer.COLOR_LINE, (self.startPoint[0]+offsetY,self.startPoint[1]+1),(self.startPoint[0]+offsetY, self.startPoint[1]+1+self.sLineLen),1)
			offsetY += MapDrawer.GRID_SIDE_LEN + 1

		offsetX = MapDrawer.GRID_SIDE_LEN + 1
		for j in range(self.hLineNum):
			self.pygame.draw.line(self.screen, MapDrawer.COLOR_LINE, (self.startPoint[0]+1,self.startPoint[1]+offsetX),(self.startPoint[0]+1+self.hLineLen,self.startPoint[1]+offsetX),1)
			offsetX += MapDrawer.GRID_SIDE_LEN + 1			

		# draw grid
		for x in range(self.gridMap.rows):
			for y in range(self.gridMap.cols):
				drawColor = MapDrawer.COLOR_FLOOR
				if self.gridMap.isWallNode(x, y):
					drawColor = MapDrawer.COLOR_WALL
				elif self.gridMap.isStartGridNode(x, y):
					drawColor = MapDrawer.COLOR_START
				elif self.gridMap.isEndGridNode(x, y):
					drawColor = MapDrawer.COLOR_END

				self.pygame.draw.rect(self.screen, drawColor, ((y*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[0],x*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[1]),(MapDrawer.GRID_SIDE_LEN, MapDrawer.GRID_SIDE_LEN)))

	def drawPath(self, pathNodes, visNodes):

		bigestStep = 1
		if visNodes:
			for node in visNodes:
				if node.gv > bigestStep:
					bigestStep=node.gv

		if visNodes:
			for node in visNodes:
				prev = node.prev
				if prev is not None:
					nodeGrid = node.gridNode
					prevGrid = prev.gridNode
					colorR = float(node.gv) / bigestStep
					self.pygame.draw.line(self.screen, (int(255*colorR), 50, 100), (nodeGrid.y*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[0]+MapDrawer.GRID_SIDE_LEN/2,nodeGrid.x*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[1]+MapDrawer.GRID_SIDE_LEN/2),(prevGrid.y*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[0]+MapDrawer.GRID_SIDE_LEN/2,prevGrid.x*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[1]+MapDrawer.GRID_SIDE_LEN/2),1)

		if pathNodes:
			for node in pathNodes:
				prev = node.prev
				if prev is not None:
					nodeGrid = node.gridNode
					prevGrid = prev.gridNode
					self.pygame.draw.line(self.screen, MapDrawer.COLOR_PATH_LINE, (nodeGrid.y*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[0]+MapDrawer.GRID_SIDE_LEN/2,nodeGrid.x*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[1]+MapDrawer.GRID_SIDE_LEN/2),(prevGrid.y*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[0]+MapDrawer.GRID_SIDE_LEN/2,prevGrid.x*(MapDrawer.GRID_SIDE_LEN+1)+1+self.startPoint[1]+MapDrawer.GRID_SIDE_LEN/2),2)


	def getCoordFromPos(self, x, y):
		x = x - self.startPoint[0]
		y = y - self.startPoint[1]
		if x <= 0 or x >= self.drawRect[0] or y <= 0 or y >= self.drawRect[1]:
			return None
		if (x - 1)%(MapDrawer.GRID_SIDE_LEN + 1) == 0 or (y - 1)%(MapDrawer.GRID_SIDE_LEN + 1) == 0:
			return None
		return (int(math.floor(y/(MapDrawer.GRID_SIDE_LEN + 1))), int(math.floor(x/(MapDrawer.GRID_SIDE_LEN + 1))))





