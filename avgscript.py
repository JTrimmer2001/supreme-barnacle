import pandas as pd
import numpy as np

i = 1

while i <=10:
    data = pd.read_csv('Matched-2-catalogue/Set ' + str(i) + '.csv')
    data_agns = data[data['AGN or not'] == 0]
    data_gals = data[data['AGN or not'] == 1]

    data_agns.mean()