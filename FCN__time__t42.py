import time

def int_to_base42(num):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEF'
    base42 = ''
    while num:
        num, i = divmod(num, 42)
        base42 = alphabet[i] + base42
    return base42

def t42():
    return int_to_base42(int(time.time() * 1000))