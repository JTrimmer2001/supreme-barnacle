import pandas as pd
import numpy as np

i = 1

data = pd.read_csv('Matched-2-catalogue/Set 1.csv',header = 0, delimiter=',')

agns = data[data['AGN or not'] == 0]
gals = data[data['AGN or not'] == 1]

a,b = np.polyfit(agns['mass_best'],agns['sfr_best'],1)
c,d = np.polyfit(gals['mass_best'],gals['sfr_best'],1)

print('a: ',a)
print('b: ',b)
print('c: ',c)
print('d: ',d)