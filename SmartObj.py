#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

import math
from PFAlgorithm import PFAlgorithm as PFA

class SmartObj(object):
    ID = 0
    def __init__(self, gridMap, x=0, y=0, isSelected=False):
        self.isSelected = isSelected
        self.x = x
        self.y = y
        self.gridMap = gridMap
        self.defDIR = PFA.DIR_1
        self.currDIR = PFA.DIR_1
        self.id = SmartObj.ID
        SmartObj.ID += 1

    def getID(self):
        return self.id

    def _turn(self):
        if self.currDIR == PFA.DIR_1:
            self.currDIR = PFA.DIR_2
        elif self.currDIR == PFA.DIR_2:
            self.currDIR = PFA.DIR_3
        elif self.currDIR == PFA.DIR_3:
            self.currDIR = PFA.DIR_4
        elif self.currDIR == PFA.DIR_4:
            self.currDIR = PFA.DIR_5
        elif self.currDIR == PFA.DIR_5:
            self.currDIR = PFA.DIR_6
        elif self.currDIR == PFA.DIR_6:
            self.currDIR = PFA.DIR_7
        elif self.currDIR == PFA.DIR_7:
            self.currDIR = PFA.DIR_8
        elif self.currDIR == PFA.DIR_8:
            self.currDIR = PFA.DIR_1

    def updateCoord(self, nx, ny):
        self.x = nx
        self.y = ny

    def _tryStep(self):

        dv = PFA.DIR_VECTOR[self.currDIR]
        
        nx = self.x + dv[0]
        ny = self.y + dv[1]
                
        if not self.gridMap.isFloorNode(nx, ny) or not self.gridMap.isValidPos(nx, ny) or self.gridMap.isThroughTheWall(self.x, self.y, dv):
            self._turn()
        else:
            self.gridMap.setFloorGridNode(self.x, self.y)
            self.updateCoord(nx, ny)
            if self.isSelected:
                self.gridMap.setSelObjGridNode(self.x, self.y)
            else:
                self.gridMap.setNSelObjGridNode(self.x, self.y)
            return True
        return False

    def moveOneStep(self):

        if self._tryStep():
            return True

        while self.currDIR != self.defDIR:
            if self._tryStep():
                return True

        return False

    def _getDistance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))

    def moveOneStepAwayFrom(self, x, y):

        disMax = -1
        currDv = None
        for dv in PFA.DIR_VECTOR:
            nx = self.x + dv[0]
            ny = self.y + dv[1]
            if self.gridMap.isFloorNode(nx, ny) and self.gridMap.isValidPos(nx, ny) and not self.gridMap.isThroughTheWall(self.x, self.y, dv):
                dis = self._getDistance(nx, ny, x, y)
                if dis > disMax:
                    disMax = dis
                    currDv = dv

        if currDv is not None:
            nx = self.x + currDv[0]
            ny = self.y + currDv[1]

            self.gridMap.setFloorGridNode(self.x, self.y)
            self.updateCoord(nx, ny)
            if self.isSelected:
                self.gridMap.setSelObjGridNode(self.x, self.y)
            else:
                self.gridMap.setNSelObjGridNode(self.x, self.y)
            return True
        return False

    def isSelected(self):
        return self.isSelected

    def getX(self):
        return self.x

    def getY(self):
        return self.y


