
def cap2num(cap):
    return int(ord(cap) - ord('A'))

def num2cap(num):
    return chr(ord('A') + num)

def increment_cap(capnum):
    incremented = ''
    last_ind = len(capnum) - 1
    
    carry = False
    if (capnum[last_ind] == 'Z'):
        incremented.append('A')
        carry = True
        for i in reversed(range(last_ind + 1)):
            if (i > 0):
                if (carry == True):
                    if (capnum[i] == 'Z'):
                        incremented.append('A')
                    else:
                        incremented.append(num2cap(cap2num(capnum[i])+1))
                        carry = False
                else:
                    incremented.append(capnum[i])
        if (carry == True):
            incremented.append('B')
        incremented = reversed(incremented)
    else:
        incremented = capnum
        incremented = incremented[:last_ind] + num2cap(cap2num(capnum[last_ind]) + 1)
    return incremented

def inc(key):
    newkey = 'AAAA000'
    if (key != ''):
        key = str(key)
        key_int = int(key[4:7]) + 1
        key_str = key[0:4]
        if (key_int > 999):
            key_str = increment_cap(key_str)
            key_int = 0
        newkey = f'{key_str}{format(key_int, "03d")}'
    return newkey

def increment_key(key):
    newkey = 'AAAA000'
    if (key != ''):
        pval = 26 * 26 * 26 * 10 * 10 * 10
        keynum = 0
        for i in range(4):
            keynum += int(cap2num(key[i]) * pval)
            pval /= 26
        for i in range(3):
            keynum += int(int(key[i+4]) * pval)
            pval /= 10
            
        keynum += 1

        newkey = ''
        for i in range(3):
            newkey = f'{int(keynum % 10)}{newkey}'
            keynum = int(keynum / 10)
        for i in range (4):
            newkey = f'{num2cap(int(keynum % 26))}{newkey}'
            keynum = int(keynum / 26)

    return newkey
