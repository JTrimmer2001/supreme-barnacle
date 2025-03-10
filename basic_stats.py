import sys, os
import numpy as np
import scipy.stats.distributions as dist
from scipy import special
import pandas



# (Cameron 2011)
# given subpop count k (e.g. n_spirals), sample size n (e.g. n_all), confidence level c (e.g. 0.68 or 0.95), the basic code is:
#p_lower = dist.beta.ppf((1-c)/2.,  k+1,n-k+1)
#p_upper = dist.beta.ppf(1-(1-c)/2.,k+1,n-k+1)
def p_lower(c, n, k):
    return dist.beta.ppf((1-c)/2.,  k+1,n-k+1)

def p_upper(c, n, k):
    return dist.beta.ppf(1-(1-c)/2.,k+1,n-k+1)

def get_errors_on_fractions(subpophist, allpophist, n_random=10000):
    # compute uncertainties using bayesian binomial confidence intervals
    # let's compute this for both 1 sigma and 2 sigma, so both 0.68 and 0.95
    subfrac_upper_1sig = subpophist * 0.0
    subfrac_lower_1sig = subpophist * 0.0
    subfrac_upper_2sig = subpophist * 0.0
    subfrac_lower_2sig = subpophist * 0.0
    c1 = 0.68
    c2 = 0.95

    if n_random > 0:
        subfrac_dists = np.zeros((len(subpophist), n_random))
    else:
        subfrac_dists = []

    for i, allcount in enumerate(allpophist):
        subcount = subpophist[i]
        subfrac_lower_1sig[i] = dist.beta.ppf((1-c1)/2.,   subcount+1, allcount-subcount+1)
        subfrac_upper_1sig[i] = dist.beta.ppf(1-(1-c1)/2., subcount+1, allcount-subcount+1)
        subfrac_lower_2sig[i] = dist.beta.ppf((1-c2)/2.,   subcount+1, allcount-subcount+1)
        subfrac_upper_2sig[i] = dist.beta.ppf(1-(1-c2)/2., subcount+1, allcount-subcount+1)

        if n_random > 0:
            # randomly populate the full beta function so we can do better errors later
            subfrac_dists[i] = np.random.beta(subcount+1, allcount-subcount+1, n_random)

    return subfrac_dists, subfrac_lower_1sig, subfrac_upper_1sig, subfrac_lower_2sig, subfrac_upper_2sig



def weight_dist(arr1, arr2, bins=None, return_bins=True, renorm=False):
    # note the bins need to be the same for both datasets
    # so either supply 1 number or 1 array of bin edges
    # also if you have fully specified the bins you don't need them returned
    # but if we've had to figure them out, you do need them returned
    # if you want to make sure you aren't under-weighting (e.g. if a whole dataset is
    # much larger than the other so you might always be able select >1 object
    # in dataset 1 for each object in dataset 2) then you can re-normalise to make
    # sure the max weight of both datasets is 1
    # Note, if the distributions cross this won't make a difference

    # weight arrays
    w1 = np.zeros_like(arr1)
    w2 = np.zeros_like(arr2)

    # if bins not specified, guess at them ourselves
    if bins is None:
        minsize = np.amin([    len(arr1),     len(arr2)])
        themin  = np.amin([np.nanmin(arr1), np.nanmin(arr2)])
        themax  = np.amax([np.nanmax(arr1), np.nanmax(arr2)])

        # on average 5 data points per bin, but at least 3 bins pls, max value is last bin edge
        bins = np.linspace(themin, themax, int(np.amax([(minsize/5)+1, 3])), endpoint=True)

    else:
        pass
        # because the np.histogram function can deal with distinguishing between number of bins or specific bins itself
        # so we don't have to

    hist1, thebins = np.histogram(arr1, bins=bins)  # returns (counts_arr, bins_arr)
    # use the bins from hist1 to make hist2
    # note: for these purposes, any values of hist2 outside the minmax range of hist1 should have 0 weight
    # which is taken care of by the zeros_like initialisation of w1 and w2 above
    # so it's fine for them to be excluded below
    hist2, thebins = np.histogram(arr2, bins=thebins)

    # now step through the bins and assign weights
    for i_bin in range(len(thebins)-1):
        # zero-"index"ing these because they're indices and not values
        # and if I get them mixed up below I want this to error that there's no b2 or whatever
        b0 = thebins[i_bin]
        b1 = thebins[i_bin+1]

        count1 = hist1[i_bin]
        count2 = hist2[i_bin]

        # don't miss any values and don't double-count
        if i_bin == 0:
            in_bin1 = (arr1 >= b0) & (arr1 <= b1)
            in_bin2 = (arr2 >= b0) & (arr2 <= b1)
        else: 
            in_bin1 = (arr1 >  b0) & (arr1 <= b1)
            in_bin2 = (arr2 >  b0) & (arr2 <= b1)


        # don't divide by 0 in the rest of the if/else
        if (count1 == 0) | (count2 == 0):
            w1[in_bin1] = 0.0
            w2[in_bin2] = 0.0

        elif count1 < count2:
            # weight count2 values so the sum of wt2 in this bin equals count1
            # wt_fac will always be < 1
            wt_fac = float(count1)/float(count2)
            w1[in_bin1] = 1.0
            w2[in_bin2] = wt_fac

        else:
            # weight count1 values so the sum of wt1 in this bin equals count2
            # wt_fac will always be <= 1
            wt_fac = float(count2)/float(count1)
            w1[in_bin1] = wt_fac
            w2[in_bin2] = 1.0


    # now the weights should be determined
    # we can optionally re-normalise to make sure we are getting max value out of the datasets
    if renorm:
        if (np.sum(w1) > 0.00000) & (np.amax(w1) < 1.0):
            w1 /= np.amax(w1)

        if (np.sum(w2) > 0.00000) & (np.amax(w2) < 1.0):
            w2 /= np.amax(w2)


    if return_bins:
        return w1, w2, thebins 
    else: 
        return w1, w2




def prob_dist_overlap(arr1, arr2, getsigma=False):

    # provides weights needed such that weighted histograms of arr1 and arr2 are statistically indistinguishable
    # which, in practice, is the overlap of the distributions
    w1, w2, thebins = weight_dist(arr1, arr2, renorm=True)

    # technically we don't want to double count the overlap area in either numerator or denominator
    # but if your statistics depend on quibbling about this, your significance is marginal at best
    # so report that and don't overegg the results
    overlap_area = 0.5*(np.sum(w1) + np.sum(w2))
    total_area = float(len(arr1) + len(arr2)) - np.sum(w1)

    f_overlap = overlap_area / total_area

    if getsigma:
        # the special.erfc(x) is the complementary error function, where x = sigma/sqrt(2)
        # i.e. the table of p-value-to-sigma at https://en.wikipedia.org/wiki/Normal_distribution#Standard_deviation_and_tolerance_intervals is actually a table of erf(x), erfc(x), 1./erfc(x) for sigma values from 1 to 6
        # and special.erfcinv(alpha)*np.sqrt(2.) will return the significance level in sigma.
        # however, WARNING - this sigma is only valid assuming the distributions are normal
        # which a lot of this utils file assumes they aren't.
        # so use as guidance but not gospel, and very much with caution.
        sigma_overlap = special.erfcinv(f_overlap)*np.sqrt(2.)
        return f_overlap, sigma_overlap
    else:
        return f_overlap





# hmm, pretty sure this is crap - it only figures out what fraction of values are overlapping,
# not e.g. the area of intersection between the 2 KDEs of the 2 distributions
def prob_dist_overlap_old(dist1, dist2, getsigma=False):

    # figure out which one is higher
    if np.mean(dist1) >= np.mean(dist2):
        dist_hi = dist1
        dist_lo = dist2
    else:
        dist_hi = dist2
        dist_lo = dist1

    # how many times does the upper end of the low distribution overlap the lower end of the high distribution?
    overlap_lo = sum(dist_lo >= np.min(dist_hi))
    # print("Low overlap: %d" % overlap_lo)
    # now flip it - check overlap of high dist into upper parts of low dist
    overlap_hi = sum(dist_hi <= np.max(dist_lo))
    # print("high overlap: %d" % overlap_hi)

    # print("total samples: %d" % len(dist_lo) + len(dist_hi))

    # total fraction of points that overlap
    f_overlap = float(overlap_lo + overlap_hi)/float(len(dist_lo) + len(dist_hi))

    if getsigma:
        # the special.erfc(x) is the complementary error function, where x = sigma/sqrt(2)
        # i.e. the table of p-value-to-sigma at https://en.wikipedia.org/wiki/Normal_distribution#Standard_deviation_and_tolerance_intervals is actually a table of erf(x), erfc(x), 1./erfc(x) for sigma values from 1 to 6
        # and special.erfcinv(alpha)*np.sqrt(2.) will return the significance level in sigma.
        # however, WARNING - this sigma is only valid assuming the distributions are normal
        # which a lot of this utils file assumes they aren't.
        # so use as guidance but not gospel, and very much with caution.
        sigma_overlap = special.erfcinv(f_overlap)*np.sqrt(2.)
        return f_overlap, sigma_overlap
    else:
        return f_overlap


# what to do if there's loads of zero-weighted stuff in here? think we have to remove those
# 
# x == rank
# p == pctile_val
# N == dimension of array
# the method numpy uses for straight percentile:
# x = p(N-1) + 1
# then linearly interpolate... 
# we have to do something similar except with weights
# there's an extension for weighted percentiles in wikipedia
# https://en.wikipedia.org/wiki/Percentile#Weighted_percentile
# I have tested it for various things and it seems to work fine

def percentile_wt(sample, weights, pct, verbose=False):

    sample  = np.array(sample)
    weights = np.array(weights)

    if not ((pct >= 0.0) & (pct <= 100.0)):
        print("Percentile requested must be between 0 and 100")
        return np.nan 
    else:
        pass


    count_this = float(np.sum(weights))
    if count_this <= 0.0:
        print("Sum of weights is 0 or negative, something has gone very wrong")
        return np.nan

    else:
        zero_weights = weights <= 0.0
        if (sum(zero_weights) > 0) & verbose:
            print("Removing zero-weight points before computing")
        ssample = sample[np.invert(zero_weights)].copy()
        wweights = weights[np.invert(zero_weights)].copy()
        j_sorted = ssample.argsort()
        sample_sort = ssample[j_sorted]
        weight_sort = weights[j_sorted]
        _c = np.cumsum(weight_sort)

        p_rank = _c/float(_c[-1])

        x = pct/100.*(sum(weight_sort)-1) + 1.

        x_n = x/_c[-1]

        # searchsorted returns the index immediately *before* which you'd insert a 
        # new value to maintain the order
        j_which = np.searchsorted(_c, x, side='left') - 1

        if j_which < 0:
            return sample_sort[0]
        else:

            #print(j_which, "==========")
            #print("_c", _c, "x", x, "x_n", x_n, "p_rank", p_rank, "sample", sample)
            if j_which == len(sample_sort)-1:
                if verbose:
                    print("Returning highest value (index %d)" % j_which)

                return sample_sort[j_which]
            else:        
                return sample_sort[j_which] + ((x_n-p_rank[j_which])/(p_rank[j_which+1]-p_rank[j_which]))*(sample_sort[j_which+1]-sample_sort[j_which])


        # # linearly interpolate
        # cdist_tot   = rank[j_which+1] - rank[j_which]
        # cdist_left  = pct - rank[j_which]
        # cdist_right = rank[j_which+1] - pct

        # # whichever has the shortest distance gets the largest weight, so swap left & right distances
        # return (cdist_right/cdist_tot)*sample_sort[j_which] + (cdist_left/cdist_tot)*sample_sort[j_which+1]




def get_stats_indices():

    n_val_basicstats = 13
    i_mean   = 0
    i_median = 1
    i_count  = 2
    i_16p    = 3
    i_25p    = 4
    i_75p    = 5
    i_84p    = 6
    i_var    = 7
    i_varmed = 8
    i_05p    = 9  #0.5th pctile
    i_5p     = 10
    i_95p    = 11
    i_995p   = 12 # 99.5th pctile

    i_stats = {'mean':    0,
               'median':  1,
               'count':   2,
               '16p':     3,
               '25p':     4,
               '75p':     5,
               '84p':     6,
               'var':     7,
               'varmed':  8,
               '05p':     9,
               '5p':     10,
               '95p':    11,
               '995p':   12
               }

    return n_val_basicstats, i_mean, i_median, i_count, i_16p, i_25p, i_75p, i_84p, i_var, i_varmed, i_05p, i_5p, i_95p, i_995p, i_stats






def get_basic_stats(sample, weights=None, verbose=False):

    n_val_basicstats, i_mean, i_median, i_count, i_16p, i_25p, i_75p, i_84p, i_var, i_varmed, i_05p, i_5p, i_95p, i_995p, i_stats = get_stats_indices()

    basic_stats = np.zeros(n_val_basicstats)

    if weights is None:
        themedian  = np.median(sample)
        count_this = len(sample)

        basic_stats[i_count] = count_this

        if count_this > 0:
            basic_stats[i_mean] = np.mean(sample)
            basic_stats[i_median] = themedian
            if count_this > 2:
                basic_stats[i_05p]  = np.percentile(sample, 0.5)
                basic_stats[i_5p]   = np.percentile(sample, 5)
                basic_stats[i_16p]  = np.percentile(sample, 16)
                basic_stats[i_25p]  = np.percentile(sample, 25)
                basic_stats[i_75p]  = np.percentile(sample, 75)
                basic_stats[i_84p]  = np.percentile(sample, 84)
                basic_stats[i_95p]  = np.percentile(sample, 95)
                basic_stats[i_995p] = np.percentile(sample, 99.5)
                basic_stats[i_var] = np.var(sample)

            # try to estimate the variance on the median, which isn't built into numpy
            # https://en.wikipedia.org/wiki/Median#The_sample_median
            # we will use the asymptotic approximation, which will tend to overestimate
            #    the variance, especially when the sample size is small
            # these seem really small when plotted though
            if count_this > 10:
                # we want at least 4 gals per bin on average
                this_nbins = int(min((count_this / 4, 12)))
                # we need to get the PDF for this bin and get the value of it at the median
                sample_hist = np.histogram(sample, bins=this_nbins, density=True)
                # identify all bins with x values <= the median, then take the last one
                medbins = sample_hist[0][sample_hist[1][:-1] <= themedian]
                pdf_at_median = medbins[-1]

            else:
                # not really sure what to do here b/c we don't really know the distribution
                #pdf_at_median = 0.5
                # this goes from 0.4 at n=1 to 0.6 at n=10, but it's kind of arbitrary
                # just trying to characterize doing better at the median with more points
                pdf_at_median = (1./30.)*float(count_this - 1) + 0.4

            basic_stats[i_varmed] = 1./(4.*float(count_this)*pdf_at_median**2)


        return basic_stats

    else: 
        # there are weights, we need to use them to compute everything
        count_this = float(np.sum(weights))
        basic_stats[i_count] = count_this

        # some things are built into numpy, others not so much

        if count_this > 0:

            basic_stats[i_mean] = avg = np.average(sample, weights=weights)
            basic_stats[i_var]  = np.sqrt(np.average((sample-avg)**2, weights=weights))
    
            if len(sample[weights >= 0.0] > 2):
                basic_stats[i_05p]  = percentile_wt(sample, weights, 0.5, verbose=verbose)
                basic_stats[i_5p]   = percentile_wt(sample, weights, 5, verbose=verbose)
                basic_stats[i_16p]  = percentile_wt(sample, weights, 16, verbose=verbose)
                basic_stats[i_25p]  = percentile_wt(sample, weights, 25, verbose=verbose)
                basic_stats[i_median]  = themedian = percentile_wt(sample, weights, 50, verbose=verbose)
                basic_stats[i_75p]  = percentile_wt(sample, weights, 75, verbose=verbose)
                basic_stats[i_84p]  = percentile_wt(sample, weights, 84, verbose=verbose)
                basic_stats[i_95p]  = percentile_wt(sample, weights, 95, verbose=verbose)
                basic_stats[i_995p] = percentile_wt(sample, weights, 99.5, verbose=verbose)
 

            # try to estimate the variance on the median, which isn't built into numpy
            # https://en.wikipedia.org/wiki/Median#The_sample_median
            # we will use the asymptotic approximation, which will tend to overestimate
            #    the variance, especially when the sample size is small
            # these seem really small when plotted though
            if len(sample[weights >= 0.0]) > 10:
                # we want at least 4 gals per bin on average
                this_nbins = int(min((len(sample[weights >= 0.0]) / 4, 12)))
                # we need to get the PDF for this bin and get the value of it at the median
                sample_hist = np.histogram(sample, bins=this_nbins, density=True, weights=weights)
                # identify all bins with x values <= the median, then take the last one
                medbins = sample_hist[0][sample_hist[1][:-1] <= themedian]
                pdf_at_median = medbins[-1]

            else:
                # not really sure what to do here b/c we don't really know the distribution
                #pdf_at_median = 0.5
                # this goes from 0.4 at n=1 to 0.6 at n=10, but it's kind of arbitrary
                # just trying to characterize doing better at the median with more points
                pdf_at_median = (1./30.)*float(len(sample[weights >= 0.0]) - 1) + 0.4

            basic_stats[i_varmed] = 1./(4.*float(len(sample[weights >= 0.0]))*pdf_at_median**2)


        return basic_stats





# binning in 1D - uses functions above
# usually you want to bin a bunch of things (like stellar mass, BH mass, SFR, X-ray luminosity, etc)
# according to a different quantity (like redshift)
# so in that case you'd call
# bin_array(redshift, redshift_bin_boundaries, list_of_other_arrays=[stellar_mass, bh_mass, SFR, Xray_lum, etc])
# but if you just want to get stats and bin 1 array, then go for it, the list (and weight array) is optional
def bin_array(the_array, the_bin_boundaries, list_of_other_arrays=None, weights=None):

    # in case the function was passed a list or tuple instead of an array
    # if it's already an array this won't do anything
    the_array = np.array(the_array)

    # some built-in indices we will find it useful to have
    n_val_basicstats, i_mean, i_median, i_count, i_16p, i_25p, i_75p, i_84p, i_var, i_varmed, i_05p, i_5p, i_95p, i_995p, i_stats = get_stats_indices()

    # there are 1 fewer bins than bin boundaries, so get arrays corresponding to the left
    # and right edges of each bin, and the centers, which have the correct dimensions
    bins_lo  = np.array(the_bin_boundaries[:-1])
    bins_hi  = np.array(the_bin_boundaries[1:])
    bins_ctr = 0.5*(bins_lo + bins_hi)

    # define the arrays/lists we need
    array_binned = []
    stats_t      = []
    if list_of_other_arrays is not None:
        array_binned_list_t_v = []
        array_binned_list_t   = []
        array_binned_list     = []
        stats_list_t_v        = []
        stats_list_t          = []
    else:
        array_binned_list = None
        stats_list_t      = None


    # sort values into each bin
    for _i in range(len(bins_lo)):
        # pick out values from the array that are in this bin

        # if it's the last bin, it's ok if the value equals the bin limit
        # otherwise one test should be "or equals" and the other not, to
        # prevent double-counting
        if (_i == (len(bins_lo)-1)):
            in_bin = (the_array >= bins_lo[_i]) & (the_array <= bins_hi[_i])
        else:
            in_bin = (the_array >= bins_lo[_i]) & (the_array < bins_hi[_i])

        # set a subarray
        a_bin = the_array[in_bin]

        # save the individual sub-arrays in a list, which we may need later
        array_binned.append(a_bin)

        # get stats
        a_stats = get_basic_stats(a_bin, weights=weights)
        # save stats for each bin to a list (we'll rearrange this later)
        stats_t.append(a_stats)

        # now do the same on every array in the list of arrays, if there is one
        if list_of_other_arrays is not None:
            array_binned_list_t_v = []
            # stats_list_t_v        = []
            for _v, vals in enumerate(list_of_other_arrays):
                vals_arr = np.array(vals)
                vals_bin = vals_arr[in_bin]

                array_binned_list_t_v.append(vals_bin)

                v_stats = get_basic_stats(vals_bin, weights=weights)

                stats_list_t_v.append(v_stats)

            # this is a list of lists, bit gross but we'll sort it out later
            array_binned_list_t.append(array_binned_list_t_v)
            stats_list_t.append(stats_list_t_v)




    # right now if we wanted e.g. the median values for each bin we'd need to get them with
    # stats_t[0][i_median], stats_t[1][i_median], etc.
    # when we'd like to have stats[i_median] contain an array with all the bins
    # i.e., we need the transpose.

    the_stats = np.array(stats_t).T 


    # do the same on every array in the list of arrays, if there is one
    if list_of_other_arrays is not None:
        array_binned_list = np.array(array_binned_list_t).T

        the_stats_list = []
        for _v, vals in enumerate(list_of_other_arrays):
            # we need to create a list analogous to the_stats that corresponds to 
            # the original list that was input
            the_stats_list.append(np.array(stats_list_t[_v]).T)
    else:
        the_stats_list = None

    # ok, send both the list of binned array values and the stats for each bin back
    return array_binned, the_stats, array_binned_list, the_stats_list





