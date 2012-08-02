#!/usr/bin/env
'''
Some example data from Jim Frank to fill a PTC schema.

'''

#: Example data for the PtcAmpTableHDU:


LinearGain = [
    1.4572438, 0.37302515, 1.3140824, 0.40682960, 
    1.3867835, 0.35201603, 1.3657773, 0.52264518,
    1.2855487, 1.26558510, 1.3183337, 1.34101490, 
    1.2750523, -0.011732696, 1.244482, 1.321605]

MedianGain = [
    1.3775581121444702, 1.3544012308120728, 1.3438643217086792,
    1.4176301956176758, 1.3420248031616211, 1.3762127161026001,
    1.3616477251052856, 1.346621036529541, 1.2526081800460815, 
    1.3216733932495117, 1.3206708431243896, 1.3494513034820557, 
    1.2954639196395874, 0, 1.2805390357971191, 
    1.3580198287963867]

OverScanNoise = [
    3.6349176024447241, 5.0803160657704165, 3.7611882576354776,
    4.1825168577813292, 3.7870860180107475, 4.7791443484294343,
    3.803611821759024, 4.1700321304217791, 5.3516890952179761, 
    4.567408746351699, 4.5286492536406477, 4.3512778744438974, 
    4.3783375662173425, 27.241841668653755, 4.7022006982103601, 
    3.8474055279987058]

StdDevNoise = [
    3.4675993788979267, 3.8130243903933319, 3.5896886777892139, 
    3.5447938323969193, 3.6777452958038537, 3.599257407154167, 
    3.7090086568698353, 3.8826428047533503, 5.2779119514087727, 
    4.6063258782349044, 4.4775588092356786, 4.3754068096469618, 
    4.3582311404977654, 14.413842712760189, 4.6319668234301501, 
    3.8080911964676485]

LinearRangeMin = [
    2823.37696145, 3363.92126418, 2884.43321090, 
    3235.15399556, 2939.34630959, 3361.84491382, 
    2848.64347043, 2043.12254248, 1929.16075318, 
    2033.47952452, 2659.58007023, 3724.17801655, 
    3243.12833421, 2617.01368638, 2552.21401493, 
    2645.14063128]

LinearRangeMax = [
    37128.7915286, 36400.9073340, 37086.5943257,
    36391.0308101, 37512.0427495, 37185.8362640,
    37090.7744662, 39876.0583927, 35149.2702176,
    32688.0410648, 34688.4983750, 31930.3124836,
    34816.5848581, 31964.3730567, 32947.6380666,
    35783.2214620]

FullWell = [
    36049.506329113923, 35151.949367088608, 36075.678481012656,
    34945.617721518989, 36073.802531645568, 35700.691139240509, 
    35653.868354430379, 38417.741772151901, 33887.265822784808, 
    31785.448101265822, 33297.453164556959, 30653.405063291139,
    33733.111392405066, 30824.529113924051, 32718.886075949365, 
    34186.010126582281,
    ]


#: Not yet provided, but specified.
PRNUTotal  = [0.0]*16
PRNUCorrected = [0.0]*16
LinRangeMin = [0.0]*16
LinRangeMax = [0.0]*16
LinearResponse = [0.0]*16


#: 
analyzed_files = [ '112_01_ptc_higain_00.00s_flat1.fits', 
                   '112_01_ptc_higain_00.00s_flat2.fits']

_cold_spots = [
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
    
ampnum = []
pixcount = []
spotx = []
spoty = []
for spots in _cold_spots:
    n = spots[0]
    c = spots[1]
    for x,y in spots[2:]:
        ampnum.append(n)
        pixcount.append(c)
        spotx.append(x)
        spoty.append(y)
        continue
    continue
