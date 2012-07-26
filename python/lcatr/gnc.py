#!/usr/bin/env python
'''
Results for the Gain/Noise/ColdSpot (GNC) test.
'''

import schema as schema

class GncPrimaryHDU(schema.PrimaryHDU):
    def __init__(self, version = 0):
        super(GncPrimaryHDU,self).__init__()
        self.update_ext_name('GainNoiseColdSpot')
        self.update_ext_version(version)
        return
    pass

class GncInputFilesHDU(schema.TableHDU):
    def __init__(self, filelist = None, sha1list = None, version = 0):
        super(GncInputFilesHDU,self).__init__()
        self.update_ext_name('FileRefs')
        self.update_ext_version(version)
        fc = schema.Column(name='FileName', format='A64', array=filelist)
        hc = schema.Column(name='SHA1Hash', format='A64', array=sha1list)
        self.columns = schema.ColDefs([fc,hc])
        return
    pass

class GncGainsHDU(schema.TableHDU):
    def __init__(self, lin_gains = None, med_gains = None, version = 0):
        super(GncGainsHDU,self).__init__()
        self.update_ext_name('Gains')
        self.update_ext_version(version)
        lc = schema.Column(name='LinGains', format='E', array=lin_gains)
        mc = schema.Column(name='MedGains', format='E', array=med_gains)
        self.columns = schema.ColDefs([lc,mc])
        return
    pass

class GncNoisesHDU(schema.TableHDU):
    def __init__(self, ovsc_noise = None, sdev_noise = None, version = 0):
        super(GncNoisesHDU,self).__init__()
        self.update_ext_name('Noises')
        self.update_ext_version(version)
        lc = schema.Column(name='OvScNois', format='E', array=ovsc_noise)
        mc = schema.Column(name='SdevNois', format='E', array=sdev_noise)
        self.columns = schema.ColDefs([lc,mc])
        return
    pass

class GncColdSpotsHDU(schema.TableHDU):
    def __init__(self, **kwds):
        super(GncColdSpotsHDU,self).__init__()
        self.update_ext_name('ColdSpot')
        self.update_ext_version(kwds.get('version') or 0)
        cols = []
        for what in ['AmpNum','PixCount','SpotX','SpotY']:
            c = schema.Column(name=what, format='I', array = kwds.get(what.lower()))
            cols.append(c)
            continue
        self.columns = schema.ColDefs(cols)
        return
    pass
        
class GncResult(schema.HDUList):
    def __init__(self):
        super(GncResult,self).__init__(hdus = [
                GncPrimaryHDU(),
                GncInputFilesHDU(),
                GncGainsHDU(),
                GncNoisesHDU(),
                GncColdSpotsHDU(),
                ])
        return
    pass
        


def test_and_dump(gnc):
    print 'Validating empty GNC:'
    #gnc.validate()
    gnc.info()
    for hdu in gnc:
        print hdu.header
        try:
            cols = hdu.columns
        except AttributeError:
            continue
        print cols
        for c in cols:
            print c.array
        print
        continue
    return

def test_empty():
    gnc = GncResult()
    test_and_dump(gnc)

def test_update():
    gnc = GncResult()
    gnc['Gains'].columns[0].array = [2.5122094, 2.8183959, 2.5010307, 2.7617979, 2.5760174, 2.7574365, 2.492455, 2.5485373, 2.7024412, 2.6239278, 2.6323957, 2.888442, 2.7222559, 2.7458601, 2.7033682, 2.7953243]
    gnc['Gains'].columns[1].array = [2.6737275123596191, 2.7658350467681885, 2.6715354919433594, 2.89190673828125, 2.6117188930511475, 2.7842977046966553, 2.6492691040039062, 2.6967630386352539, 2.8955318927764893, 2.8027498722076416, 2.8578372001647949, 3.0660858154296875, 2.9354989528656006, 2.934161901473999, 2.9992959499359131, 2.8692851066589355]
    test_and_dump(gnc)

if __name__ == '__main__':
    # test_empty()
    test_update()
