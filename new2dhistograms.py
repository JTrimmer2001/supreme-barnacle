import basic_stats as bs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['figure.figsize'] = [10,7]
plt.rcParams['font.size'] = 13

nonagn_data = pd.read_csv('/Users/Owner/Documents/Coding/LimitedData-nonAgns.csv',low_memory=False)

nonagn_useful = nonagn_data[['zpdf','mass_best','ssfr_best']].copy()
x1 = nonagn_data[['zpdf']].copy()
x1 = x1.to_numpy()
x2 = nonagn_data[['mass_best']].copy()
x2 = x2.to_numpy()
del nonagn_data

all_data = pd.read_csv('/Users/Owner/Documents/Coding/LimitedData.csv',low_memory=False)

all_useful = all_data[['zpdf','mass_best','ssfr_best']].copy()
del all_data

agn_data = pd.read_csv('Radio sorted.csv')

y = agn_data[['zpdf']].copy()
w1,w2,binsx = bs.weight_dist(x1,y,return_bins=True)
zrescale = w2*100

y = agn_data[['mass_best']].copy()
w1,w2,binsy = bs.weight_dist(x2,y,return_bins=True)
mrescale=w2*100

fig, ax = plt.subplots(2,2,width_ratios=[0.7,0.3],height_ratios=[0.3,0.7])

pcm = ax[1,0].hist2d('zpdf','mass_best',bins=[binsx,binsy],data= all_useful,cmap='Greys_r')
scatter1 = ax[1,0].scatter('zpdf','mass_best',data=agn_data,c='r',s=8,label='AGNs')
ax[1,0].set_xlabel('redshift')
ax[1,0].set_ylabel('mass')
xlim = ax[1,0].get_xlim()
ylim = ax[1,0].get_ylim()

hist1 = ax[0,0].hist(agn_data['zpdf'],binsx,histtype='step',color='b',label='AGNs (x100)',weights=zrescale)
hist2 = ax[0,0].hist(nonagn_useful['zpdf'],binsx,histtype='step',color='r',label='non AGNs')
ax[0,0].set_xlim(xlim)
ax[0,0].set_xticks([])
ax[0,0].set_yticks([])

ax[1,1].hist(agn_data['mass_best'],binsy,histtype='step',color='b',orientation='horizontal',weights=mrescale)
ax[1,1].hist(nonagn_useful['mass_best'],binsy,histtype='step',color='r',orientation='horizontal')
ax[1,1].set_ylim(ylim)
ax[1,1].set_xticks([])
ax[1,1].set_yticks([])

ax[0,1].axis('off')

fig.legend(loc='upper right',borderaxespad = 3)

plt.tight_layout()
plt.show()