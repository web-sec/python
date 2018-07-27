#coding:utf-8
#!python3
class Node(object):
    def __init__(self,data = None,left = None,right = None):
        self.data = data
        self.left = left
        self.right = right

class BinaryTree(object):
    def __init__(self,root = None):
        self.root = root

    def is_empty(self):
        return self.root == None

    def pre_order(self,node):
        if node is None:
            return
        self.pre_order(node.left)
        print(node.data)
        self.pre_order(node.right)
n4 = Node('D')
n5 = Node('E')
n6 = Node('F')
n7 = Node('G')

n2 = Node('B',n4,n5)
n3 = Node('C',n6,n7)
n1 = Node('A',n2,n3)
t = BinaryTree(n1)
t.pre_order(n1)