# -*- coding:utf-8 -*-
# Author : kjy
# Date : 18. 9. 27
# Version : v1.0
# Explanation : 모듈 스켈레톤 코드
import zipfile

class LVModule:
    def init(self, plugin_path):
        return 0

    def uninit(self):
        return 0

    def getInfo(self):
        info = dict()

        info['author'] = 'kjy'
        info['version'] = 'v1.0'
        info['explanation'] = 'Zip Archive Engine'
        info['moduleName'] = 'zip'
        info['sigNum'] = 0

        return info

    '''
    def scan(self, filehandle, filename):
        pass

    def disinfected(self):
        pass

    def virusList(self):
        pass
    '''

    # function : format(self, fileHandle, fileName)
    # Explanation : 파일 포멧을 분석
    # input : filehandle - 분석할 파일 핸들러, filename - 분석할 파일 이름
    # return : ret - 파일 포멧, 사이즈 딕셔너리, None - 실패
    def format(self, fileHandle, fileName):
        fileFormat = {}
        mm = fileHandle
        if mm[0:4] == 'PK\x03\x04':
            fileFormat['size'] = len(mm)

            ret = {'ff_zip': fileFormat}
            return ret

        return None

    # function : arclist(self, fileName, fileFormat)
    # Explanation : 압축파일 내부의 파일목록을 얻음
    # input :fileName - 파일 이름, fileFormat - 파일 포멧
    # return : [[압축엔진, 압축된 파일 이름]]
    def arclist(self, fileName, fileFormat):
        fileScanList = list()

        if 'ff_zip' in fileFormat:
            zfile = zipfile.ZipFile(fileName)
            for name in zfile.namelist():
                fileScanList.append(['arc_zip', name])
            zfile.close()

        return fileScanList

    # function : unarc(self, arcEngineID, arcName, fnameInArc)
    # Explanation : 압축된 파일 이름으로 하나씩 압축을 해제
    # input : arcEngineID - 압축 엔진, arcName - 압축 파일, fnameInArc - 압축 해제할 파일 이름
    # return : [[압축엔진, 압축된 파일 이름]]
    def unarc(self, arcEngineID, arcName, fnameInArc):
        if arcEngineID == 'arc_zip':
            zfile = zipfile.ZipFile(arcName)
            data = zfile.read(fnameInArc)
            zfile.close()

            return data

        return None

    def mkarc(self, arc_engine_id, arc_name, file_infos):
        if arc_engine_id == 'arc_zip':
            zfile = zipfile.ZipFile(arc_name, 'w')

            for file_info in file_infos:
                rname = file_info.get_filename()

                try:
                    with open(rname, 'rb') as fp:
                        buf = fp.read()

                        a_name = file_info.get_filename_in_archive()
                        zfile.writestr(a_name, buf)
                except IOError:
                    pass

            zfile.close()
            return True

        return False