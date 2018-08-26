#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

from PFAlgorithm import PFAlgorithm as PFA

class PathFinder(object):
	''' path finder '''
	def __init__(self):
		self.lastRetData = None

	def setMapDrawer(self, mapDrawer=None):
		self.mapDrawer = mapDrawer

	def update(self, dt):
		if self.mapDrawer:
			self.mapDrawer.draw()
		if self.lastRetData:
			if self.mapDrawer:
				self.mapDrawer.drawPath(self.lastRetData[1], self.lastRetData[2], self.lastRetData[3])

	def clean(self):
		self.lastRetData = None

	def work(self, algorithm):
		if not algorithm:
			return False

		self.lastRetData = algorithm.run(self.mapDrawer.getGridMap())

		if self.lastRetData[0] == PFA.RSLT_OK:
			return True
		else:
			print("err:%d" % self.lastRetData[0])
			self.clean()
			return False
