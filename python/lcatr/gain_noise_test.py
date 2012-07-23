#!/usr/bin/env python
'''
From Jim Frank,

Gains, calculated in two different ways: 1 floating point number per
amplifier, 16 amplifiers 

Noise, calculated in two different ways: 1 floating poing number per
amplifier, 16 amplifiers Strings of files analyzed for the noise
analysis Information about

'cold spots': if cold spot found in any amplifier, strings are created
containing 'amp#, number of pixels with low response, x-y location of
spots for all spots found...(maybe up to n_spot_max locations)
'''


linear_fit_gains = [1.4572438, 0.37302515, 1.3140824, 
                    0.4068296, 1.3867835, 0.35201603,
                    1.3657773, 0.52264518, 1.2855487,
                    1.2655851, 1.3183337, 1.3410149, 
                    1.2750523, -0.011732696, 1.244482,
                    1.321605]

median_gains = [1.3775581121444702, 1.3544012308120728, 1.3438643217086792,
                1.4176301956176758, 1.3420248031616211, 1.3762127161026001,
                1.3616477251052856, 1.346621036529541, 1.2526081800460815, 
                1.3216733932495117, 1.3206708431243896, 1.3494513034820557, 
                1.2954639196395874, 0, 1.2805390357971191, 
                1.3580198287963867]

overscan_noise = [3.6349176024447241, 5.0803160657704165, 3.7611882576354776,
                  4.1825168577813292, 3.7870860180107475, 4.7791443484294343,
                  3.803611821759024, 4.1700321304217791, 5.3516890952179761, 
                  4.567408746351699, 4.5286492536406477, 4.3512778744438974, 
                  4.3783375662173425, 27.241841668653755, 4.7022006982103601, 
                  3.8474055279987058]

stddev_noise = [3.4675993788979267, 3.8130243903933319, 3.5896886777892139, 
                3.5447938323969193, 3.6777452958038537, 3.599257407154167, 
                3.7090086568698353, 3.8826428047533503, 5.2779119514087727, 
                4.6063258782349044, 4.4775588092356786, 4.3754068096469618, 
                4.3582311404977654, 14.413842712760189, 4.6319668234301501, 
                3.8080911964676485]

analyzed_files = [ '112_01_ptc_higain_00.00s_flat1.fits', 
                   '112_01_ptc_higain_00.00s_flat2.fits']

cold_spots = [
    (2, 161, (155, 360), (1928, 279), (204, 325), (1937, 304), (899, 397)),
    (5, 234, (642, 148), (619, 153), (1267, 102)),
    (6, 33, (1891, 174), (1546, 207)),
    (8, 35, (1531, 180), (370, 226)),
    (9, 170, (590, 477), (1953, 272), (569, 497), (2001, 511)),
    (10, 98, (969, 383), (95, 203), (1219, 92)),
    (12, 145, (1652, 257), (1673, 233), (644, 1)),
    (13, 45, (1477, 423), (1504, 416), (1927, 330)),
    (14, 48, (1477, 423), (1504, 416), (1927, 330)),
    (15, 33, (1828, 324), (163, 505), (29, 18))]




def primary_hdu(test_name, test_date, commit_hash):
    '''
http://heasarc.gsfc.nasa.gov/docs/heasarc/ofwg/docs/rates/ogip_93_003/ogip_93_003.html
http://heasarc.nasa.gov/docs/heasarc/ofwg/ofwg_recomm.html
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

def gain_noise_payload(lgain, mgain, onoise, snoise, spots, flist):
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
    lc = Column(name='FileName', format='A64', array=np.array(flist))
    ft = new_table([lc])
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
    ampnum = np.array([], dtype = np.int16)
    pixcount = np.array([], dtype = np.int16)
    spotx = np.array([], dtype = np.int16)
    spoty = np.array([], dtype = np.int16)
    
    for spot in spots:
        an = spot[0]
        nc = spot[1]
        nspots = len(spot[2:])
        nper = nc/nspots
        for x,y in spot[2:]:
            ampnum = np.append(ampnum, an)
            pixcount = np.append(pixcount, nper)
            spotx = np.append(spotx, x)
            spoty = np.append(spoty, y)
            continue            # over spots in amp
        continue                # over all amps
    anc = Column(name='AmpNum', format='I', array=ampnum)
    pcc = Column(name='PixCount', format='I', array=pixcount)
    sxc = Column(name='SpotX', format='I', array=spotx)
    syc = Column(name='SpotY', format='I', array=spoty)

    ct = new_table([anc,pcc,sxc,syc])
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
                            analyzed_files)

    hdul = HDUList([phdu]+pl)
    hdul.writeto(filename, checksum=True)
    
    
