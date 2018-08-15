#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

import time

from PFAlgorithm import PFAlgorithm as PFA
from PriorityQueue import PriorityQueue as PQ
from PathNode import PathNode as PN

class PFAlgorithmJPS(PFA):
    ''' path find algorithm : jump point search '''
    def __init__(self):
        self.pMap = None

    def initPathMap(self, gridMap, distanceType):
        endNode = gridMap.getEndGridNode()
        self.pMap = [[0 for y in range(gridMap.cols)] for x in range(gridMap.rows)]
        self.visMap = [[False for y in range(self.gridMap.cols)] for x in range(self.gridMap.rows)]
        for x in range(gridMap.rows):
            for y in range(gridMap.cols):
                gridNode = gridMap.getGridNode(x, y)
                if gridNode is not None:
                    if not gridMap.isWallNode(x, y):
                        hdis = self.getDistance(gridNode, endNode, distanceType)
                        if gridMap.isStartGridNode(gridNode.x, gridNode.y):
                            self.pMap[x][y] = PN(prev=None, gridNode=gridNode, gv=0, hv=hdis)
                        else:
                            self.pMap[x][y] = PN(prev=None, gridNode=gridNode, gv=PFA.MAX_DISTANCE, hv=hdis)

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

    def getAccompanyDir(self, dirType):
        if dirType == self.DIR_5:
            return (self.DIR_1, self.DIR_2)
        elif dirType == self.DIR_6:
            return (self.DIR_2, self.DIR_3)
        elif dirType == self.DIR_7:
            return (self.DIR_3, self.DIR_4)
        elif dirType == self.DIR_8:
            return (self.DIR_4, self.DIR_1)

    def isOkPos(self, gridNode, dv):
        nx = gridNode.x + dv[0]
        ny = gridNode.y + dv[1]

        if not self.gridMap.isValidPos(nx, ny):
            return False

        if self.gridMap.isWallNode(nx, ny):
            return False

        if self.gridMap.isThroughTheWall(gridNode.x, gridNode.y, dv):
            return False

        return True

    def getPathNode(self, gridNode, dv):
        nx = gridNode.x + dv[0]
        ny = gridNode.y + dv[1]

        return self.pMap[nx][ny]       

    def updateJumpNode(self, prevNode, jumpNode, openSet):

        gCost = self.getEuclideanDistance(prevNode.gridNode, jumpNode.gridNode)

        if jumpNode.isInClose:
            if prevNode.gv + gCost < jumpNode.gv:
                jumpNode.isInClose = False
                jumpNode.updatePrev(prevNode, gCost)
                openSet.push(jumpNode)
                jumpNode.isInOpen = True
        else:
            if prevNode.gv + gCost < jumpNode.gv:
                jumpNode.updatePrev(prevNode, gCost)
                if not jumpNode.isInOpen:
                    openSet.push(jumpNode)
                    jumpNode.isInOpen = True
                else:
                    openSet.update(jumpNode)

    def _checkJumpNode(self, testX, testY, obsX, obsY, negNeigX, negNeigY):
        return self.gridMap.isValidPos(testX, testY) and not self.gridMap.isWallNode(testX, testY) and self.gridMap.isWallNode(obsX, obsY) and self.gridMap.isValidPos(negNeigX, negNeigY) and not self.gridMap.isWallNode(negNeigX, negNeigY)

    def isJumpNode(self, gn, dirType):
        if dirType == self.DIR_1:
            # return self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x-1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x-1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y-1)
            return self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x-1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x-1, gn.y+1) 
        elif dirType == self.DIR_2:
            # return self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x-1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x+1, gn.y+1)
            return self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y+1)
        elif dirType == self.DIR_3:
            # return self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x+1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x+1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y-1)
            return self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x+1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x+1, gn.y+1)
        elif dirType == self.DIR_4:
            # return self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x-1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x+1, gn.y-1)
            return self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y-1)
        elif dirType == self.DIR_5:
            return self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x-1, gn.y-1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y+1)
        elif dirType == self.DIR_6:
            return self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x, gn.y-1, gn.x+1, gn.y-1)
        elif dirType == self.DIR_7:
            return self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x+1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x-1, gn.y, gn.x-1, gn.y-1)
        elif dirType == self.DIR_8:
            return self._checkJumpNode(gn.x, gn.y, gn.x, gn.y+1, gn.x-1, gn.y+1) or self._checkJumpNode(gn.x, gn.y, gn.x+1, gn.y, gn.x+1, gn.y-1)
        else:
            return False

    def findJumpNode(self, lastJumpNode, lastNode, testNode, openSet):

        if not testNode:
            return None

        currGridNode = testNode.gridNode

        if self.visMap[currGridNode.x][currGridNode.y]:
            return None

        self.visMap[currGridNode.x][currGridNode.y] = True

        if self.gridMap.isEndGridNode(currGridNode.x, currGridNode.y):
            return testNode

        if testNode.isInOpen:
            return None

        dirType = self.getDirBetweenTwoNode(lastNode.gridNode, currGridNode)
        if self.isJumpNode(currGridNode, dirType):
            # find a jump , then return
            return testNode
        else:
            if dirType == self.DIR_1 or dirType == self.DIR_2 or dirType == self.DIR_3 or dirType == self.DIR_4:
                dv = PFA.DIR_VECTOR[dirType]
                
                if not self.isOkPos(currGridNode, dv):
                    return None

                nextNode = self.getPathNode(currGridNode, dv)

                nextJumpNode = self.findJumpNode(lastJumpNode, testNode, nextNode, openSet)

                return nextJumpNode

            else:
                accDirType1, accDirType2 = self.getAccompanyDir(dirType)

                dv1 = PFA.DIR_VECTOR[accDirType1]
                dv2 = PFA.DIR_VECTOR[accDirType2]
                dv = PFA.DIR_VECTOR[dirType]

                currIsJumpNode = False

                # step 1
                if self.isOkPos(currGridNode, dv1):
                    nextNode = self.getPathNode(currGridNode, dv1)
                    nextJumpNode = self.findJumpNode(lastJumpNode, testNode, nextNode, openSet)
                    if nextJumpNode:
                        if currIsJumpNode:
                            self.updateJumpNode(testNode, nextJumpNode, openSet)
                        else:
                            currIsJumpNode = True
                            self.updateJumpNode(lastJumpNode, testNode, openSet)
                            self.updateJumpNode(testNode, nextJumpNode, openSet)

                # step 2
                if self.isOkPos(currGridNode, dv2):
                    nextNode = self.getPathNode(currGridNode, dv2)
                    nextJumpNode = self.findJumpNode(lastJumpNode, testNode, nextNode, openSet)
                    if nextJumpNode:
                        if currIsJumpNode:
                            self.updateJumpNode(testNode, nextJumpNode, openSet)
                        else:
                            currIsJumpNode = True
                            self.updateJumpNode(lastJumpNode, testNode, openSet)
                            self.updateJumpNode(testNode, nextJumpNode, openSet)


                # step 3
                if self.isOkPos(currGridNode, dv):
                    nextNode = self.getPathNode(currGridNode, dv)
                    nextJumpNode = None
                    nextJumpNode = self.findJumpNode(lastJumpNode, testNode, nextNode, openSet)
                    if nextJumpNode:
                        if currIsJumpNode:
                            self.updateJumpNode(testNode, nextJumpNode, openSet)
                        else:
                            self.updateJumpNode(lastJumpNode, nextJumpNode, openSet)
                    return nextJumpNode

                return None

        return None

    def run(self, gridMap, distanceType=PFA.DIS_TYPE_MANHATTAN):


        if not gridMap:
            return (PFA.RSLT_GRIDMAP_ERR,)

        startNode = gridMap.getStartGridNode()
        if not startNode:
            return (PFA.RSLT_NO_START_NODE,)

        endNode = gridMap.getEndGridNode()
        if not endNode:
            return (PFA.RSLT_NO_END_NODE,)

        hdis = self.getDistance(startNode, endNode, distanceType)
        if hdis < 0:
            return (PFA.RSLT_DIS_INVALID,)

        self.gridMap = gridMap

        self.initPathMap(gridMap, distanceType)

        openSet = PQ()

        startPathNode = self.pMap[startNode.x][startNode.y]
        openSet.push(startPathNode)

        endPathNode = self.pMap[endNode.x][endNode.y]

        ret = (PFA.RSLT_NONE,)
        jumpPoint = []
        while not openSet.isEmpty() and ret[0] == PFA.RSLT_NONE:
            currNode = openSet.pop()
            jumpPoint.append(currNode)
            currNode.isInClose = True
            currGridNode = currNode.gridNode

            if gridMap.isEndGridNode(currGridNode.x, currGridNode.y):
                ret = (PFA.RSLT_OK, self.genValidPath(gridMap), self.genAllVisNodeSet(gridMap), jumpPoint)
                break

            for i in range(len(self.visMap)):
                for j in range(len(self.visMap[i])):
                    self.visMap[i][j] = False

            for dv in PFA.DIR_VECTOR:
                if not self.isOkPos(currGridNode, dv):
                    continue
                jumpNode = self.findJumpNode(currNode, currNode, self.getPathNode(currGridNode, dv), openSet)
                if jumpNode:
                    self.updateJumpNode(currNode, jumpNode, openSet)

        return ret
