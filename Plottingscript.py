import matplotlib.pyplot as plt
from astropy.io import fits
import pandas as pd
from pandas import DataFrame as df
import numpy as np
import seaborn as sns
import matplotlib
import basic_stats as bs

matplotlib.rcParams.update({'font.size':16})

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

def getbigdata(x,y):
    big_data = pd.read_csv("/Users/Jet26/Documents/Data/Graph plotting/LimitedData.csv",low_memory=False)

        #On the above function, low_memory was used to suppress an error so it stopped coming up
        # I believe it removes a memory cap for the pandas function, so if youre using a computer with low memory capacity maybe take this bit out?

    limited_data = big_data.filter([x,y], axis=1)
    
    return(limited_data)

def ssfr_mass_graph(filenum,contour_data): 

    data = pd.read_csv('Matched-2-catalogue/Set ' + str(filenum) + '.csv',header = 0, delimiter=',')

    agns = data[data['AGN or not'] == 0]
    gals = data[data['AGN or not'] == 1] # Pandas operation to make two data frames from the full data frame
                                         # Pandas is really nice like that, basically just a filter but it takes the rest of the data too
                                         # no need to match the data back up afterwards
    '''
    x1 = agns['ssfr_best'].to_numpy()
    x1 = logmoment(x1)
    x2 = gals['ssfr_best'].to_numpy()
    x2 = logmoment(x2)
    '''

    fig, ax = plt.subplots() # This just initialises an instance for plotting, is a bit nicer than just using plt.plot or whatever
    # I honestly dont know why the fig, bit is needed but it doesnt seem to work without it????

    plt.subplots_adjust(bottom=0.15,top=0.95,left=0.15,right=0.95)

    sns.kdeplot(data=contour_data,x='mass_best',y='sfr_best',cmap='viridis',zorder=1) 
    # Seaborn (sns here) does contour plots really well, just needs an x and y input and its all sorted
    #In general, the 'data' parameter tells the function where to get data from, here it takes data from 'contour_data' with the x coords being
    #   'mass_best' and y being 'ssfr_best', both of these are column names from the 'contour_data' data frame

    #zorder determines which plot is made first, here the lines are in the background so zorder is 1
    #cmap just sets a colour scheme for the contour lines, if you want a different map theres a list here: https://matplotlib.org/stable/gallery/color/colormap_reference.html

    ax.scatter('mass_best','sfr_best',c='b',s=13,data=agns,marker='^',label='AGNs',zorder=2)
    ax.scatter('mass_best','sfr_best',c='r',s=13,data=gals,label='Galaxies',zorder=3)
    # This does the scattering of the agn and non-agn points
    # All the formatting is done in the arguments (c,s,data, etc)
    # c is the colour, s is the size, marker is the shape of the point
    # some of these can take multiple different input formats, please see the matplotlib documentation for each function

    ax.set_xlabel('Total Mass $Log_{10}M_{\odot}$')
    ax.set_ylabel('SFR $Log_{10} year^{-1}$')
    ax.set_ylim(bottom=-10)
    ax.set_xlim(left=7,right=11.8)
    #add background of wider cosmos galaxy samples - contour plot [DONE]
    #histogram of ssfr and mass
    #anderson-darling for ssfr [done]
    #save plots with overwrite mode [done]

    ax.legend(loc='lower left')

    plt.savefig('Plots/sfr-stellarmass/set ' + str(filenum) + '.png')
    #plt.show()

'''i = 1
big_data = getbigdata('mass_best','sfr_best')
while i <= 10:
    ssfr_mass_graph(i,big_data)
    i+=1'''



def bolometric(filenum):
 
    #begin with finding the bolometric corrected luminosities of the galaxies 
    #import the correction table and get python to read ecah column
    lxcorr_table = pd.read_csv('/Users/Jet26/Documents/Data/Graph plotting/lglx_kbol_tuv09.csv')
    
    xp = lxcorr_table["LX_hard_corr"]
    #print(xp)
    fp = lxcorr_table["bolometric_correction"]
    #print(fp)
    

    lx_data_point = pd.read_csv('Matched-2-catalogue/Set '+str(filenum)+'.csv')

    agns = lx_data_point[lx_data_point['AGN or not'] == 0]


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
    
    '''making redshift bins

    redhsift1 = agns[agns['zpdf_2']<0.38 & agns['zpdf_2']>=0.25]
    redshift2 = agns[agns['zpdf_2']<0.51 & agns['zpdf_2']>=0.38]
    redshift3 = agns[agns['zpdf_2']<0.64 & agns['zpdf_2']>=0.51]
    redshift4 = agns[agns['zpdf_2']<0.77 & agns['zpdf_2']>=0.64]
    redshift5 = agns[agns['zpdf_2']<0.9 & agns['zpdf_2']>=0.77]
    '''
    #Log_(BH) = 1.12Log(M*)-4.12

    length = agns_useful.shape
    avg_lum = np.zeros(shape=(length[0]))

    for i in range(length[0]):
        if np.isnan(agns_useful.iloc[i,0])==True: #Checks if the xmm luminosity is nan
            avg_lum[i] = agns_useful.iloc[i,1] #If xmm lum is nan at this index, takes into account the chandra lum

        else:
            avg_lum[i] = agns_useful.iloc[i,0] #If chandra lum is nan, takes xmm luminosity


    agns_useful['avg_lum'] = avg_lum # Adds the list to the data frame as a column

    #if one take that, if the other take that one, not avg maybe

    bhmass = []
    for i in agns_useful['mass']:
        y = 1.12*i - 4.12 # Finds Black hole mass
        bhmass.append(y)

    bolo_lum = []
    for i_lum in agns_useful['avg_lum']:
        bolo = np.interp(i_lum,xp,fp) # Interpolates luminosities to a correction table to find bolo luminosity
        
        bolo_lum.append(np.log10(bolo)+i_lum)


    agns_useful['bhmass'] = bhmass
    agns_useful['bolo_lum'] = bolo_lum # Adds these lists to the data frame as a table

    ratios = [1,0.1,0.01,0.001]
    
    fig, ax = plt.subplots() # Intend to make a plot with different colours for redshift bands
                             # thinking 5 bands between 0.25 and 9, whatever spacing that is

    for i in range(length[0]):

        if agns_useful.iloc[i, 3] <= 0.4:
            ax.scatter()

    ratioline = []

    for i in ratios:
        x = np.linspace(5.5,9,100)


    ax.set_xlabel('Black hole mass $Log_{10}$ $M_{BH}/M_{/odot}$')
    ax.set_ylabel('Bolometric Luminosity $Log_{10}$ $L_{bol}$')
    ax.set_xlim(left=5.84,right=8.74)
    ax.set_ylim(bottom=44.63,top=46.82)
    
    plt.show()


# eddington lum:
# L = 1.26*10^38 (M[BH]/M[sol])

def doublehistogram():
    '''Need a pair of histograms demonstrating that the matching of the data worked properly'''

    #plt.rcParams['figure.figsize'] = [10,7]
    plt.rcParams['font.size'] = 13

    data = pd.read_csv('Matched-2-catalogue/Set 1.csv')

    agn = data[data['AGN or not'] == 0]
    gal = data[data['AGN or not'] == 1]
    
    w1,w2,bins_mass = bs.weight_dist(agn['mass_best'],gal['mass_best'],return_bins=True)
    w1,w2,bins_zpdf = bs.weight_dist(agn['zpdf_1'],gal['zpdf_1'],return_bins=True)
    '''
    print(agn['mass_best'].max(),agn['mass_best'].min())
    print(gal['mass_best'].max(),gal['mass_best'].min())
    print(agn['zpdf_1'].max(),agn['zpdf_1'].min())
    print(gal['zpdf_1'].max(),gal['zpdf_1'].min())
    '''
    '''
    del bins_mass[::2]
    del bins_zpdf[::2]
    '''
    fig, [ax1,ax2] = plt.subplots(1,2)

    ax1.hist('mass_best',color='b',bins=bins_mass[1::2],data=agn,histtype='step',label='AGNs')
    ax1.hist('mass_best',color='r',bins=bins_mass[1::2],data=gal,histtype='step',label='non-AGNs')
    ax1.set_xlabel('Mass $M_{\odot}$')
    ax1.legend(bbox_to_anchor=(0.5, 1.02, 1., .102), loc='lower left', mode="expand", borderaxespad=0.,ncol = 2)

    ax2.hist('zpdf_1',color='b',bins=bins_zpdf[1::2],data=agn,histtype='step')
    ax2.hist('zpdf_1',color='r',bins=bins_zpdf[1::2],data=gal,histtype='step')
    ax2.set_xlabel('Redshift')

    plt.tight_layout()
    plt.show()

    
doublehistogram()