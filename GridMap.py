#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import GridNode as gn
import math

class GridMap(object):
	''' the grid map '''
	
	INIT_TYPE_EMPTY = 1
	INIT_TYPE_RANDOM = 2
	INIT_TYPE_MAZE = 3

	NODE_TYPE_FLOOR = 1
	NODE_TYPE_WALL = 2
	NODE_TYPE_START = 3
	NODE_TYPE_END = 4


	def __init__(self, rows, cols, gmiType=INIT_TYPE_EMPTY, mazeMaker=None):
		self.rows = rows
		self.cols = cols
		
		self.hasStartNode = False
		self.hasEndNode = False

		self.setMazeMaker(mazeMaker)

		self.gMap = [[0 for y in range(cols)] for x in range(rows)]
		for x in range(rows):
			for y in range(cols):
				self.gMap[x][y] = gn.GridNode(x, y, GridMap.NODE_TYPE_FLOOR)

		self.resetGridMap(gmiType)

	def setMazeMaker(self, mazeMaker):
		if not mazeMaker:
			self.mazeMaker = None
			return
		self.mazeMaker = mazeMaker
		self.mazeMaker.setGridMap(self)

	def printMap(self):
		for x in range(self.rows):
			for y in range(self.cols):
				node = self.gMap[x][y]
				if node.gnType == GridMap.NODE_TYPE_FLOOR:
					print('.', end='')
				elif node.gnType == GridMap.NODE_TYPE_WALL:
					print('#', end='')
				elif node.gnType == GridMap.NODE_TYPE_START:
					print('s', end='')
				elif node.gnType == GridMap.NODE_TYPE_END:
					print('e', end='')
				else:
					print('x', end='')
			print()

	def isValidPos(self, x, y):
		if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
			return False
		return True

	def _clearStartEndNode(self, x, y):
		if self.isStartGridNode(x, y):
			self.removeStartGridNode()
		if self.isEndGridNode(x, y):
			self.removeEndGridNode()

	def setFloorGridNode(self, x, y):
		self._clearStartEndNode(x, y)
		self._setGridNodeType(x, y, GridMap.NODE_TYPE_FLOOR)

	def setWallGridNode(self, x, y):
		self._clearStartEndNode(x, y)
		self._setGridNodeType(x, y, GridMap.NODE_TYPE_WALL)

	def isStartGridNode(self, x, y):
		return self.hasStartNode and x == self.sNode.x and y == self.sNode.y

	def removeStartGridNode(self):
		if self.hasStartNode:
			self.hasStartNode = False
			self._setGridNodeType(self.sNode.x, self.sNode.y, GridMap.NODE_TYPE_FLOOR)

	def getStartGridNode(self):
		if self.hasStartNode:
			return self.sNode
		return None

	def setStartGridNode(self, x, y):
		if self.hasStartNode:
			self.removeStartGridNode()
		self.hasStartNode = True
		self.sNode = self.gMap[x][y]
		self._setGridNodeType(x, y, GridMap.NODE_TYPE_START)

	def isEndGridNode(self, x, y):
		return self.hasEndNode and x == self.eNode.x and y == self.eNode.y

	def removeEndGridNode(self):
		if self.hasEndNode:
			self.hasEndNode = False
			self._setGridNodeType(self.eNode.x, self.eNode.y, GridMap.NODE_TYPE_FLOOR)

	def getEndGridNode(self):
		if self.hasEndNode:
			return self.eNode
		return None

	def setEndGridNode(self, x, y):
		if self.hasEndNode:
			self.removeEndGridNode()
		self.hasEndNode = True
		self.eNode = self.gMap[x][y]
		self._setGridNodeType(x, y, GridMap.NODE_TYPE_END)

	def getGridNode(self, x, y):
		if not self.isValidPos(x, y):
			return None
		return self.gMap[x][y]

	def isWallNode(self, x, y):
		node = self.getGridNode(x, y)
		if not node:
			return False
		if node.gnType == GridMap.NODE_TYPE_WALL:
			return True
		return False

	def _setGridNodeType(self, x, y, gnType):
		if self.isValidPos(x, y):
			self.gMap[x][y].gnType = gnType

	def resetGridMap(self, gmiType=INIT_TYPE_EMPTY):

		if self.hasStartNode:
			self.removeStartGridNode()
		if self.hasEndNode:
			self.removeEndGridNode()

		if gmiType == GridMap.INIT_TYPE_EMPTY:
			self._genEmptyGridMap()
		elif gmiType == GridMap.INIT_TYPE_RANDOM:
			self._genRandomGridMap()
		elif gmiType == GridMap.INIT_TYPE_MAZE:
			self._genMazeGridMap()

	def isThroughTheWall(self, x, y, dv):
		if not dv:
			return False
		dcost = math.fabs(dv[0]) + math.fabs(dv[1])
		if dcost != 2:
			return False
		if self.isWallNode(x+dv[0], y) and self.isWallNode(x, y+dv[1]):
			return True
		return False

	def _genEmptyGridMap(self):
		if self.mazeMaker is not None:
			self.mazeMaker.genEmptyMap()

	def _genRandomGridMap(self):
		if self.mazeMaker is not None:
			self.mazeMaker.genRandomMap()

	def _genMazeGridMap(self):
		if self.mazeMaker is not None:
			self.mazeMaker.genMaze()