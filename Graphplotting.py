from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt


'''
with fits.open("TOPCAT B") as BaseTable:
    rawdata = BaseTable[5].data

    mask = rawdata['type'] != 1
    nonstar = rawdata[mask]
    hdu = fits.BinTableHDU(data=nonstar)

    hdu.write('MatchedCosmos.fits')



with fits.open('NonStarMatchedCosmos.fits') as galtable:
    galdata = galtable[1].data

    mask1 = galdata['zpdf'] > 0.25
    interim = galdata[mask1]

    mask2 = interim['zpdf'] < 0.75
    redshiftlim = interim[mask2]

    hdu = fits.BinTableHDU(data=redshiftlim)

    hdu.writeto('RedshiftLimitedgalaxies.fits')
  
'''

def zpdfVabsmag():
    with fits.open('Limited Data set') as table:
        hdu = table[1].data
        zpdf = hdu.field('zpdf')

        absmag = hdu.field('m_r')

    plt.scatter(zpdf, absmag)
    plt.show()
    

    
