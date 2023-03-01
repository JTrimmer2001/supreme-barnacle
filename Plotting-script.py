import matplotlib.pyplot as plt
from astropy.io import fits
import pandas as pd
from pandas import DataFrame as df
import numpy as np




'''
This is intended to be a graphing script, code may be compartmentalised into functions but the functions should be reuseable easily

tables I want to do: Mass-SFR  
                     mass-redshift (again) [done]
                     Luminosity - redshift (maybe)
                     log(ssfr) - log(Mstar)
                     BoloL against black hole mass
'''
def logmoment(x):
    y=[]

    for i in x:
        log = np.log10(i)
        y.append(log)
    return y 


def ssfr_mass_graph(filenum):
    data = pd.read_csv('Matched-2-catalogue/Set ' + str(filenum) + '.csv',header = 0, delimiter=',')

    agns = data[data['AGN or not'] == 0]
    gals = data[data['AGN or not'] == 1]
    '''
    x1 = agns['ssfr_best'].to_numpy()
    x1 = logmoment(x1)
    x2 = gals['ssfr_best'].to_numpy()
    x2 = logmoment(x2)
    '''

    fig, ax = plt.subplots()

    ax.scatter('mass_best','sfr_best',c='b',s=8,data=agns,label='AGNs')
    ax.scatter('mass_best','sfr_best',c='r',s=8,data=gals,label='Galaxies')

    ax.legend()

    ax.set_title('Log of specific SFR against the Log of total stellar mass')

    ax.set_xlabel('Total mass $Log_(10)(M_\odot)$')
    ax.set_ylabel('Specific Star Forming Rate $Log_(10)$')
    #ax.set_ylim(top=-5,bottom=-20)
    #ax.set_xlim(left=8.5,right=12)

    plt.show()
'''
i = 1
while i <= 10:
    ssfr_mass_graph(i)
    i+=1
'''


def bolometric():
 
    #begin with finding the bolometric corrected luminosities of the galaxies 
    #import the correction table and get python to read ecah column
    lxcorr_table = pd.read_csv('/Users/Owner/Documents/Coding/lglx_kbol_tuv09.csv')
    
    xp = lxcorr_table["LX_hard_corr"]
    #print(xp)
    fp = lxcorr_table["bolometric_correction"]
    #print(fp)
    
    lx_data_point = pd.read_csv('Matched-2-catalogue/Set 1.csv')

    agns = lx_data_point[lx_data_point['AGN or not'] == 0]
    gals = lx_data_point[lx_data_point['AGN or not'] == 1]


    '''Ill put it here so its easier to see in a nice bright colour:
    Need to plot the bolometric luminosity against the black hole mass
    
    BH mass comes from a formula involving mass_best and constants, nothing fancy - can use a similar method to the logmoment function (albeit with differet maths obviously)
    Bolometric luminosity comes form interpolating with xp and lp, this is where x comes in
    
    agns_ and gals_bolo are arrays of bolometric luminosities
    
    Note- with the current method, details of the source type (AGN or nah) are lost.
        Produce a second data frame from the first containing only AGNs and the other being an inverse of this
        Then the two frames can be dealt with sepereately and allows data cleanliness to be maintained
        Then obviously just plot the two together, sort the data into smaller redshift bins'''
    
    agns_useful = agns[['log_final_lum_xmm','log_final_lum_chandra','mass','zpdf_2']].copy()
    gals_useful = gals[['log_final_lum_xmm','log_final_lum_chandra','mass','zpdf_2']].copy()

    #Log_(BH) = 1.12Log(M*)-4.12

    length = agns_useful.shape
    avg_lum = np.zeros(shape=(length[0]))

    for i in range(length[0]):
        if np.isnan(agns_useful.iloc[i,0])==True: #Checks if the xmm luminosity is nan
            avg_lum[i] = agns_useful.iloc[i,1] #If xmm lum is nan at this index, takes into account the chandra lum

        elif np.isnan(agns_useful.iloc[i,1])==True:
            avg_lum[i] = agns_useful.iloc[i,0] #If chandra lum is nan, takes xmm luminosity

        else:
            average = agns_useful.iloc[i,0] + agns_useful.iloc[i,1]
            avg_lum[i] = average/2 # takes the average of the two luminosities if theyre both present

    agns_useful['avg_lum'] = avg_lum # Adds the list to the data frame as a column

    bhmass = []
    for i in agns_useful['mass']:
        y = 1.12*i - 4.12 # Finds Black hole mass
        bhmass.append(y)

    bolo_lum = []
    for i_lum in agns_useful['avg_lum']:
        bolo = np.interp(i_lum,xp,fp) # Interpolates luminosities to a correction table to find bolo luminosity
        bolo_lum.append(bolo)


    agns_useful['bhmass'] = bhmass
    agns_useful['bolo_lum'] = bolo_lum # Adds these lists to the data frame as a table

    fig, ax = plt.subplots() # Intend to make a plot with different colours for redshift bands
                             # thinking 5 bands between 0.25 and 9, whatever spacing that is

    ax.scatter('bhmass','bolo_lum',c='r',s=8,data=agns_useful)
    ax.set_ylim(top=48,bottom=42) # this seems to be giving weird results? Doesnt seem to show any pattern when compared to other results

    plt.show()



    
bolometric()


# eddington lum:
# L = 1.26*10^38 (M[BH]/M[sol])
