#*************************************
#Author : Santosh Kumar Desai
#ID : 2017H1030130P
#*************************************

import copy
class Node:
    parent = None
    child_nodes=[]

    def __init__(self, state, pos, parent, action, depth):
        self.state = copy.deepcopy(state)
        self.pos = pos
        self.parent = parent
        self.action = action
        self.depth = depth
        if self.state:
            self._hash_ = ''.join(self.compress(e) for e in self.state)
        self.addChildNode(parent,self)

    def addChildNode(self,parent,child):
        if parent is not None:
            parent.child_nodes.insert(0,child)

    def compress(self,entity):
        if entity:
            return '1'
        else:
            return '0'

# class State2:
#     parent = None
#     child_nodes=[]

#     def __init__(self, state, pos, parent, action, depth):
#         self.state = copy.deepcopy(state)
#         self.pos = pos
#         self.parent = parent
#         self.action = action
#         self.depth = depth
#         if self.state:
#             self._hash_ = ''.join(self.compress(e) for e in self.state)
#             self._hash_ += ","+str(self.pos)
#         self.addChildNode(parent,self)

#     def addChildNode(self,parent,child):
#         if parent is not None:
#             parent.child_nodes.insert(0,child)

#     def compress(self,entity):
#         if entity:
#             return '1'
#         else:
#             return '0'