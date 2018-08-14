#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com) 
 
from PFAlgorithm import PFAlgorithm as PFA
from PriorityQueue import PriorityQueue as PQ
from PathNode import PathNode as PN

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
					# if gridNode.gnType != GM.NODE_TYPE_WALL:
					if not gridMap.isWallNode(x, y):
						if gridMap.isStartGridNode(gridNode.x, gridNode.y):
							self.pMap[x][y] = PN(prev=None, gridNode=gridNode, gv=0)
						else:
							self.pMap[x][y] = PN(prev=None, gridNode=gridNode, gv=PFA.MAX_DISTANCE)
	def genValidPath(self, gridMap):
		retSet = []
		endGridNode = gridMap.getEndGridNode()
		endPathNode = self.pMap[endGridNode.x][endGridNode.y]
		retSet.append(endPathNode)
		prevPathNode = endPathNode.prev
		while prevPathNode is not None:
			retSet.append(prevPathNode)
			prevPathNode = prevPathNode.prev
		# retSet.reverse()
		return retSet

	def genAllVisNodeSet(self, gridMap):
		retSet = []
		for x in range(gridMap.rows):
			for y in range(gridMap.cols):
				pathNode = self.pMap[x][y]
				if pathNode:
					if pathNode.isInClose:
						retSet.append(pathNode)
		return retSet

	def run(self, gridMap, distanceType=PFA.DIS_TYPE_MANHATTAN):
		if not gridMap:
			return (PFA.RSLT_GRIDMAP_ERR,)

		startNode = gridMap.getStartGridNode()
		if not startNode:
			return (PFA.RSLT_NO_START_NODE,)

		endNode = gridMap.getEndGridNode()
		if not endNode:
			return (PFA.RSLT_NO_END_NODE,)

		# hdis = self.getDistance(startNode, endNode, distanceType)
		# if hdis < 0:
		# 	return (PFA.RSLT_DIS_INVALID,)

		self.initPathMap(gridMap, distanceType)

		closeSet = PQ()

		startPathNode = self.pMap[startNode.x][startNode.y]
		closeSet.push(startPathNode)

		endPathNode = self.pMap[endNode.x][endNode.y]
		endPathNode.isInClose = True

		ret = (PFA.RSLT_NONE,)
		while not closeSet.isEmpty() and ret[0] == PFA.RSLT_NONE:
			currNode = closeSet.pop()
			currNode.isInClose = True

			# print("%d,%d,%d" % (currNode.gridNode.x, currNode.gridNode.y,currNode.fv))

			currGridNode = currNode.gridNode

			for dv in PFA.DIR_VECTOR:
				
				nx = currGridNode.x + dv[0]
				ny = currGridNode.y + dv[1]
				
				if not gridMap.isValidPos(nx, ny):
					continue

				if gridMap.isThroughTheWall(currGridNode.x, currGridNode.y, dv):
					continue

				gCost = self.getGCost(dv)

				if gridMap.isEndGridNode(nx, ny):
					endPathNode.updatePrev(currNode, gCost)
					ret = (PFA.RSLT_OK, self.genValidPath(gridMap), self.genAllVisNodeSet(gridMap), None)
					break

				newNode = self.pMap[nx][ny]
				
				if newNode:
					if not newNode.isInClose:
						newNode.isInClose = True
						closeSet.push(newNode)

					if currNode.gv + gCost < newNode.gv:
						newNode.updatePrev(currNode, gCost)
						closeSet.update(newNode)

					# if newNode.isInClose:
					# 	if currNode.gv + gCost < newNode.gv:
					# 		newNode.isInClose = False
					# 		newNode.updatePrev(currNode, gCost)
					# 		openSet.push(newNode)
					# 		newNode.isInOpen = True
					# else:
					# 	if currNode.gv + gCost < newNode.gv:
					# 		newNode.updatePrev(currNode, gCost)
					# 		if not newNode.isInOpen:
					# 			openSet.push(newNode)
					# 			newNode.isInOpen = True
					# 		else:
					# 			openSet.update(newNode)
		return ret
