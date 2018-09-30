# -*- coding:utf-8 -*-

import base64
import marshal
import random

def __ext_euclid(a, b):
    i = -1
    list_r = list()
    list_q = list()
    list_x = list()
    list_y = list()

    i += 1
    list_r.append(a)
    list_r.append(b)

    list_q.append(0)
    list_q.append(0)

    list_x.append(1)
    list_x.append(0)

    list_y.append(0)
    list_y.append(1)
    
    i=2

    while 1:
        list_r.append(list_r[i - 2] % list_r[i - 1])
        list_q.append(list_r[i - 2] / list_r[i - 1])

        if list_r[i] == 0:
            d = list_r[i - 1]
            x = list_x[i - 1]
            y = list_y[i - 1]

            if x < 0:
                x += b
            if y < 0:
                y += b

            return d, x, y

        list_x.append(list_x[i - 2] - (list_q[i] * list_x[i - 1]))
        list_y.append(list_y[i - 2] - (list_q[i] * list_y[i - 1]))

        i += 1

    
def __mr(n):
    composite = 0
    inconclusive = 0

    def get_kq(num):
        sub_k = 0
        
        sub_t = num - 1
        b_t = bin(sub_t)

        for sub_i in range(len(b_t) - 1, -1, -1):
            if b_t[sub_i] == '0':
                sub_k += 1
            else:
                break

        sub_q = sub_t >> sub_k
        return sub_k, sub_q
    
    k, q = get_kq(n)
    if k == 0:
        return 0

    for i in range(10):
        a = int(random.uniform(2, n))
        if pow(a, q, n) == 1:
            inconclusive += 1
            continue

        t = 0
        for j in range(k):
            if pow(a, (2 * j * q), n) == n - 1:
                inconclusive += 1
                t = 1
        
        if t == 0:
            composite += 1

    if inconclusive >= 6:
        return 1


def __gen_number(gen_bit):
    random.seed()

    b = str()
    for i in range(gen_bit - 1):
        b += str(int(random.uniform(1, 10)) % 2)
    b += '1'

    return int(b, 2)


def __gen_prime(gen_bit):
    while 1:
        p = __gen_number(gen_bit)
        if __mr(p) == 1:
            return p

def __gen_ed(n):
    while 1:
        t = int(random.uniform(2, 1000))
        d, x, y = __ext_euclid(t, n)
        if d == 1:
            return t, x


def __value_to_string(val):
    ret = str()
    for i in range(32):
        b = val & 0xff
        val >>= 8
        ret += chr(b)

        if val == 0:
            break
    return ret


def __string_to_value(buf):
    plaintext_ord = 0
    for i in range(len(buf)):
        plaintext_ord |= ord(buf[i]) << (i * 8)

    return plaintext_ord

'''
def create_key(pu_fname='key.prk', pr_fname='key.skr', debug=False):
    p = __gen_prime(128)
    q = __gen_prime(128)

    n = p * q
    
    qn = (p - 1) * (q - 1)

    e, d = __gen_ed(qn)

    pu = [e, n]
    pr = [d, n]

    pu_data = base64.b64encode(marshal.dumps(pu))
    pr_data = base64.b64encode(marshal.dumps(pr))

    try:
        open(pu_fname, 'wt').write(pu_data)
        open(pr_fname, 'wt').write(pr_data)
    except IOError:
        return False

    if debug:
        print '[*] Make key : %s, %s' % (pu_fname, pr_fname)

    return True
'''

def read_key(key_filename):
    try:
        with open(key_filename, 'rt') as fp:
            b = fp.read()
            s = base64.b64decode(b)
            key = marshal.loads(s)

        return key
    except IOError:
        return None


def crypt(buf, key):
    plaintext_ord = __string_to_value(buf)

    val = pow(plaintext_ord, key[0], key[1])

    return __value_to_string(val)