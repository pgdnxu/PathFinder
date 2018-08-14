#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

# from GridMap import GridMap as GM
# from GridNode import GridNode as GN
# from PathNode import PathNode as PN
from PFAlgorithm import PFAlgorithm as PFA
# from PFAlgorithmAStar import PFAlgorithmAStar as PFAAS

class PathFinder(object):
	''' path finder '''
	def __init__(self):
		pass

	def work(self, gridMap, algorithm, mapDrawer=None):
		if not gridMap or not algorithm:
			return False
		# ret = algorithm.run(gridMap,PFA.DIS_TYPE_EUCLIDEAN)
		ret = algorithm.run(gridMap)

		if ret[0] == PFA.RSLT_OK:
			# for item in ret[1]:
			# 	print("%d,%d:%d" % (item.gridNode.x, item.gridNode.y, item.getPriorityValue()))
			if mapDrawer is not None:
				mapDrawer.drawPath(ret[1],ret[2],ret[3])
			return True
		else:
			print("err:%d" % ret[0])
			return False

# if __name__ == "__main__":
# 	gridMap = GM(10,10)
# 	gridMap.setStartGridNode(0,0)
# 	gridMap.setEndGridNode(4,4)

# 	gridMap.setWallGridNode(0,1)
# 	gridMap.setWallGridNode(1,1)
# 	gridMap.setWallGridNode(2,1)
# 	gridMap.setWallGridNode(3,1)

# 	gridMap.setWallGridNode(1,3)
# 	gridMap.setWallGridNode(2,3)
# 	gridMap.setWallGridNode(3,3)
# 	gridMap.setWallGridNode(4,3)

# 	gridMap.printMap()

# 	algorithm = PFAAS()

# 	pathFinder = PathFinder()
# 	pathFinder.work(gridMap,algorithm)