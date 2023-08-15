import time

def int_to_base62(num):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base62 = ''
    while num:
        num, i = divmod(num, 62)
        base62 = alphabet[i] + base62
    return base62

def t62():
    t = int(time.time() * 1000)
    return int_to_base62(t)

print(int_to_base62(1691726746))