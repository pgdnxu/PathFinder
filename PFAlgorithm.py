#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

class PFAlgorithm(object):

	RSLT_NONE = 0
	RSLT_OK = 1
	RSLT_GRIDMAP_ERR = 2
	RSLT_NO_START_NODE = 3
	RSLT_NO_END_NODE = 4
	RSLT_NO_VALID_PATH = 5
	RSLT_DIS_INVALID = 6

	DIS_TYPE_MANHATTAN = 1
	DIS_TYPE_EUCLIDEAN = 2

	MAX_DISTANCE = 1000000

	DIR_VECTOR = [[-1,0],[0,1],[1,0],[0,-1],[-1,1],[1,1],[1,-1],[-1,-1]]

	def __init__(self):
		pass

	def run(self, gridMap, distanceType):
		return (RSLT_NONE,)

	def getManhattanDistance(self, aNode, bNode):
		if not aNode or not bNode:
			return -1
		return math.fabs(aNode.x-bNode.x)+math.fabs(aNode.y-bNode.y)

	def getEuclideanDistance(self, aNode, bNode):
		if not aNode or not bNode:
			return -1
		return math.sqrt(math.pow(aNode.x-bNode.x,2)+math.pow(aNode.y-bNode.y,2))

	def getDistance(self, aNode, bNode, distanceType):
		if distanceType == PFAlgorithm.DIS_TYPE_MANHATTAN:
			return self.getManhattanDistance(aNode, bNode)
		elif distanceType == PFAlgorithm.DIS_TYPE_EUCLIDEAN:
			return self.getEuclideanDistance(aNode, bNode)
	def getGCost(self, dv):
		if not dv:
			return PFAlgorithm.MAX_DISTANCE
		absum = math.fabs(dv[0])+math.fabs(dv[1])
		if absum == 1:
			return 1
		if absum == 2:
			return 1.41

