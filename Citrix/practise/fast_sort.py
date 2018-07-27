def fast_sort(l,start,end):
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
        fast_sort(l,start,i-1)
        fast_sort(l,i+1,end)
    return l

a=[5,4,3,1,2,3,5,7,77,1,2,43]
print(fast_sort(a,0,11))