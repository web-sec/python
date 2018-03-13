#!python3
#-*-utf-8-*-
def main(l):
    for x in range(len(l)):
        l[x] = getNewColor(l,x)
    return l

def getAve(color_list):
    a = 0
    for x in color_list:
        a += x
    return a/len(color_list)

def getNewColor(color_list,location):
    ave_color = getAve(color_list)
    new_color = color_list[location]
    for x in range(len(color_list)):
        distance = abs(x - location)+1
        if color_list[x] < ave_color:
            p_n = -1
        else:
            p_n = 1
        effect = p_n * color_list[x] * ((1/distance)**2)
        new_color += effect
    return new_color

p = [1,2,3,4,5]
for x in range(10):
    np = main(p)
print(np)
