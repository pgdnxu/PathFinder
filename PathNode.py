#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

from PriorityQueue import PriorityItem

class PathNode(PriorityItem):
	''' path node '''
	def __init__(self, prev, gridNode, gv, hv=0):
		self.prev = prev
		self.gridNode = gridNode
		self.gv = gv
		self.hv = hv
		self.fv = gv + hv
		self.isInClose = False
		self.isInOpen = False

	def updatePrev(self, prev, gCost):
		if not prev:
			return

		self.prev = prev
		self.gv = prev.gv + gCost
		self.fv = self.gv + self.hv

	def getPriorityValue(self):
		return self.fv


