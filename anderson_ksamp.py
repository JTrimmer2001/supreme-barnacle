import numpy as np
from scipy import stats
from astropy.io import fits




'''
Simple script to run a ksample anderson darling test on two data sets

This script will be used for comparing a set of agns to a wider set of galaxies in the cosmos field
It should be easily adaptable to other tests, and I may later incorporate it into a larger file with a number of useful functions

For the time being, change the parameters to test within the code itself

'''


with fits.open('/Users/Jet26/Documents/Data/Graph plotting/nonAGNLim') as hdu:
    data_agn = hdu[1].data
    mass_agn = data_agn.field('mass_best')
    zpdf_agn = data_agn.field('zpdf')   # This converts the relevant column in the fits file into a 1D numpy array
    sfr_agn = data_agn.field('sfr_best')

with fits.open('/Users/Jet26/Documents/Data/Graph plotting/AGNLim') as hdu:
    data_nagn = hdu[1].data
    mass_nagn = data_nagn.field('mass_best')
    zpdf_nagn = data_nagn.field('zpdf')
    sfr_nagn = data_nagn.field('sfr_best')

# Now the important data has been unloaded into variables, we can begin doing tests

res_mass = stats.anderson_ksamp((mass_agn,mass_nagn)) # mass test
res_zpdf = stats.anderson_ksamp((zpdf_agn,zpdf_nagn)) # reshift test
res_sfr = stats.anderson_ksamp((sfr_agn,sfr_nagn)) # sfr test

print(res_mass)
input()
print(res_zpdf)
input()
print(res_sfr)