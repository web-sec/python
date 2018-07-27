def fast_sort(l,start,end,index):
    if start<end:
        i=start
        j=end
        base=l[start]
        while i<j:
            while i<j and l[j]>=base:
                j-=1
            l[i] = l[j]
            while i<j and l[i]<=base:
                i+=1
            l[j] = l[i]
        l[i] = base
        if i+1 == index:
            return l[i]
        else:
            if i<index:
                fast_sort(l, i + 1, end,index)
            if i>index:
                fast_sort(l,start,i-1,index)



def foo(l,start,end,index):
    if start < end:
        i = start
        j = end
        base = l[index]
        while i < j:
            while i < j and l[j] >= base:
                j -= 1
            while i < j and l[i] <= base:
                i += 1
            temp = l[i]
            l[i] = l[j]
            l[j] = temp
        temp = l[i]
        l[i] = base
        l[index] = temp
        return i

a=[5,4,3,1,2,3,5,7,77,1,2,43]
print(foo(a,0,11,11))