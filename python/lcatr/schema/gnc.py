#!/usr/bin/env python
'''
Results for the Gain/Noise/ColdSpot (GNC) test.
'''

import base as pyfits

class GncPrimaryHDU(pyfits.PrimaryHDU):
    def __init__(self, version = 0):
        super(GncPrimaryHDU,self).__init__()
        self.update_ext_name('GainNoiseColdSpot')
        self.update_ext_version(version)
        return
    pass

class GncInputFilesHDU(pyfits.TableHDU):
    def __init__(self, filelist = None, sha1list = None, version = 0):
        super(GncInputFilesHDU,self).__init__()
        self.update_ext_name('FileRefs')
        self.update_ext_version(version)
        fc = pyfits.Column(name='FileName', format='A64', array=filelist, start=1)
        hc = pyfits.Column(name='SHA1Hash', format='A64', array=sha1list, start=2)
        self.columns = pyfits.ColDefs([fc,hc])
        return
    pass

class GncGainsHDU(pyfits.TableHDU):
    def __init__(self, lin_gains = None, med_gains = None, version = 0):
        super(GncGainsHDU,self).__init__()
        self.update_ext_name('Gains')
        self.update_ext_version(version)
        lc = pyfits.Column(name='LinGains', format='E', array=lin_gains, start=1)
        mc = pyfits.Column(name='MedGains', format='E', array=med_gains, start=2)
        self.columns = pyfits.ColDefs([lc,mc])
        return
    pass

class GncNoisesHDU(pyfits.TableHDU):
    def __init__(self, ovsc_noise = None, sdev_noise = None, version = 0):
        super(GncNoisesHDU,self).__init__()
        self.update_ext_name('Noises')
        self.update_ext_version(version)
        lc = pyfits.Column(name='OvScNois', format='E', array=ovsc_noise, start=1)
        mc = pyfits.Column(name='SdevNois', format='E', array=sdev_noise, start=2)
        self.columns = pyfits.ColDefs([lc,mc])
        return
    pass

class GncColdSpotsHDU(pyfits.TableHDU):
    def __init__(self, **kwds):
        super(GncColdSpotsHDU,self).__init__()
        self.update_ext_name('ColdSpot')
        self.update_ext_version(kwds.get('version') or 0)
        cols = []
        for count, what in enumerate(['AmpNum','PixCount','SpotX','SpotY']):
            c = pyfits.Column(name=what, format='I', array = kwds.get(what.lower()), start=count+1)
            cols.append(c)
            continue
        self.columns = pyfits.ColDefs(cols)
        return
    pass
        
class GncResult(pyfits.HDUList):
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
        
