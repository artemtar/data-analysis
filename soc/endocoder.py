import binascii
from functools import reduce

test = "COLOMBIA 2 - MESSI 0"

def encode_data(sentence):
    sentence = str(sentence)
    if len(sentence) > 20:
        raise Exception("input size out of bound")
    if len(sentence) < 20:
        missing = 20 - len(sentence)
        for _ in range(missing):
            sentence += " "
    sentence = sentence.encode()
    encoded = []
    size = len(sentence) // 2
    for i in range(size):
        hex_str = binascii.b2a_hex(sentence[i*2:(i+1)*2])
        encoded.append(hex_str)
    return encoded
        
def get_header():
    ipType = '4'
    length = '5'
    tos = '00'
    tottal = ['00' + '28']
    idf = ['1c' +'46']
    flag = '40'
    ofset = '00'
    ttl = '40'
    pf = '06'
    csum = '0x0000'
    src = ['c0' + 'a8', '00' + '03']
    dest = ['c0' + 'a8', '00' + '01']

    head = [append_hex(ipType) + length + tos]
    head += map(append_hex, tottal + idf)
    head += map(append_hex, [flag + ofset, ttl + pf])
    head.append(csum)
    head += map(append_hex, src + dest)
    print(head)
    checksum = reduce(lambda x, y: add_two_hex(x, y), head)
    if len(checksum) < 6:
        missing = 6 - len(checksum)
        full_checksum = '0x'
        for _ in range(missing):
            full_checksum += '0'
        checksum = full_checksum + checksum[2:]
    fc = first_compliment(checksum)
    head[5] = fc
    print(head)
    return head

def first_compliment(hex_num):
    bin_num = bin(int(hex_num, 16))
    if(len(bin_num[2:]) < 16):
        missing = 16 - len(bin_num[2:])
        start = '0b'
        for _ in range(missing):
            start += '0'
        bin_num = start + bin_num[2:]

    bin_list = []
    for e in bin_num[2:]:
        if e == '0':
            bin_list.append('1')
        if e == '1':
            bin_list.append('0')
    bin_first_comp = (reduce(lambda x, y: x + y, bin_list))
    toReturn = hex(int('0b' + bin_first_comp, 2))

    if len(toReturn) < 6:
        start = '0x'
        missing = 6 - len(toReturn)
        for _ in range(missing):
            start += '0'
        toReturn = start + toReturn[2:]
    return toReturn

def append_hex(x):
    return '0x' + x

def add_two_hex(a, b):
    if (len(a) > 6 or len(b) > 6):
        raise Exception('input error')
    a_bin = bin(int(a, 16))[2:]
    b_bin = bin(int(b, 16))[2:]
    missingA = 16 - len(a_bin)
    missingB = 16 - len(b_bin)
    for _ in range(missingA):
        a_bin = '0' + a_bin
    for _ in range(missingB):
        b_bin = '0' + b_bin
    return  hex(int(sum_of_two_bin(a_bin, b_bin), 2))

def add_binary_digits(x,y,c):
    carry = c
    result = ''
    sum = int(x) + int(y) + carry
    if(sum == 0):
        result += '0'
        carry = 0
    if(sum == 1):
        result += '1'
        carry = 0
    if(sum == 2):
        result += '0'
        carry = 1
    if(sum == 3):
        result += '1'
        carry = 1
    return result, carry

def separate_addition(x, y):
    if len(x) == 1:
        return add_binary_digits(x[0], y[0], 0)
    else:
        privRes, privCarry = separate_addition(x[1:], y[1:])
        res, carry = add_binary_digits(x[0], y[0], privCarry)
        return res + privRes, carry

def sum_of_two_bin(x, y):
    first = separate_addition(x, y)
    carry = bin(first[1])[2:]
    for _ in range( 16 - len(carry)):
        carry = '0' + carry
    second = separate_addition(first[0], carry)
    return second[0]

print(get_header() + encode_data(test))