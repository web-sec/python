#!python3
#-*-coding:utf-8-*-
def getShotTimes(people_number,shotting_damage,sputtering_damage,health):
    times = 0
    if shotting_damage > sputtering_damage:
        while not isEmpty(health):
            health.sort()
            print(health)
            health[-1] -=shotting_damage
            if health[-1] < 0:
                health[-1] = 0
            for x in range(len(health)-1):
                health[x] -=sputtering_damage
                if health[x] < 0:
                    health[x] = 0
            times+=1
    else:
        while not isEmpty(health):
            health.sort()
            print(health)
            health[0] -=shotting_damage
            if health[0] < 0:
                health[0] = 0
            for x in range(len(health)-1):
                health[x] -=sputtering_damage
                if health[x] < 0:
                    health[x] = 0
            times+=1
    return times

def isEmpty(health):
    m=0
    for x in health:
        if x == 0:
            m+=1
    if m == len(health):
        return True
    else:
        return False

n=10
p=10
q=5
h=[14,3,66,7,31,22,15,18,40,30]
print(getShotTimes(n,p,q,h))
