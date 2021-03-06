# -*- coding:utf-8 -*-
import re
import sys
import os
import struct
import marshal
import linvtimelib

MAX_COUNT = 100000
re_comment = r'#.*'

size_sig = []  # 크기와 ID 저장
p1_sig = {}  # MD5 앞쪽 6Byte
p2_sig = []  # MD5 앞쪽 10Byte
name_sig = []  # 악성코드 이름


def add_signature(line):
    t = line.split(':')

    size = int(t[0])  # size
    fmd5 = t[1].decode('hex')  # MD5를 텍스트에서 바이너리로 바꾼다.
    name = t[2]

    # 크기 추가
    size_sig.append(size)

    p1 = fmd5[:6]  # 앞쪽 6Byte
    p2 = fmd5[6:]  # 뒤쪽 10Byte

    p2_sig.append(p2)  # 2차 악성코드 패턴 추가
    p2_id = p2_sig.index(p2)

    # 혹시 기존 p1이 존재하는가?
    if p1 in p1_sig:
        p1_sig[p1].append(p2_id)
    else:
        p1_sig[p1] = [p2_id]

    name_sig.append(name)

# -------------------------------------------------------------------------
# 파일을 생성한다.
# -------------------------------------------------------------------------
def save_file(fname, data):
    fp = open(fname, 'wb')
    fp.write(data)
    fp.close()


# -------------------------------------------------------------------------
# ID별로 파일을 생성한다.
# -------------------------------------------------------------------------
def save_sig_file(fname, _id):
    # 주어진 패턴 파일명을 이용해서 sig 파일을 만듦
    t = os.path.abspath(fname)
    _, t = os.path.split(t)
    name = os.path.splitext(t)[0]
    save_signature(name, _id)

    # 초기화
    global size_sig
    global p1_sig
    global p2_sig
    global name_sig

    size_sig = []  # 크기와 ID 저장
    p1_sig = {}  # MD5 앞쪽 6Byte
    p2_sig = []  # MD5 앞쪽 10Byte
    name_sig = []  # 악성코드 이름


# -------------------------------------------------------------------------
# 텍스트 형태의 악성코드 패턴 DB 파일을 분석해서 악성코드 패턴 파일들을 생성한다.
# -------------------------------------------------------------------------
def make_signature(fname, _id):
    fp = open(fname, 'rb')

    idx = 0

    while True:
        line = fp.readline()
        if not line:
            break

        # 주석문 및 화이트 스페이스 제거
        line = re.sub(re_comment, '', line)
        line = re.sub(r'\s', '', line)

        if len(line) == 0:
            continue  # 아무것도 없다면 다음줄로...

        add_signature(line)

        idx += 1

        if idx >= MAX_COUNT:
            print '[*] %s : %d' % (fname, _id)
            save_sig_file(fname, _id)
            idx = 0
            _id += 1

    fp.close()

    save_sig_file(fname, _id)


def save_signature(fname, _id):
    # 현재 날짜와 시간을 구한다.
    ret_date = linvtimelib.get_now_date()
    ret_time = linvtimelib.get_now_time()

    # 날짜와 시간 값을 2Byte로 변경한다.
    val_date = struct.pack('<H', ret_date)
    val_time = struct.pack('<H', ret_time)

    # 크기 파일 저장 : ex) script.s01
    sname = '%s.s%02d' % (fname, _id)
    t = marshal.dumps(set(size_sig))  # 중복된 데이터 삭제 후 저장
    t = 'LINV' + struct.pack('<L', len(size_sig)) + val_date + val_time + t
    save_file(sname, t)

    # 패턴 p1 파일 저장 : ex) script.i01
    sname = '%s.i%02d' % (fname, _id)
    t = marshal.dumps(p1_sig)
    t = 'LINV' + struct.pack('<L', len(p1_sig)) + val_date + val_time + t
    save_file(sname, t)

    # 패턴 p2 파일 저장 : ex) script.c01
    sname = '%s.c%02d' % (fname, _id)
    t = marshal.dumps(p2_sig)
    t = 'LINV' + struct.pack('<L', len(p2_sig)) + val_date + val_time + t
    save_file(sname, t)

    # 악성코드 이름 파일 저장 : ex) script.n01
    sname = '%s.n%02d' % (fname, _id)
    t = marshal.dumps(name_sig)
    t = 'LINV' + struct.pack('<L', len(name_sig)) + val_date + val_time + t
    save_file(sname, t)

# -------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage : sigtool_md5.py [sig text] [id]'
        exit(0)

    if len(sys.argv) == 2:
        sin_fname = sys.argv[1]
        _id = 1
    elif len(sys.argv) == 3:
        sin_fname = sys.argv[1]
        _id = int(sys.argv[2])

    make_signature(sin_fname, _id)