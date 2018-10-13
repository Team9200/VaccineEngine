import hashlib
import os
import py_compile
import random
import shutil
import struct
import sys
import zlib
import linrc4
import linrsa
import lintimelib
import marshal
import imp


def ntimes_md5(buf, ntimes):
    md5 = hashlib.md5()
    md5hash = buf
    for i in range(ntimes):
        md5.update(md5hash)
        md5hash = md5.hexdigest()

    return md5hash


class LMDFormatError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class LMDConstants:
    LMD_SIGNATURE = 'LINV'

    LMD_DATE_OFFSET = 4
    LMD_DATE_LENGTH = 2
    LMD_TIME_OFFSET = 6 
    LMD_TIME_LENGTH = 2

    LMD_RESERVED_OFFSET = 8
    LMD_RESERVED_LENGTH = 28

    LMD_RC4_KEY_OFFSET = 36
    LMD_RC4_KEY_LENGTH = 32

    LMD_MD5_OFFSET = -32


class LMD(LMDConstants):
    def __init__(self, fname, pu):
        self.filename = fname
        self.date = None
        self.time = None
        self.body = None

        self.__LMD_data = None
        self.__rsa_pu = pu
        self.__rc4_key = None

        if self.filename:
            self.__decrypt(self.filename)

    def __decrypt(self, fname, debug=True):
        with open(fname, 'rb') as fp:
            if fp.read(4) == self.LMD_SIGNATURE:
                self.__LMD_data = self.LMD_SIGNATURE + fp.read()
            else:
                raise LMDFormatError('LMD Header magic not found.')
        tmp = self.__LMD_data[self.LMD_DATE_OFFSET:self.LMD_DATE_OFFSET + self.LMD_DATE_LENGTH]
        self.date = lintimelib.convert_date(struct.unpack('<H', tmp)[0])
        

        tmp = self.__LMD_data[self.LMD_TIME_OFFSET:self.LMD_TIME_OFFSET + self.LMD_TIME_LENGTH]
        self.time = lintimelib.convert_time(struct.unpack('<H', tmp)[0])

        e_md5hash = self.__get_md5()

        md5hash = ntimes_md5(self.__LMD_data[:self.LMD_MD5_OFFSET], 3)

        if e_md5hash != md5hash.decode('hex'):
            raise LMDFormatError('Invalid LMD MD5 hash.')

        self.__rc4_key = self.__get_rc4_key()

        e_LMD_data = self.__get_body()

        self.body = zlib.decompress(e_LMD_data)
        if debug:
            print len(e_LMD_data)
        
    
    def __get_rc4_key(self):
        e_key = self.__LMD_data[self.LMD_RC4_KEY_OFFSET:self.LMD_RC4_KEY_OFFSET + self.LMD_RC4_KEY_LENGTH]
        
        return linrsa.crypt(e_key, self.__rsa_pu)

    
    def __get_body(self):
        e_LMD_data = self.__LMD_data[self.LMD_RC4_KEY_OFFSET + self.LMD_RC4_KEY_LENGTH:self.LMD_MD5_OFFSET]
        r = linrc4.RC4()
        r.set_key(self.__rc4_key)
        return r.crypt(e_LMD_data)

    
    def __get_md5(self):
        e_md5 = self.__LMD_data[self.LMD_MD5_OFFSET:]
        return linrsa.crypt(e_md5, self.__rsa_pu)

def load(mod_name, buf):
    if buf[:4] == '03F30D0A'.decode('hex'):
        code = marshal.loads(buf[8:])
        module = imp.new_module(mod_name)
        exec (code, module.__dict__)
        sys.modules[mod_name] = module
        
        return module
    else:
        return None
