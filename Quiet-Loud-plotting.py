import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


agn_data = pd.read_csv('Radio sorted.csv')

radioLoud = agn_data[agn_data['Radio Loud'].notnull()]
radioQuiet = agn_data[agn_data['Radio Loud'].notnull() == False]

fig, ax = plt.subplots()

length = agn_data.shape
length = length[0]

radioindex = agn_data.columns.get_loc('Radio Loud')
massindex = agn_data.columns.get_loc('mass_best')
ssfrindex = agn_data.columns.get_loc('ssfr_best')

for i in range(length):

    if np.isnan(agn_data.iloc[i,radioindex]) == True: # If isnan is true then there is no radio loudness
        ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='r',marker='o',s=10,label='radio quiet')

    elif np.isnan(agn_data.iloc[i,radioindex]) == False:

        if agn_data.iloc[i,radioindex] >= 20:
            ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='g',marker='s',s=12,label='radio loud >= 20')

        elif agn_data.iloc[i,radioindex] >= 5:
            ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='b',marker='^',s=12,label='radio loud >= 5')

        else:
           ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='k',marker='d',s=12,label='radio loud') 


ax.set_xlabel('$Log_{10}$ total stellar mass $M_{\odot}$')
ax.set_ylabel('SSFR $year^{-1}$')

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

plt.show()