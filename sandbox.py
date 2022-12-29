g = 9.8

def down_data(h):
    t = 0
    while h > 0:
        t += .0001
        h = -4.9*t**2 + 1
        v = g*t
        yield h, v

print()