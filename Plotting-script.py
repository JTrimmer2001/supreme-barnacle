import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import pandas as pd




'''
This is intended to be a graphing script, code may be compartmentalised into functions but the functions should be reuseable easily

tables I want to do: Mass-SFR  
                     mass-redshift (again) [done]
                     Luminosity - redshift (maybe)
'''

def unifunction(x,y):
    data = pd.read_csv('Matched-2-catalogue/Set 1.csv',header = 0, delimiter=',')

    agns = data[data['AGN or not'] == 0]
    gals = data[data['AGN or not'] == 1]

    plt.scatter(x,y,c='b',s=2,data = agns)
    plt.scatter(x,y,c='r',s=2,data = gals)

    plt.xlabel(x)
    plt.ylabel(y)

    plt.show()


unifunction('ra_1','dec_1')