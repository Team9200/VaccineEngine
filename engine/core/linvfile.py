# -*- coding:utf-8 -*-
# Author : kjy
# Date : 18. 9. 27
# Version : v1.0
# Explanation : 파일정보 구조체를 다루는 클래스


class FileStruct:
    # function : __init__(self, filename=None, level=0)
    # Explanation : 클래스 초기화
    # input : filename - 파일 이름, level - 압축 깊이
    def __init__(self, filename=None, level=0):
        self.__fs = {}

        if filename:
            self.setDefault(filename, level)

    # function : setDefault(self, filename, level)
    # Explanation : FileStruct 생성 및 초기화
    # input : filename - 파일 이름, level - 압축 깊이
    def setDefault(self, filename, level):
        self.__fs['isArc'] = False
        self.__fs['arcEngineName'] = -1
        self.__fs['arcFilename'] = str()
        self.__fs['filenameInArc'] = str()
        self.__fs['realFilename'] = filename
        self.__fs['additionalFilename'] = str()

        self.__fs['masterFilename'] = filename
        self.__fs['isModify'] = False
        self.__fs['canArc'] = False
        self.__fs['level'] = level

    # function : isArchive(self)
    # Explanation : 압축 여부 확인
    # return : True - 압축, False - 압축 안됨
    def isArchive(self):
        return self.__fs['isArc']

    # function : getArchiveEngineName(self)
    # Explanation : 압축 해제 가능 엔진 확인
    # return : 압축 해제 가능 엔진
    def getArchiveEngineName(self):
        return self.__fs['arcEngineName']

    # function : getArchiveFilename(self)
    # Explanation : 실제 압축 파일 이름 확인
    # return : 실제 압축 파일 이름
    def getArchiveFilename(self):
        return self.__fs['arcFilename']

    # function : getFilenameInArchive(self)
    # Explanation : 압축 해제 대상 파일 이름 확인
    # return : 압축 해제 대상 파일 이름
    def getFilenameInArchive(self):
        return self.__fs['filenameInArc']


    def getFilename(self):
        return self.__fs['realFilename']


    def setFilename(self, fname):
        self.__fs['realFilename'] = fname


    def getMasterFilename(self):
        return self.__fs['masterFilename']


    def getAdditionalFilename(self):
        return self.__fs['additionalFilename']


    def isModify(self):
        return self.__fs['isModify']


    def setModify(self, modify):
        self.__fs['isModify'] = modify


    def canArchive(self):
        return self.__fs['canArc']


    def getLevel(self):
        return self.__fs['level']


    def setLevel(self, level):
        self.__fs['level'] = level

    # function : setDefault(self, filename, level)
    # Explanation : FileStruct 생성 및 초기화
    # input : filename - 파일 이름, level - 압축 깊이
    def setArchive(self, engine_id, rname, fname, dname, mname, modify, canArc, level):
        self.__fs['isArc'] = True
        self.__fs['arcEngineName'] = engine_id
        self.__fs['arcFilename'] = rname
        self.__fs['filenameInArc'] = fname
        self.__fs['realFilename'] = str()
        self.__fs['additionalFilename'] = dname

        self.__fs['masterFilename'] = mname
        self.__fs['isModify'] = modify
        self.__fs['canArc'] = canArc
        self.__fs['level'] = level


    def printfileinfo(self):
        print self.__fs['isArc'], self.__fs['arcEngineName'], self.__fs['arcFilename'], self.__fs['filenameInArc'], self.__fs['realFilename'],