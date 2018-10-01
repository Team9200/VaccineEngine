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
    def format(self, fileHandle, fileName):
        fileFormat = {}
        mm = fileHandle
        if mm[0:4] == 'PK\x03\x04':
            fileFormat['size'] = len(mm)

            ret = {'ff_zip': fileFormat}
            return ret

        return None

    def arclist(self, fileName, fileFormat):
        fileScanList = list()

        if 'ff_zip' in fileFormat:
            zfile = zipfile.ZipFile(fileName)
            for name in zfile.namelist():
                fileScanList.append(['arc_zip', name])
            zfile.close()

        return fileScanList

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