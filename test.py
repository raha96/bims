from serialfuncs import *

key = 'AAAA000'

for i in range(100):
    for j in range(100):
        key = inc(key)
    print(key)
