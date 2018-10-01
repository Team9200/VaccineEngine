import os
import sys

import core.linvengine


def linvScan(fileName):
    linvEngine = core.linvengine.Engine()#debug=True)

    if linvEngine.setModules('modules'):
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
                    linv.scan(absoluteFilePath, scanFile_callback, scanDir_callback)
                else:
                    print '[!] Envalid path: \'%s\'' % absoluteFilePath

                ret = linv.getResult()
                printScanResult(ret)
                linv.uninit()
    else:
        print "[!] No modules!"


def scanDir_callback(resultValue):
    realName = resultValue['fileName']
    print realName


def scanFile_callback(resultValue):
    fs = resultValue['fileStruct']

    if len(fs.getAdditionalFilename()) != 0 :
        displayName = '%s (%s)' % (fs.getMasterFilename(), fs.getAdditionalFilename())
    else:
        displayName = '%s' % (fs.getMasterFilename())

    if resultValue['result']:
        state = 'infected'

        virusName = resultValue['virusName']
        message = '%s : %s' % (state, virusName)
    else:
        message = 'ok'

    resultMessage = displayName + ' - ' + message
    print resultMessage


def printScanResult(ret):
    print '\n[-] Result'
    for key in ret.keys():
        print key, ":", ret[key]


if __name__ == '__main__':
    linvScan(sys.argv[1])
