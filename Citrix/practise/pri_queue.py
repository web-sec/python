class Pri_Queue(object):
    def __init__(self, elems=[]):
        self._elems = list(elems)
        self._elems.sort(reverse=True)


p=Pri_Queue([1,2,3,])
print(p._elems)