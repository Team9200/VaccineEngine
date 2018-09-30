# -*- coding:utf-8 -*-
# Author : kjy
# Date : 18. 9. 27
# Version : v1.0
# Explanation : 공유 라이브러리

import hashlib

def md5(data):
    return hashlib.md5(data).hexdigest()

class LVModule:
    def init(self, modulePath):
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
