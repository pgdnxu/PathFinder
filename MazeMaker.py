#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random

class MazeMaker(object):
	def __init(self):
		self.gridMap = None

	def setGridMap(self, gridMap):
		self.gridMap = gridMap

	def genEmptyMap(self):
		if self.gridMap is not None:
			for x in range(self.gridMap.rows):
				for y in range(self.gridMap.cols):
					# self.gMap[x][y].gnType = GridMap.NODE_TYPE_FLOOR
					self.gridMap.setFloorGridNode(x,y)

	def genRandomMap(self):
		if self.gridMap is not None:

			self.genEmptyMap()

			wallNum = self.gridMap.rows * self.gridMap.cols / 3
			n = 0
			while n < wallNum:
				x = random.randint(0, self.gridMap.rows - 1)
				y = random.randint(0, self.gridMap.cols - 1)
				self.gridMap.setWallGridNode(x,y)
				n+=1

	def genMaze(self):
		if self.gridMap is not None:
			pass