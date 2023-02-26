from astropy.io import fits
from astropy.table import table
import basic_stats as bs
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time



def newMatchset():
    #Im just going to start a new function because the old one was pretty cool
    matchesmade = int(0)

    #Loading in the data:

    with fits.open('/Users/Jet26/Documents/Data/Graph plotting/nonAGNLim') as hdu:
        data_gal = hdu[1].data
        gal_ids = data_gal.field('id')
        gal_ids = gal_ids.byteswap().newbyteorder()
        gal_zpdf = data_gal.field('zpdf')
        gal_zpdf = gal_zpdf.byteswap().newbyteorder()
        gal_mass = data_gal.field('mass_best') # These load the three important fields into their own numpy arrays
        gal_mass = gal_mass.byteswap().newbyteorder()

    with fits.open('/Users/Jet26/Documents/Data/Graph plotting/AGNLim') as hdu:
        data_agn = hdu[1].data
        agn_ids = data_agn.field('id') # ID allows the galaxy to be identified in the catalogues afterwards
        agn_ids = agn_ids.byteswap().newbyteorder()
        agn_zpdf = data_agn.field('zpdf') # zpdf is the redshift of the galaxy
        agn_zpdf = agn_zpdf.byteswap().newbyteorder()
        agn_mass = data_agn.field('mass_best') # mass_best is the best estimate for the mass
        agn_mass = agn_mass.byteswap().newbyteorder()

    gal_table = pd.DataFrame({
        'id': gal_ids,
        'zpdf': gal_zpdf,
        'mass': gal_mass,
    }) # Pandas data tables seem easy to use and allow for rows to be selected easily without needing to worry about losing track of whats what
    
    agn_table = pd.DataFrame({
        'id': agn_ids,
        'zpdf': agn_zpdf,
        'mass': agn_mass,
    })

    w1,w2,zpdf_bins = bs.weight_dist(gal_zpdf,agn_zpdf,return_bins=True)
    w1,w2,mass_bins = bs.weight_dist(gal_mass,agn_mass,return_bins=True) # generates a good set of bins for each histogram axis

    agn_histogram, xbins_agn, ybins_agn = np.histogram2d(agn_zpdf,agn_mass,[zpdf_bins,mass_bins]) # generates a histogram of the agn data
    gal_histogram, xbins_gal, ybins_gal = np.histogram2d(gal_zpdf,gal_mass,[zpdf_bins,mass_bins]) # generates histogram of non-agn data

    '''
    agn_subset = agn_table[agn_table['zpdf'] <= 0.7] 

    ^^^ This is how selecting pandas data works, doesnt seem to like having more than one expression at a time so will
    need to filter a few times for all data, thats chill tho
    '''

    master = pd.DataFrame(columns=('id','zpdf','mass')) # initialises an empty data frame for the sampled data to be appended to

    x=0
    for i_x in agn_histogram:
        y=0
        for i_y in i_x: # These nested loops loop through the histogram to see if there are more or less agns

            if i_y == 0: # begins checking the amount of agns in the square with 0 (to speed up process)
                print('\r','Skipped data at:',x,',',y,'                               matches made: ',matchesmade,'                 ',sep='',end='', flush = True)
                time.sleep(0.1) # slows the skipping so you can see whats going on

            elif i_y < gal_histogram[x,y]:


                agn_subset = agn_table[agn_table['zpdf'] >= xbins_agn[x]]
                agn_subset = agn_subset[agn_subset['zpdf'] <= xbins_agn[x+1]] # Upper and lower zpdf limit for current histogram position
                agn_subset = agn_subset[agn_subset['mass'] >= ybins_agn[y]]
                agn_subset = agn_subset[agn_subset['mass'] <= ybins_agn[y+1]] # Upper and lower mass limit for current histogram position

                gal_subset = gal_table[gal_table['zpdf'] >= xbins_gal[x]]
                gal_subset = gal_subset[gal_subset['zpdf'] <= xbins_gal[x+1]]
                gal_subset = gal_subset[gal_subset['mass'] >= ybins_gal[y]]
                gal_subset = gal_subset[gal_subset['mass'] <= ybins_gal[y+1]]

                gal_sample = gal_subset.sample(int(i_y) )# Takes a random sample of data in the set to match the amount in the agn set

                master = pd.concat([master,agn_subset,gal_sample], ignore_index=True, sort=False) # Concats the three tables together, ignoring index so thngs dont get confuse
                matchesmade += 2*i_y
                print('\r',i_y,'AGNs and', gal_histogram[x,y], 'Galaxies at',[x,y],'                 matches made: ',matchesmade,'  ',sep='',end='', flush = True)
                time.sleep(0.1)

            else: # This method includes cases when i_y > gal_histogram[x,y], decided this was best until proven otherwise to maintain the amount of agns

                agn_subset = agn_table[agn_table['zpdf'] >= xbins_agn[x]]
                agn_subset = agn_subset[agn_subset['zpdf'] <= xbins_agn[x+1]] # Upper and lower zpdf limit for current histogram position
                agn_subset = agn_subset[agn_subset['mass'] >= ybins_agn[y]]
                agn_subset = agn_subset[agn_subset['mass'] <= ybins_agn[y+1]] # Upper and lower mass limit for current histogram position

                gal_subset = gal_table[gal_table['zpdf'] >= xbins_gal[x]]
                gal_subset = gal_subset[gal_subset['zpdf'] <= xbins_gal[x+1]]
                gal_subset = gal_subset[gal_subset['mass'] >= ybins_gal[y]]
                gal_subset = gal_subset[gal_subset['mass'] <= ybins_gal[y+1]]  

                master = pd.concat([master, agn_subset, gal_subset], ignore_index=True, sort=False) # Concats tables, index are ignore as ID is the identifier
                matchesmade += 2*i_y
                print('\r',i_y,'AGNs and', gal_histogram[x,y], 'Galaxies at',[x,y],'                 matches made: ',matchesmade,'  ',sep='',end='', flush = True)
                time.sleep(0.1) # A note for another time: this whole progress thing would look alot nicer with the matches made bit at the front (not of particularly variable width)

            y+=1 # iterates y so the indices can be changed

        x+=1 

    master.info()
    #master.to_csv('Matched sets/Matched data10.csv')


newMatchset()