import core.linvengine

k2 = core.linvengine.Engine(debug=True)
if k2.setModules('modules'):
    kav = k2.createInstance()
    if kav:
        ret = kav.init()
        info = kav.getInfo()
        result, malwareName, malwareID, engineID = kav.scan('eicar.txt')
        if result:
            kav.disinfect('eicar.txt', malwareID, engineID)
        kav.uninit()
