from astropy.io import fits
import basic_stats as bs
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

def starfilter():
    with fits.open("TOPCAT B") as BaseTable: #This isnt in this directory anymore lol
        rawdata = BaseTable[5].data

        mask = rawdata['type'] != 1
        nonstar = rawdata[mask]
        hdu = fits.BinTableHDU(data=nonstar)

        hdu.write('MatchedCosmos.fits')


def redshiftlimit(): 
    with fits.open('Limited Data set') as galtable:
        galdata = galtable[1].data

        mask1 = galdata['zpdf'] >= 0.25
        interim = galdata[mask1]

        mask2 = interim['zpdf'] <= 0.9
        redshiftlim = interim[mask2]

        hdu = fits.BinTableHDU(data=redshiftlim)

        hdu.writeto('RedshiftLimitedgalaxies.fits', overwrite = True)



def zpdfVabsmag():
    with fits.open('RedshiftLimitedgalaxies.fits') as table:
        hdu = table[1].data
        zpdf = hdu.field('zpdf')

        absmag = hdu.field('m_r')

    plt.scatter(zpdf, absmag,s=1, c='r')
    plt.gca().invert_yaxis()
    plt.show()
    

def histograms2d(file):
    with fits.open(file) as table:
        data = table[1].data


def histogram2D():
    with fits.open('RedshiftLimitedgalaxies.fits') as table:
        hdu = table[1].data
        zpdf = hdu.field('zpdf')

        sfr = hdu.field('mass_best')

    param = bs.weight_dist(zpdf,sfr)

    fig = px.density_heatmap(x = zpdf, y = sfr,nbinsx=30,nbinsy=30,color_continuous_scale='viridis',text_auto = True,labels=dict(x="zpdf",y='mass_best'))

    fig.show()

histogram2D()
