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
        
