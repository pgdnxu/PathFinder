#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

from PFAlgorithmAStar import PFAlgorithmAStar as PFAAS
from GridMap import GridMap as GM
from SmartObj import SmartObj as SO
from PFAlgorithm import PFAlgorithm as PFA
import random

class RTSSim(object):

    STATUS_STOP = 1
    STATUS_RUNNING = 2

    SPEED_MSEC = 100

    def __init__(self):
        self.mapDrawer = None
        self.gridMap = None
        self.dtSum = 0
        self.nselObjList = []
        self.selObj = None
        self.currStatus = RTSSim.STATUS_STOP
        self.pfaas = PFAAS()
        self.noFindNum = 0

    def getCurrStatus(self):
        return self.currStatus

    def setCurrStatus(self, status):
        if self.currStatus != status:
            if status == RTSSim.STATUS_STOP:
                self.reset()
        self.currStatus = status

    def setMapDrawer(self, mapDrawer):
        self.mapDrawer = mapDrawer
        if mapDrawer is not None:
            self.gridMap = mapDrawer.getGridMap()

    def reset(self):

        for obj in self.nselObjList:
            self.gridMap.setFloorGridNode(obj.getX(), obj.getY())
        self.nselObjList = []
        if self.selObj is not None:
            self.gridMap.setFloorGridNode(self.selObj.getX(), self.selObj.getY())
            self.selObj = None


    def _setEndNode(self, row, col):
        if self.gridMap.isFloorNode(row, col):
            self.gridMap.setEndGridNode(row, col)

    def _setWallNode(self, row, col):
        if self.gridMap.isWallNode(row, col):
            self.gridMap.setFloorGridNode(row, col)
        elif self.gridMap.isFloorNode(row, col):
            self.gridMap.setWallGridNode(row, col)

    def _setSelObjNode(self, row, col):
        if self.gridMap.isFloorNode(row, col):

            if self.selObj is not None:
                self.gridMap.setFloorGridNode(self.selObj.getX(), self.selObj.getY())
                self.selObj = None

            self.selObj = SO(self.gridMap, row, col, True)
            self.gridMap.setSelObjGridNode(row, col)

    # def _updateSelObjNode(self, row, col):
        

    def _setNSelObjNode(self, row, col):
        if self.gridMap.isNSelObjGridNode(row, col):
            delObj = None
            for obj in self.nselObjList:
                if obj.getX() == row and obj.getY() == col:
                    delObj = obj
                    break
            if delObj is not None:
                self.nselObjList.remove(delObj)
                self.gridMap.setFloorGridNode(delObj.getX(), delObj.getY())
        elif self.gridMap.isFloorNode(row, col):
            nselObj = SO(self.gridMap, row, col, False)
            self.nselObjList.append(nselObj)
            self.gridMap.setNSelObjGridNode(row, col)

    # def _updateNSelObjNode(self, row, col):
        # pass

    def setNode(self, nodeType, row, col):
        if nodeType == GM.NODE_TYPE_END:
            self._setEndNode(row, col)
        else:
            self.setCurrStatus(RTSSim.STATUS_STOP)
            if nodeType == GM.NODE_TYPE_WALL:
                self._setWallNode(row, col)
            elif nodeType == GM.NODE_TYPE_SEL_OBJ:
                self._setSelObjNode(row, col)
            elif nodeType == GM.NODE_TYPE_NSEL_OBJ:
                self._setNSelObjNode(row, col)

    def moveAPath(self, selObj, nselObjOnPathList):

        # print("===================================")

        # for item in nselObjOnPathList:
        #     print(item.getX(), item.getY())

        nselObjOnPathSet = set()
        
        for dv in PFA.DIR_VECTOR:
            nx = selObj.getX() + dv[0]
            ny = selObj.getY() + dv[1]
            for obj in self.nselObjList:
                if obj.getX() == nx and obj.getY() == ny:
                    nselObjOnPathSet.add(obj)

        for i in range(random.randint(1,5)):
            rSecList = [obj for obj in nselObjOnPathSet]

            for obj1 in rSecList:
                for dv in PFA.DIR_VECTOR:
                    nx = obj1.getX() + dv[0]
                    ny = obj1.getY() + dv[1]
                    for obj2 in self.nselObjList:
                        if obj2.getX() == nx and obj2.getY() == ny:
                            nselObjOnPathSet.add(obj2)

        for obj1 in nselObjOnPathList:
            for dv in PFA.DIR_VECTOR:
                nx = obj1.getX() + dv[0]
                ny = obj1.getY() + dv[1]
                for obj2 in self.nselObjList:
                    if obj2.getX() == nx and obj2.getY() == ny:
                        nselObjOnPathSet.add(obj2)

        for i in range(random.randint(1,5)):
            rSecList = [obj for obj in nselObjOnPathSet]

            for obj1 in rSecList:
                for dv in PFA.DIR_VECTOR:
                    nx = obj1.getX() + dv[0]
                    ny = obj1.getY() + dv[1]
                    for obj2 in self.nselObjList:
                        if obj2.getX() == nx and obj2.getY() == ny:
                            nselObjOnPathSet.add(obj2)

        cantMoveNum = 0

        if self.noFindNum >= random.randint(3,15):
            for i in range(random.randint(1,5)):
                selObj._turn()
            self.noFindNum = 0

        if not selObj.moveOneStep():
            cantMoveNum += 1

        for obj in nselObjOnPathSet:
            if not obj.moveOneStep():
                cantMoveNum += 1

        if cantMoveNum == len(nselObjOnPathSet) + 1:
            return False
        return True

    def moveAPath2(self, selObj, onPathList):

        endNode = self.gridMap.getEndGridNode()
        if endNode is None:
            return False

        cantMoveNum = 0
        if not selObj.moveOneStepAwayFrom(endNode.x, endNode.y):
            cantMoveNum += 1

        # for obj in self.nselObjList:
        if onPathList is None:
            onPathList = self.nselObjList

        for obj in onPathList:
            if not obj.moveOneStepAwayFrom(endNode.x, endNode.y):
                cantMoveNum += 1

        if cantMoveNum == len(self.nselObjList) + 1:
            return False

        return True

    def work(self):
        if self.selObj is not None:

            self.gridMap.openRtsMode()
            ret = self.pfaas.run(self.gridMap, self.gridMap.getGridNode(self.selObj.getX(), self.selObj.getY()))

            if ret[0] == PFA.RSLT_OK:
                # 找到一条路径，可以不需要让队友让路即可到达终点
                pathNodeList = ret[1]
                listLen = len(pathNodeList)
                if listLen > 1:
                    self._setSelObjNode(pathNodeList[-2].gridNode.x, pathNodeList[-2].gridNode.y)
            
            elif ret[0] == PFA.RSLT_NONE:
                self.noFindNum += 1
                #没有直达路径，需要队友让路
                self.gridMap.closeRtsMode()
                ret2 = self.pfaas.run(self.gridMap, self.gridMap.getGridNode(self.selObj.getX(), self.selObj.getY()))

                if ret2[0] == PFA.RSLT_OK:
                    pathNodeList = ret2[1]
                    listLen = len(pathNodeList)
                    if listLen > 1:
                        nextNode = pathNodeList[-2]
                        if nextNode.gridNode.gnType == GM.NODE_TYPE_NSEL_OBJ:
                            
                            onPathList = []
                            for i1 in self.nselObjList:
                                for i2 in pathNodeList:
                                    if i1.getX() == i2.gridNode.x and i1.getY() == i2.gridNode.y:
                                        # onPathList.add(i1)
                                        onPathList.append(i1)

                            self.gridMap.openRtsMode()
                            
                            moveRet = False

                            rand = random.randint(1, 10)

                            if rand > 4:
                                moveRet = self.moveAPath(self.selObj, onPathList)
                            elif rand > 1 and rand <= 4:
                                moveRet = self.moveAPath2(self.selObj, onPathList)
                            elif rand == 1:
                                moveRet = self.moveAPath2(self.selObj, None)

                            if not moveRet:
                                return

                        else:
                            self._setSelObjNode(nextNode.gridNode.x, nextNode.gridNode.y)

            else:
                print("err:%d" % ret[0])

    def update(self, dt):
        if self.mapDrawer is not None:
            self.mapDrawer.draw()
        if self.currStatus == RTSSim.STATUS_RUNNING:
            self.dtSum += dt
            if self.dtSum >= RTSSim.SPEED_MSEC:
                self.work()
                self.dtSum %= RTSSim.SPEED_MSEC


