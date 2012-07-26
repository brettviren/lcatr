#!/usr/bin/env python

import schema  
import cards
import tables
import hdus
import headers

from gnc_test_data import * 

class GainHDU(schema.HDU):
    def __init__(self, lin_gains = None, med_gains = None):
        mh = headers.MinimalHeader('Gains')
        
        lgc = schema.Column('LinGain', 'float32', 'Linear fit gains',lin_gains)
        mgc = schema.Column('MedGain', 'float32', 'Median gains',    med_gains)

        base = super(GainHDU,self)
        base.__init__(mh,[lgc,mgc])
        return
    pass

class NoiseHDU(schema.HDU):
    def __init__(self, ovsc_noise = None, sdev_noise = None):
        mh = headers.MinimalHeader('Noises')
        
        onc = schema.Column('OvScNoise', 'float32', 'Overscan Noise',  ovsc_noise)
        snc = schema.Column('SdevNoise', 'float32', 'Std. Dev. Noise', sdev_noise)

        base = super(NoiseHDU,self)
        base.__init__(mh,[onc,snc])
        return
    pass
    
class ColdSpotHDU(schema.HDU):
    def __init__(self, **kwds):

        mh = headers.MinimalHeader('ColdSpot')

        amp = schema.Column('AmpNum',   'int16', 'Amplifier Number', kwds.get('ampnum'))
        pix = schema.Column('PixCoung', 'int16', 'Pixel Count',      kwds.get('pixcount'))
        spx = schema.Column('SpotX',    'int16', 'Spot X pixel',     kwds.get('spotx'))
        spy = schema.Column('SpotY',    'int16', 'Spot Y pixel',     kwds.get('spoty'))
        
        base = super(ColdSpotHDU,self)
        base.__init__(mh,[amp,pix,spx,spy])
        return
    pass

secondary_hdus = [
    hdus.FileRefHDU(),
    GainHDU(),
    NoiseHDU(),
    ColdSpotHDU(),
    ]

gnc_schema = schema.Result(
    hdus.PrimaryHDU('GainNoiseCold','theuser'), 
    secondary_hdus
)

if __name__ == '__main__':
    print gnc_schema
    
