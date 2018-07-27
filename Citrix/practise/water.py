def drink_water(n):
    has_drink = n
    empty = n
    while empty > 1:
        print(empty)
        if empty%2==0:
            has_drink += empty//2
            empty = empty//2
        else:
            has_drink += empty//2
            empty = empty//2 + 1
    return has_drink

print(drink_water(20))