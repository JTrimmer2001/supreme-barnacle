import numpy as np
from scipy import stats
from astropy.io import fits
import pandas as pd



'''
Simple script to run a ksample anderson darling test on two data sets

This script will be used for comparing a set of agns to a wider set of galaxies in the cosmos field
It should be easily adaptable to other tests, and I may later incorporate it into a larger file with a number of useful functions

For the time being, change the parameters to test within the code itself




with fits.open('/Users/Jet26/Documents/Data/Graph plotting/nonAGNLim') as hdu:
    data_agn = hdu[1].data
    mass_agn = data_agn.field('mass_best')
    zpdf_agn = data_agn.field('zpdf')   # This converts the relevant column in the fits file into a 1D numpy array
    ssfr_agn = data_agn.field('sfr_best')

with fits.open('/Users/Jet26/Documents/Data/Graph plotting/AGNLim') as hdu:
    data_nagn = hdu[1].data
    mass_nagn = data_nagn.field('mass_best')
    zpdf_nagn = data_nagn.field('zpdf')
    ssfr_nagn = data_nagn.field('sfr_best')

# Now the important data has been unloaded into variables, we can begin doing tests

res_mass = stats.anderson_ksamp((mass_agn,mass_nagn)) # mass test
res_zpdf = stats.anderson_ksamp((zpdf_agn,zpdf_nagn)) # reshift test
res_sfr = stats.anderson_ksamp((ssfr_agn,ssfr_nagn)) # sfr test

print(res_mass)
input()
print(res_zpdf)
input()
print(res_sfr)

'''
def radiosorted():
    data = pd.read_csv('Radio sorted.csv')

    loudness_index = data.columns.get_loc('Radio Loud')
    ssfr_index = data.columns.get_loc('ssfr_best')
    mass_index = data.columns.get_loc('mass_best')
    length = data.shape

    Loud = []
    quiet = []

    for i in range(length[0]):
        if np.isnan(data.iloc[i,loudness_index]) == True:
            quiet.append(data.iloc[i,ssfr_index])

        elif np.isnan(data.iloc[i,loudness_index])==False:
            Loud.append(data.iloc[i,ssfr_index])
            


    ssfr_matched = stats.anderson_ksamp((quiet,Loud))

    print(ssfr_matched)

def matchedstats(set=False):
    p_sfr = []
    p_ssfr = []
    p_mass = []
    p_zpdf = []

    if set==False:
        i = 1

        while i <= 10:
            data = pd.read_csv('Matched-2-catalogue/Set ' + str(i) + '.csv')

            agn_data = data[data['AGN or not'] == 0]
            gal_data = data[data['AGN or not'] == 1]

            p_sfr.append(stats.anderson_ksamp((agn_data['sfr_best'],gal_data['sfr_best'])).significance_level)
            p_ssfr.append(stats.anderson_ksamp((agn_data['ssfr_best'],gal_data['ssfr_best'])).significance_level)
            p_mass.append(stats.anderson_ksamp((agn_data['mass_best'],gal_data['mass_best'])).significance_level)
            p_zpdf.append(stats.anderson_ksamp((agn_data['zpdf_1'],gal_data['zpdf_1'])).significance_level)

            i+=1

    else:
        data = pd.read_csv('Matched-2-catalogue/Set ' + str(set) + '.csv')

        agn_data = data[data['AGN or not'] == 0]
        gal_data = data[data['AGN or not'] == 1]

        p_sfr.append(stats.anderson_ksamp((agn_data['sfr_best'],gal_data['sfr_best'])).significance_level)
        p_ssfr.append(stats.anderson_ksamp((agn_data['ssfr_best'],gal_data['ssfr_best'])).significance_level)
        p_mass.append(stats.anderson_ksamp((agn_data['mass_best'],gal_data['mass_best'])).significance_level)
        p_zpdf.append(stats.anderson_ksamp((agn_data['zpdf_1'],gal_data['zpdf_1'])).significance_level)

    print('sfr pvalues:  \b')
    print(p_sfr)
    print('ssfr pvalues: \b')
    print(p_ssfr)
    print('mass pvalues: \b')
    print(p_mass)
    print('zpdf pvalues: \b')
    print(p_zpdf)

matchedstats()


