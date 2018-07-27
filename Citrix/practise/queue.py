class Queue(object):
    def __init__(self,elems=[]):
        self._elems = list(elems)

    def is_empty(self):
        return self._elems == []

    def add(self,e):
        self._elems.append(e)

    def delete(self,index):
        if index < len(self._elems)-1:
            d = self._elems[index]
            del self._elems[index]
            print('{a} is deleted'.format(a=d))
        else:
            print('out of index!')
    def peek(self):
        if self.is_empty():
            print('empty queue!')
            return
        else:
            p = self._elems[0]
            del self._elems[0]
            return p

q=Queue([13,4,5,6])
q.add(9)
q.delete(0)
print(q.peek())