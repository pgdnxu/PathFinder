#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Shannon Xu (pgdninf#gmail.com)

class PriorityItem(object):
    def getPriorityValue(self):
        return 0

class PriorityQueue(object):  
    def __init__(self):  
        self.queue = [0]  
        self.length = 0  
      
    def count(self):  
        return self.length  
      
    def isEmpty(self):  
        return self.count() == 0
        
    def top(self):  
        return self.queue[1]  
      
    def pop(self):  
        if not self.isEmpty():
            ret = self.queue[1] 
            self.queue[1] = self.queue[self.length]  
            self.length -= 1  
            self._adjust()
            return ret
        return None
      
    def _updateAtIndex(self, index):
        while index >= 2 and self.queue[index].getPriorityValue() < self.queue[index/2].getPriorityValue():  
            self.queue[index] , self.queue[index/2] = self.queue[index/2] , self.queue[index]
            index = index / 2
        

    def push(self, item):  
        self.length += 1  
        if len(self.queue) > self.length:
            self.queue[self.length] = item
        else:
            self.queue.insert(self.length, item)

        self._updateAtIndex(self.length)

    def update(self, item):
        if not item:
            return
            
        self._updateAtIndex(self.queue.index(item))        

    def _adjust(self):  
        root = 1  
        j = root << 1  
        temp = self.queue[root]  
        while j <= self.length:  
            if j < self.length and self.queue[j].getPriorityValue() > self.queue[j+1].getPriorityValue():  
                j += 1  
            if self.queue[j].getPriorityValue() > temp.getPriorityValue():  
                break  
            self.queue[j],self.queue[root] = self.queue[root],self.queue[j]  
            root = j  
            j = j << 1  
              
        self.queue[root] = temp  
