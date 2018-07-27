#coding:utf-8
#!python3
class Node():
    def __init__(self,data,next=None):
        self.data = data
        self.next = next

class LinkList():
    def __init__(self,head=None):
        self.head = head

    def is_empty(self):
        return self.head == None

    def get_list_length(self):
        list_length = 0
        if self.is_empty():
            return list_length
        else:
            list_length += 1
            p = self.head
            while p.next is not None:
                p = p.next
                list_length += 1
            return list_length

    def print_list(self):
        p = self.head
        l = [p.data]
        while p.next is not None:
            p = p.next
            l.append(p.data)
        print(l)

    def get_data_by_index(self,index):
        list_length = self.get_list_length()
        if index < 0 or index > list_length:
            print("index out of range! total {l} nodes in this list!".format(l=list_length))
            return
        else:
            p = self.head
            for i in range(index-1):
                p = p.next
            return p.data

    def append(self,date):
        node = Node(date)
        if self.is_empty():
           self.head = node
        else:
            next_node = self.head
            while next_node.next is not None:
                next_node = next_node.next
            next_node.next = node
    def delete(self):
        if self.is_empty():
            print("this list is already empty!")
        else:
            list_length = self.get_list_length()
            if list_length == 1:
                self.head = None
            else:
                p = self.head
                for i in range(list_length-2):
                    p = p.next
                p.next = None
            print("last node has been deleted!")
    def insert(self,index,data):
        node = Node(data)
        list_length = self.get_list_length()
        if index > list_length+1 or index < 1:
            print("index out of range! total {l} nodes in list!".format(l=list_length))
        elif index == list_length+1:
            self.append(data)
        elif index == 1 :
            p = self.head
            self.head = node
            node.next = p
        else:
            p = self.head
            for i in range(index-2):
                p = p.next
            temp = p.next
            p.next = node
            node.next = temp
    def remove(self,index):
        list_length = self.get_list_length()
        if index > list_length:
            print("list out of range! total {l} nodes! in list".format(l=list_length))
        elif index == 1:
            p = self.head.next
            self.head = p
        else:
            p = self.head
            for i in range(index-2):
                p = p.next
            temp = p.next.next#the next node of the removed node
            p.next = temp


if __name__ == "__main__":
    n1 = Node(5)
    l = LinkList(n1)
    l.append(4)
    l.append(3)
    l.append(2)
    l.append(1)
    l.print_list()
    l.remove(1)
    l.print_list()