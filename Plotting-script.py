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

    ax.scatter('mass_best','ssfr_best',c='b',s=8,data=agns,label='AGNs')
    ax.scatter('mass_best','ssfr_best',c='r',s=8,data=gals,label='Galaxies')

    ax.legend()

    ax.set_title('Log of specific SFR against the Log of total stellar mass')

    ax.set_xlabel('Total mass $Log_(10)(M_\odot)$')
    ax.set_ylabel('Specific Star Forming Rate $Log_(10)$')
    ax.set_ylim(top=-5,bottom=-20)
    ax.set_xlim(left=8.5,right=12)

    plt.show()

i = 1
while i <= 10:
    ssfr_mass_graph(i)
    i+=1





