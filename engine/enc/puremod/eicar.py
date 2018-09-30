# -*- coding:utf-8 -*-
# Author : kjy
# Date : 18. 9. 27
# Version : v1.0
# Explanation : eicar 전용 백신 모듈

import os
import linvsharelib

# class : LVPlugin
# Explanation : eicar 모듈
class LVModule:
    # function : init(self, modulePath)
    # Explanation : 모듈 초기화
    # input : modulePath - 모듈 경로
    # return : 0 - 성공, 0 이외 - 실패
    def init(self, modulePath):
        return 0

    # function : uninit(self)
    # Explanation : 모듈 초기화
    # input : modulePath - 모듈 경로
    # return : 0 - 성공, 0 이외 - 실패
    def uninit(self):
        return 0

    # function : scan(self)
    # Explanation : 모듈 초기화
    # input : filehandle - 검사할 파일 핸들러, filename - 검사할 파일 이름
    # return : (성공/실패 여부, 악성코드 이름, 악성코드 ID)
    def scan(self, filehandle, filename):
        try:
            tmpFileHandle = filehandle

            size = os.path.getsize(filename)
            if size == 68:
                fileMd5 = linvsharelib.md5(tmpFileHandle[:68])

                if fileMd5 == "44d88612fea8a8f36de82e1278abb02f":
                    return True, 'EICAR-Test-File (not a virus)', 0

        except IOError:
            pass

        return False, '', -1
        
    # function : uninit(self)
    # Explanation : 모듈 초기화
    # input : modulePath - 모듈 경로
    # return : 0 - 성공, 0 이외 - 실패
    def disinfect(self, filename, malwareID):
        try:
            if malwareID == 0:
                os.remove(filename)
                return True

        except IOError:
            pass

        return False

    # function : virusList(self)
    # Explanation : 진단/치료 가능한 악성코드 목록
    # return : vlist - 악성코드 목록
    def virusList(self):
        vlist = list()

        vlist.append('EICAR-Test-File (not a virus)')

        return vlist

    # function : getInfo(self)
    # Explanation : 모듈 정보
    # return : info - 모듈 정보
    def getInfo(self):
        info = dict()

        info['author'] = 'kjy'
        info['version'] = 'v1.0'
        info['explanation'] = 'EICAR Scan Engine'
        info['moduleName'] = 'eicar'
        info['sigNum'] = 1

        return info