# -*- coding:utf-8 -*-
# Author : kjy
# Date : 18. 9. 27
# Version : v1.0
# Explanation : 공유 라이브러리

import hashlib
import struct
import re
import glob
import os
import marshal
import time

def md5(data):
    return hashlib.md5(data).hexdigest()


def get_uint16(buf, off):
    return struct.unpack('<H', buf[off:off+2])[0]


def get_uint32(buf, off):
    return struct.unpack('<L', buf[off:off+4])[0]


handle_pattern_md5 = None
p_md5_pattern_ext = re.compile(r'\.s(\d\d)$', re.IGNORECASE)


class PatternMD5:
    def __init__(self, plugins_path):
        self.sig_sizes = {}
        self.sig_p1s = {}
        self.sig_p2s = {}
        self.sig_names = {}
        self.sig_times = {}
        self.plugins = plugins_path

        fl = glob.glob(os.path.join(plugins_path, '*.s??'))
        fl.sort()
        for name in fl:
            obj = p_md5_pattern_ext.search(name)
            if obj:
                idx = obj.groups()[0]  # ex:01
                sig_key = os.path.split(name)[1].lower().split('.')[0]  # ex:script
                sp = self.__load_sig(name)
                if sp is None:
                    continue

                if len(sp):  # 로딩된 패턴이 1개 이상이면...
                    if not (sig_key in self.sig_sizes):
                        self.sig_sizes[sig_key] = {}

                    for psize in list(sp):
                        if psize in self.sig_sizes[sig_key]:
                            self.sig_sizes[sig_key][psize].append(idx)
                        else:
                            self.sig_sizes[sig_key][psize] = [idx]

    def match_size(self, sig_key, sig_size):
        sig_key = sig_key.lower()  # 대문자로 입력될 가능성 때문에 모두 소문자로 변환

        if sig_key in self.sig_sizes:  # sig_key가 로딩되어 있나?
            if sig_size in self.sig_sizes[sig_key]:
                return True

        return False

    def scan(self, sig_key, sig_size, sig_md5):
        sig_key = sig_key.lower()  # 대문자로 입력될 가능성 때문에 모두 소문자로 변환

        if self.match_size(sig_key, sig_size):  # 크기가 존재하는가?
            idxs = self.sig_sizes[sig_key][sig_size]  # 어떤 파일에 1차 패턴이 존재하는지 확인

            fmd5 = sig_md5.decode('hex')
            sig_p1 = fmd5[:6]  # 1차 패턴
            sig_p2 = fmd5[6:]  # 2차 패턴

            for idx in idxs:
                # 1차 패턴 비교 진행
                # 1차 패턴이 로딩되어 있지 않다면..
                if self.__load_sig_ex(self.sig_p1s, 'i', sig_key, idx) is False:
                    continue

                if sig_p1 in self.sig_p1s[sig_key][idx]:  # 1차 패턴 발견
                    p2_offs = self.sig_p1s[sig_key][idx][sig_p1]

                    # 2차 패턴 비교 진행
                    # 2차 패턴이 로딩되어 있지 않다면..
                    if self.__load_sig_ex(self.sig_p2s, 'c', sig_key, idx) is False:
                        continue

                    for off in p2_offs:
                        if self.sig_p2s[sig_key][idx][off] == sig_p2:  # 2차 패턴 발견
                            # 이름 패턴이 로딩되어 있지 않다면..
                            if self.__load_sig_ex(self.sig_names, 'n', sig_key, idx) is False:
                                continue

                            return self.sig_names[sig_key][idx][off]  # 악성코드 이름 리턴

        self.__save_mem()
        return None

    def __load_sig(self, fname):
        try:
            data = open(fname, 'rb').read()
            if data[0:4] == 'LINV':
                sp = marshal.loads(data[12:])
                return sp
        except IOError:
            return None

    def __load_sig_ex(self, sig_dict, sig_prefix, sig_key, idx):  # (self.sig_names, 'n', 'script', '01')
        if not (sig_key in sig_dict) or not (idx in sig_dict[sig_key]):
            # 패턴 로딩
            try:
                name_fname = self.plugins + os.sep + '%s.%s%s' % (sig_key, sig_prefix, idx)
                sp = self.__load_sig(name_fname)
                if sp is None:
                    return False
            except IOError:
                return False

            sig_dict[sig_key] = {idx: sp}

        # 현재 시간을 sig_time에 기록한다.
        if not (sig_key in self.sig_times):
            self.sig_times[sig_key] = {}

        if not (sig_prefix in self.sig_times[sig_key]):
            self.sig_times[sig_key][sig_prefix] = {}

        self.sig_times[sig_key][sig_prefix][idx] = time.time()

        return True

    def __save_mem(self):
        # 정리해야 할 패턴이 있을까? (3분 이상 사용되지 않은 패턴)
        n = time.time()
        for sig_key in self.sig_times.keys():
            for sig_prefix in self.sig_times[sig_key].keys():
                for idx in self.sig_times[sig_key][sig_prefix].keys():
                    # print '[-]', n - self.sig_times[sig_key][sig_prefix][idx]
                    if n - self.sig_times[sig_key][sig_prefix][idx] > (3 * 60):
                        # print '[*] Delete sig : %s.%s%s' % (sig_key, sig_prefix, idx)
                        if sig_prefix == 'i':  # 1차 패턴
                            self.sig_p1s[sig_key].pop(idx)
                        elif sig_prefix == 'c':  # 2차 패턴
                            self.sig_p2s[sig_key].pop(idx)
                        elif sig_prefix == 'n':  # 악성코드 이름 패턴
                            self.sig_names[sig_key].pop(idx)

                        self.sig_times[sig_key][sig_prefix].pop(idx)  # 시간

    def get_sig_num(self, sig_key):
        sig_num = 0
        fl = glob.glob(self.plugins + os.sep + '%s.n??' % sig_key)

        for fname in fl:
            try:
                buf = open(fname, 'rb').read(12)
                if buf[0:4] == 'LINV':
                    sig_num += get_uint32(buf, 4)
            except IOError:
                return None

        return sig_num


class LVModule:
    def init(self, modulePath):
        global handle_pattern_md5
        handle_pattern_md5 = PatternMD5(modulePath + os.sep + 'sigdb')

        return 0

    def uninit(self):
        return 0

    def getInfo(self):
        info = dict()

        info['author'] = 'kjy'
        info['version'] = '1.0'
        info['title'] = 'Share Libary'
        info['moduleName'] = 'sharelib'

        return info


if __name__ == '__main__':
    s = time.time()
    pmd5 = PatternMD5('.')

    print pmd5.scan('main', 527360, '243c838d9258efd170904c0cc7c0f3c0')
    print pmd5.scan('main', 61440, '1f7d9e478a300234406550e78e417074')

    for i in range(10):
        pmd5.scan('main', 61440, '1f7d9e478a300234406550e78e417074')

    e = time.time()
    print
    print '[*] count :', i + 1
    print '[*] time :', e-s


