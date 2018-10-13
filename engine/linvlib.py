import os
import sys
import json

import core.linvengine


def linvScan(fileName):
    linvEngine = core.linvengine.Engine()#debug=True)
    rootDir = os.path.dirname(os.path.abspath(__file__))

    if linvEngine.setModules(rootDir + '/modules'):
        linv = linvEngine.createInstance()
        if linv:
            ret = linv.init()
            scanStartTime = linv.getVersion()
            sigNum = linv.getSignum()
            print 'Scan Start time %s UTC' % scanStartTime
            print 'Total Signiture Num : ' + str(sigNum)
            print '\n[-] Scan Start'
            if ret:
                linv.setResult()
                absoluteFilePath = os.path.abspath(fileName)

                if os.path.exists(absoluteFilePath):
                    scannedPath = linv.scan(absoluteFilePath, core.linvengine.scanFile_callback, core.linvengine.scanDir_callback, core.linvengine.disinfect_callback, core.linvengine.update_callback)
                    print json.dumps(scannedPath)
                    # ret['scannedPath'] = scannedPath
                else:
                    print '[!] Envalid path: \'%s\'' % absoluteFilePath

                ret = linv.getResult()
                printScanResult(ret)
                linv.uninit()
    else:
        print "[!] No modules!"


def printScanResult(ret):
    # print '\n[-] Result'
    print json.dumps(ret)
    # for key in ret.keys():
    #     print key, ":", ret[key]


if __name__ == '__main__':
    linvScan(sys.argv[1])
