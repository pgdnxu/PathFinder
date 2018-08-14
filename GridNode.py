#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

class GridNode(object):
	'''	grid node info data'''

	def __init__(self, x, y, gnType):
		self.gnType = gnType
		self.x = x
		self.y = y
