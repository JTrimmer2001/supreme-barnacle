from astropy.io import fits
import basic_stats as bs
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def starfilter():
    with fits.open("TOPCAT B") as BaseTable: #This isnt in this directory anymore lol
        rawdata = BaseTable[5].data

        mask = rawdata['type'] != 1
        nonstar = rawdata[mask]
        hdu = fits.BinTableHDU(data=nonstar)

        hdu.write('MatchedCosmos.fits')


def redshiftlimit(): 
    with fits.open('/Users/Jet26/Documents/Data/Graph plotting/AGNLim') as galtable:
        galdata = galtable[1].data

        mask1 = galdata['zpdf'] > 0.25
        interim = galdata[mask1]

        mask2 = interim['zpdf'] < 0.9
        redshiftlim = interim[mask2]

        hdu = fits.BinTableHDU(data=redshiftlim)

        hdu.writeto('RedshiftLimitedAGNs.fits', overwrite = True)



def zpdfVabsmag():
    with fits.open('RedshiftLimitedAGNs.fits') as table:
        hdu = table[1].data
        zpdf = hdu.field('zpdf')

        absmag = hdu.field('m_r')

    plt.scatter(zpdf, absmag,s=1, c='r')
    plt.gca().invert_yaxis()
    plt.show()
    

def histogram2D():
    with fits.open('RedshiftLimitedgalaxies.fits') as table:
        hdu = table[1].data
        zpdf = hdu.field('zpdf')

        sfr = hdu.field('ssfr_best')


    fig = px.density_heatmap(x = zpdf, y = sfr,nbinsx=30,nbinsy=30,color_continuous_scale='viridis',text_auto = True,labels=dict(x="zpdf",y='ssfr_best'))

    fig.show()


def RedshiftHistogram():
    with fits.open('RedshiftLimitedAGNs.fits') as table:
        hdu = table[1].data
        zpdfagn = hdu.field('zpdf')
        zpdfagn = zpdfagn

    with fits.open('nonAGNLimit.fits') as table:
        hdu2 = table[1].data
        zpdf = hdu2.field('zpdf')

    weights = bs.weight_dist(zpdfagn, zpdf, return_bins= True)

    bins = weights[2]

    minbin = np.min(bins)
    maxbin = np.max(bins)
    diff = np.mean(np.diff(bins))

    fig = go.Figure()

    fig.add_trace(go.Histogram(x = zpdfagn, histnorm ='percent' , name = 'AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))
    fig.add_trace(go.Histogram(x = zpdf, histnorm = 'percent', name = 'Non-AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))

    fig.update_layout(title_text = 'redshift of AGN galaxies compared to non-AGN galaxies (%)', xaxis_title_text = 'redshift', yaxis_title_text = 'count', barmode = 'overlay')
    fig.show()


def masshistogram():
    with fits.open('RedshiftLimitedAGNs.fits') as table:
        hdu = table[1].data
        massagn = hdu.field('mass_best')

    with fits.open('nonAGNLimit.fits') as table:
        hdu2 = table[1].data
        mass = hdu2.field('mass_best')

    weights = bs.weight_dist(massagn, mass, return_bins= True)

    bins = weights[2]

    minbin = np.min(bins)
    maxbin = np.max(bins)
    diff = np.mean(np.diff(bins))

    fig = go.Figure()

    fig.add_trace(go.Histogram(x = massagn, name = 'AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))
    fig.add_trace(go.Histogram(x = mass, name = 'Non-AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))

    fig.update_layout(title_text = 'mass of AGN galaxies compared to non-AGN galaxies (%)', xaxis_title_text = 'mass', yaxis_title_text = 'count', barmode = 'overlay')
    fig.show()    


def sfrhistogram():
    with fits.open('RedshiftLimitedAGNs.fits') as table:
        hdu = table[1].data
        sfragn = hdu.field('sfr_best')

    with fits.open('nonAGNLimit.fits') as table:
        hdu2 = table[1].data
        sfr = hdu2.field('sfr_best')

    weights = bs.weight_dist(sfragn, sfr, return_bins= True)

    bins = weights[2]

    minbin = np.min(bins)
    maxbin = np.max(bins)
    diff = np.mean(np.diff(bins))

    fig = go.Figure()

    fig.add_trace(go.Histogram(x = sfragn , name = 'AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))
    fig.add_trace(go.Histogram(x = sfr, name = 'Non-AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))

    fig.update_layout(title_text = 'sfr of AGN galaxies compared to non-AGN galaxies', xaxis_title_text = 'rate', yaxis_title_text = 'count', barmode = 'overlay')
    fig.show() 


def customsfrhistogram():
    with fits.open('RedshiftLimitedAGNs.fits') as table:
        hdu = table[1].data
        sfragn = hdu.field('sfr_best')

    with fits.open('nonAGNLimit.fits') as table:
        hdu2 = table[1].data
        sfr = hdu2.field('sfr_best')


    weights = bs.weight_dist(sfragn, sfr, return_bins= True)

    bins = weights[2]

    minbin = np.min(bins)
    maxbin = np.max(bins)
    diff = np.mean(np.diff(bins))


    fig = go.Figure()

    fig.add_trace(go.Histogram(x = sfragn, histnorm='percent' , name = 'AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))
    fig.add_trace(go.Histogram(x = sfr, histnorm='percent', name = 'Non-AGN', xbins= dict(start= minbin, end= maxbin, size= diff), opacity = 0.75))

    fig.update_layout(title_text = 'sfr of AGN galaxies compared to non-AGN galaxies', xaxis_title_text = 'rate', yaxis_title_text = 'count', barmode = 'overlay')
    fig.show() 


def statshist():

    with fits.open('RedshiftLimitedAGNs.fits') as table:
        hdu = table[1].data
        massagn = hdu.field('mass_med')

    with fits.open('nonAGNLimit.fits') as table:
        hdu = table[1].data
        mass = hdu.field('mass_med')

    
    weights = bs.weight_dist(massagn, mass, return_bins= True)

    w1 = weights[0]
    w2 = weights[1]
    bins = weights[2]

    agn = np.histogram(massagn,bins= bins, weights=w1)
    nonagn = np.histogram(mass, bins, weights=w2)


    print(agn)
    print(nonagn)

    plt.hist(agn[0], agn[1])
    plt.hist(nonagn[0], nonagn[1])
    plt.show()



def matchsets():
    '''
    The goal of this function is to match data points from the non-agn sample to the agn sample.
    This script will use picking to select points so that we have the same amount of AGN and nonAGN data.
    Will use np.histogram2d to group data (specified using basic_stats or linspace), plotly to display said data
    For each bin, masks will be created from the redshift limited files, NEED TO LOOK AT COMPUTER GENERATED FILE NAMES
    Because picking, procedure will need to be run several times - allows generation of errors easily
    This function should be able to find statistical results aswell so rerunning is easier.

    INPUTS - 
        Files containing data for AGN and Non-Agn Samples

    OUTPUTS - 
        Files - files containing the full set of data for points within a bin

    NOTES - 

    '''


    with fits.open('/Users/Owner/Documents/Coding/AGNLim') as hdu:
        data_agn = hdu[1].data
        mass_AGN = data_agn.field('mass_best')
        zpdf_AGN = data_agn.field('zpdf') #Initialises agn data stores, takes data from fits table[1]

    with fits.open('Test data set') as hdu:
        data_gal = hdu[1].data
        mass = data_gal.field('mass_best')
        zpdf = data_gal.field('zpdf') #Initialises non-agn data stores

    zbins = bs.weight_dist(zpdf_AGN,zpdf, return_bins= True) #Retrieves bin limits from basic stats for x and y axis
    massbins = bs.weight_dist(mass_AGN,mass, return_bins= True) #Bin limits are stored in the 3rd part of the arrays

    #Producing histograms: WIll produce 2, one for each set
    #Subsequent loop will sort through the bins for each histogram (which will be the same) and compare the amounts
    #Histogram with lowest count will be the one to match to, mask will be created with limits at the bin values
    #numpy function to randomly choose points???

    zbins = zbins[2]
    massbins = massbins[2]

    AGNHist = np.histogram2d(zpdf_AGN, mass_AGN, [zbins,massbins])
    AGNbox = AGNHist[0]
    AGN_bins_x = AGNHist[1]
    AGN_bins_y = AGNHist[2]
    nonAGNHist = np.histogram2d(zpdf,mass, [zbins,massbins])
    nonAGNbox = nonAGNHist[0]
    nonAGN_bins_x = nonAGNHist[1]
    nonAGN_bins_y = nonAGNHist[2]

    #Come across an issue with the set size/bin amount
    #auto binning with basic_stats generates 62 bins, far more than is neccessary for agn data since theres only 310 points
    #Might be worth doing linspace with a bin count of 15-20 but I suppose this will just get more specific results

    '''i_ = 0
    Tablemade = False
    xindex = 0

    for i_x in AGNbox:

        xindex_plus1 = xindex +1
        yindex=0

        for i_y in i_x:

            
            yindex_plus1 = yindex + 1

            mask1 = data_gal['zpdf'] >= nonAGN_bins_x[xindex]
            interim1 = data_gal[mask1]
            mask1 = interim1['zpdf'] <= nonAGN_bins_x[xindex_plus1] # narrows pop down to the bin range
            interim1 = interim1[mask1]
            mask1 = interim1['mass_best'] >= nonAGN_bins_y[yindex]
            interim1 = interim1[mask1]
            mask1 = interim1['mass_best'] <= nonAGN_bins_y[yindex_plus1]
            interim1 = interim1[mask1]

            mask2 = data_agn['zpdf'] >= AGN_bins_x[xindex]
            interim2 = data_agn[mask2]
            mask2 = interim2['zpdf'] <= AGN_bins_x[xindex_plus1] # narrows pop down to the bin range
            interim2 = interim2[mask2]
            mask2 = interim2['mass_best'] >= AGN_bins_y[yindex]
            interim2 = interim2[mask2]
            mask2 = interim2['mass_best'] <= AGN_bins_y[yindex_plus1]
            interim2 = interim2[mask2]

            print(xindex ,',',yindex)

            NApopulation = fits.BinTableHDU(data=interim1)
            Apopulation = fits.BinTableHDU(data=interim2) # Creates new hdu tables with the restricted data

            try: 
                NArows = NApopulation._nrows
            except:
                NArows = 0
            try:
                Arows = Apopulation._nrows
            except:
                Arows = 0

            if AGNbox[xindex,yindex] == 0:
                print('Skipped',AGNbox[xindex,yindex],'at', xindex,',', yindex)

                NArows = 0

            elif AGNbox[xindex,yindex] < nonAGNbox[xindex,yindex]:
                #create mask of data within bin values (i,i+1)
                # sample a random point from mask using np.random however many times needed to be equal to agn
                # append to a matched data table - save to file
                print('AGN less than nonAGN at',xindex,',',yindex)

                diff = int(nonAGNbox[xindex,yindex] - AGNbox[xindex,yindex]) # Finds difference in samples for the box

                if Tablemade == False:
                    Master = interim2
                    print('Table made!', Master)
                    Tablemade == True

                else:
                    Master = np.append(Master,interim2)

                for i in range(diff):

                    randsample = np.random.randint(0,NArows+1)
                    sample = NApopulation[randsample]

                    if Tablemade == False:
                        Master = sample
                        Tablemade = True
                    else:
                        Master = np.append(Master,sample)


            elif AGNbox[xindex,yindex] > nonAGNbox[xindex,yindex]:
                # create mask with bin values
                # take a sample
                # append to table
                print('AGN more than nonAGN at',xindex,',',yindex)

                diff = AGNbox[xindex,yindex] - nonAGNbox[xindex,yindex] # Finds difference in samples for the box

                if Tablemade == False:
                    Master = interim1
                    Tablemade == True

                else:
                    Master = np.append(Master,interim1)

                for i in range(diff):
                    randsample = np.random.randint(0,Arows+1)
                    sample = Apopulation[randsample]

                    if Tablemade == False:
                        Master = sample
                        print('Table made!', Master)
                        Tablemade = True
                    else:
                        Master = np.append(Master,sample)

            elif AGNbox[xindex,yindex] == nonAGNbox[xindex,yindex]:
                # create mask with bin values
                # take a sample
                # append to table  
                # # appends agn mask for the box to the file
                print('AGN same as nonAGN at',xindex,',',yindex)

                # appends agn mask for the box to the file
                interim1 = np.append(interim1,interim2)

                if Tablemade == False:
                    Master = interim1
                    print('Table made!', Master)
                    Tablemade = True

                else:
                    Master = np.append(Master, interim1)

            yindex += 1


        xindex += 1   

    print(Master)
    print(Master._nrows)
    '''           

            
    #new method
    x=0
    for i_x in AGNbox:
        y=0
        for i_y in i_x: #loops through the histogram to get x and y coords

            NAGNamount = nonAGNbox[x,y]

            if i_y == 0:
                print('skipped 0 value at',x,',',y)
                y+=1

            else:
                if i_y > NAGNamount:
                    AXlower = AGN_bins_x[x]
                    AXupper = AGN_bins_x[x+1]
                    AYlower = AGN_bins_y[y]
                    AYupper = AGN_bins_y[y+1]

                    mask1 = data_agn['zpdf'] >= AXlower
                    interim = data_agn[mask1]
                    mask1 = interim['zpdf'] <= AXupper
                    interim = interim[mask1]
                    mask1 = interim['mass_best'] >= AYlower
                    interim = interim[mask1]
                    mask1 = interim['mass_best'] <= AYupper
                    AGN_quantity = interim[mask1]

                    NXlower = nonAGN_bins_x[x]
                    NXupper = nonAGN_bins_x[x+1]
                    NYlower = nonAGN_bins_y[y]
                    NYupper = nonAGN_bins_y[y+1]

                    mask2 = data_agn['zpdf'] >= NXlower
                    interim = data_agn[mask2]
                    mask2 = interim['zpdf'] <= NXupper
                    interim = interim[mask2]
                    mask2 = interim['mass_best'] >= NYlower
                    interim = interim[mask2]
                    mask2 = interim['mass_best'] <= NYupper
                    gal_quantity = interim[mask2]

                elif i_y < NAGNamount:
                    print('less agns!')

                else:
                    print('things are equal')




matchsets()



    



