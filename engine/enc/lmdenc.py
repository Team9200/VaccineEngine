import hashlib
import os
import py_compile
import random
import shutil
import struct
import sys
import zlib
import linvrc4
import linvrsa
import linvtimelib
import marshal
import imp

def make(src_fname, debug=False):
    fname = src_fname
    
    if fname.split('.')[1] == 'py':
        py_compile.compile(fname)
        pyc_name = fname + 'c'
    else:
        pyc_name = fname.split('.')[0] + '.pyc'
        shutil.copy(fname, pyc_name)
        
    rsa_pu = linvrsa.read_key('key.pkr')
    #print 'pkr : ', rsa_pu

    rsa_pr = linvrsa.read_key('key.skr')
    #print 'skr : ', rsa_pr

    if not (rsa_pr and rsa_pu):
        if debug:
            print 'ERROR : Cannot find the Key files!'
        return False

    lmd_data = 'LINV'

    ret_date = linvtimelib.get_now_date()
    ret_time = linvtimelib.get_now_time()

    val_date = struct.pack('<H', ret_date)
    val_time = struct.pack('<H', ret_time)

    reserved_buf = val_date + val_time + (chr(0) * 28)
 
    lmd_data += reserved_buf

    random.seed()

    while 1:
        tmp_lmd_date = str()
        key = str()
        for i in range(16):
            key += chr(random.randint(0, 0xff))
        
        e_key = linvrsa.crypt(key, rsa_pr)
        if len(e_key) != 32:
            continue
        
        d_key = linvrsa.crypt(e_key, rsa_pu)

        if key == d_key and len(key) == len(d_key):
            tmp_lmd_date += e_key
            
            buf1 = open(pyc_name, 'rb').read()
            buf2 = zlib.compress(buf1)

            e_rc4 = linvrc4.RC4()
            e_rc4.set_key(key)

            buf3 = e_rc4.crypt(buf2)

            e_rc4 = linvrc4.RC4()
            e_rc4.set_key(key)

            if e_rc4.crypt(buf3) != buf2:
                continue
            
            tmp_lmd_date += buf3

            md5 = hashlib.md5()
            md5hash = lmd_data + tmp_lmd_date

            for i in range(3):
                md5.update(md5hash)
                md5hash = md5.hexdigest()
            
            m = md5hash.decode('hex')

            e_md5 = linvrsa.crypt(m, rsa_pr)
            if len(e_md5) != 32:
                continue

            d_md5 = linvrsa.crypt(e_md5, rsa_pu)
            if m == d_md5:
                lmd_data += tmp_lmd_date + e_md5
                break

    ext = fname.find('.')
    lmd_name = fname[0:ext] + '.lmd'

    try:
        if lmd_data:
            open(lmd_name, 'wb').write(lmd_data)

            os.remove(pyc_name)

            if debug:
                print '        Success : %-13s -> %s' % (fname, lmd_name)
            return True
        else:
            raise IOError
    except IOError:
        if debug:
            print '        Fail : %s' % fname
        return False
