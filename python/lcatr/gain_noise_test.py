#!/usr/bin/env python
from gnc_test_data import * 


def primary_hdu(test_name, test_date, commit_hash):
    '''
http://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/docs/rates/ogip_93_003/ogip_93_003.html
http://heasarc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html

alternate time stamps:
DATE-OBS= '09/07/93'         / date of observation start (dd/mm/yy)
TIME-OBS= '01:02:26.003'     / time of observation start (hh:mm:ss.ddddd)
DATE-END= '09/07/93'         / date of observation end (dd/mm/yy)
TIME-END= '02:45:02.45'      / time of observation end (hh:mm:ss.ddddd)
    '''

    from pyfits import Card, Header, PrimaryHDU
    cards = [
        Card('SchemaV',0,'Schema Version'),
        Card('TestName',test_name,
             'Name of the test station.'),
        Card('DATE-OBS',test_date.strftime("%Y-%m-%dT%H:%M:%S"),
             'Date test was performed.'),
        Card('Commit',  commit.hexdigest(),   
             'Commit hash.'),
        ]

    header = Header(cards = cards)
    ret = PrimaryHDU(header=header)
    ret.add_checksum()
    return ret

def gain_noise_payload(lgain, mgain, onoise, snoise, spots, flist, fhash):
    '''
    Produce a list of three HDUs with the payload information from the
    gain, noise and cold spots test.

    Args give linear gain, median gain, overscan noise and std dev
    noise and cold spots list and list of analyzed files
    '''
    import numpy as np
    from pyfits import Column, new_table, Card, Header, ImageHDU, TableHDU

    ret = []

    # analyzed files
    fc = Column(name='FileName', format='A64', array=np.array(flist))
    hc = Column(name='SHA1Hash', format='A64', array=np.array(fhash))
    ft = new_table([fc,hc])
    ft.name = 'AnaFiles'
    ret.append(ft)

    # gains
    lc = Column(name='LinGain', format='E', array=np.array(lgain))
    mc = Column(name='MedGain', format='E', array=np.array(mgain))
    gt = new_table([lc,mc])
    gt.name = 'Gains'
    ret.append(gt)
    
    # noise
    oc = Column(name='OvScNois', format='E', array=np.array(onoise))
    sc = Column(name='SdevNois', format='E', array=np.array(snoise))
    nt = new_table([oc,sc])
    nt.name = 'Noise'
    ret.append(nt)

    # cold spots
    # ampnum = np.array([], dtype = np.int16)
    # pixcount = np.array([], dtype = np.int16)
    # spotx = np.array([], dtype = np.int16)
    # spoty = np.array([], dtype = np.int16)
    ampnum = []; pixcount = []; spotx = []; spoty = []
    
    for spot in spots:
        an = spot[0]
        nc = spot[1]
        nspots = len(spot[2:])
        nper = nc/nspots
        for x,y in spot[2:]:
            ampnum.append(an)
            pixcount.append(nper)
            spotx.append(x)
            spoty.append(y)
            continue            # over spots in amp
        continue                # over all amps
    print len(ampnum), ampnum
    print len(pixcount), pixcount
    anc = Column(name='AmpNum', format='I', array = ampnum)
    pcc = Column(name='PixCount', format='I', array = pixcount)
    sxc = Column(name='SpotX', format='I', array = spotx)
    syc = Column(name='SpotY', format='I', array = spoty)

    ct = new_table([anc,pcc,sxc,syc], tbtype='TableHDU')
    ct.name = 'ColdSpot'
    ret.append(ct)

    for hdu in ret:
        hdu.add_checksum()

    return ret

if '__main__' == __name__:
    import sys, time, datetime
    from hashlib import sha1

    commit = sha1()             # dummy for now
    now = datetime.datetime(*time.gmtime()[:6]) # now for now

    filename = sys.argv[1]
    from pyfits import HDUList

    phdu = primary_hdu('GainNoiseColdSpots', now, commit)

    pl = gain_noise_payload(linear_fit_gains, median_gains, 
                            overscan_noise, stddev_noise, cold_spots,
                            analyzed_files, [sha1(f).hexdigest() for f in analyzed_files])

    hdul = HDUList([phdu]+pl)
    hdul.writeto(filename, checksum=True)
    
    
