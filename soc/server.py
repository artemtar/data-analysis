#!/usr/bin/env python3
import socket
import logging
import sys
from functools import reduce

root = logging.getLogger("")
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

TCP_IP = '127.0.0.1'
TCP_PORT = 4445
BUFFER_SIZE = 1024 
HEADER_LENGTH = 20

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)
    conn, addr = s.accept()
    print ( 'Connection address:', addr )
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        logging.info( "received data from: {}: {}".format(addr, data ))
        decoder(data)
        conn.send(data)  
    # conn.close()

def decoder(data):
    msg = (data[2:]).decode()
    lcheck, spsize = len_check(msg)
    if not lcheck:
        logging.error("Length check fail. Header specified size {}, actuall size {}. Data will be discarded".format(spsize, len(msg) / 2))
        exit(0)
    header_len = int(msg[1], 16) * 4
    if not checksum_check(msg[:header_len + 20]):
        logging.error("Checksum check error, data will be discarded")
        exit(0)
    decode_data(msg[header_len + 20:])

def len_check(msg):
    msg_len = len(msg) / 2
    specified_len = msg[4:8]
    spsize = int(specified_len, 16)
    logging.info("Packet length: {}; packet hex_len: {}".format(int(msg_len), specified_len))
    return spsize == msg_len, spsize

def checksum_check(header):
    splited = []
    for i in range(len(header) // 4):
        splited.append(header[i*4:(i+1)*4])
    splited = map(append_hex, splited)
    csum = reduce(lambda x, y: add_two_hex(x, y), splited)
    fcsum = first_compliment(csum[2:])
    logging.info("Checksum: {}; First compliment: {}".format(csum, fcsum))
    return reduce(lambda x, y: int(x) + int(y), fcsum[2:]) == 0

def decode_data(data):
    decoded = []
    size = len(data) // 2
    for i in range(size):
        data_chank = data[i*2:(i+1)*2]
        decoded.append(bytes.fromhex(str(data_chank)).decode('utf-8'))
    sentence = "".join(decoded)
    logging.info("Msg length: {}".format(len(decoded)))
    logging.info("Encoded data: {}".format(sentence)) 
    return sentence

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

start_server()