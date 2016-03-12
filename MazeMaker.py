#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import copy

class MazeMaker(object):

	DIR_VECTOR = [[-2,0],[0,2],[2,0],[0,-2]]

	def __init__(self):
		self.gridMap = None

	def setGridMap(self, gridMap):
		self.gridMap = gridMap

	def genEmptyMap(self):
		if self.gridMap is None:
			return
			
		for x in range(self.gridMap.rows):
			for y in range(self.gridMap.cols):
				self.gridMap.setFloorGridNode(x,y)

	def genRandomMap(self):
		if self.gridMap is None:
			return 
		
		self.genEmptyMap()

		wallNum = self.gridMap.rows * self.gridMap.cols / 3
		n = 0
		while n < wallNum:
			x = random.randint(0, self.gridMap.rows - 1)
			y = random.randint(0, self.gridMap.cols - 1)
			self.gridMap.setWallGridNode(x,y)
			n+=1

	def _genMaze(self, mazeMap, x, y):
		mazeMap[x][y] = True
		dvList = copy.copy(MazeMaker.DIR_VECTOR)
		random.shuffle(dvList)
		for dv in dvList:
			nx = x + dv[0]
			ny = y + dv[1]
			wx = x + dv[0]/2
			wy = y + dv[1]/2
			if nx >= 0 and nx < self.gridMap.rows and ny >= 0 and ny < self.gridMap.cols:
				if not mazeMap[nx][ny]:
					mazeMap[wx][wy] = True
					self._genMaze(mazeMap, nx, ny)

	def genMaze(self):
		if self.gridMap is None:
			return
		mazeMap = [[False for y in range(self.gridMap.cols)] for x in range(self.gridMap.rows)]
		self._genMaze(mazeMap, 0, 0)
		for x in range(self.gridMap.rows):
			for y in range(self.gridMap.cols):
				if mazeMap[x][y]:
					self.gridMap.setFloorGridNode(x, y)
				else:
					self.gridMap.setWallGridNode(x, y)

