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

redshiftindex = agn_data.columns.get_loc('zpdf')
massindex = agn_data.columns.get_loc('mass_best')
ssfrindex = agn_data.columns.get_loc('ssfr_best')

for i in range(length):

    if agn_data.iloc[i,redshiftindex] <= 0.4: # If isnan is true then there is no radio loudness
        ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='r',marker='o',s=12,label='z <= 0.4',zorder=1)

    elif agn_data.iloc[i,redshiftindex] <= 0.55:
        ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='b',marker='^',s=12,label='0.4 < z <= 0.55',zorder=1)

    elif agn_data.iloc[i,redshiftindex] <= 0.7:
        ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='g',marker='X',s=12,label='0.55 < z <= 0.7',zorder=1)

    else:
        ax.scatter(agn_data.iloc[i,massindex],agn_data.iloc[i,ssfrindex], c='k',marker='s',s=12,label='0.7 < z',zorder=1)

ax.set_xlabel('$Log_{10}$ total stellar mass $M_{\odot}$')
ax.set_ylabel('SSFR $year^{-1}$')

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

plt.show()