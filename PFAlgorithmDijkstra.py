#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PFAlgorithm import PFAlgorithm as PFA 

class PFAlgorithmDijkstra(PFA):
	''' path find algorithm : Dijkstra '''

	def __init__(self):
		self.pMap = None

	def initPathMap(self, gridMap, distanceType):
		self.pMap = [[0 for y in range(gridMap.cols)] for x in range(gridMap.rows)]
		for x in range(gridMap.rows):
			for y in range(gridMap.cols):
				gridNode = gridMap.getGridNode(x, y)
				if gridNode is not None:
					if gridNode.gnType != GM.NODE_TYPE_WALL:
						if gridMap.isStartGridNode(gridNode.x, gridNode.y):
							self.pMap[x][y] = PN(prev=None, gridNode=gridNode, gv=0)
						else:
							self.pMap[x][y] = PN(prev=None, gridNode=gridNode, gv=PFA.MAX_DISTANCE)
