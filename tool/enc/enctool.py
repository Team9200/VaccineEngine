import os
import sys
import lmdenc

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage : enctool.py [python source]'
        exit()

    lmdenc.make(sys.argv[1], True)
