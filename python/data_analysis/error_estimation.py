import numpy as np
from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt

'''
    Utilities for automated checking of single dimensional data sets for error convergence.

    Block averaging is used to estimate error of a time course. At a long enough block length, blocks become
    decorrelated and can be used to estimate standard error. However, with insufficient sampling there may be too few
    blocks that are sufficiently independent to confidently estimate the error (as well as the actual value). Grossfield
    and co. suggest 20 independent "samples" is sufficient, I'd say 10 is still reasonable - it's not too far into the
    noise that you can't be confident your error has converged.
'''


def block_average(data, blocksize, partial_block_cutoff_size=0.5):
    '''
        Calculates the block average error estimate for a 1D data set given a set block size.

        Parameters -
            -data                 - 1D numpy array
            -blocksize            - integer, number of data points in a block
            -partial_block_cutoff - float between 0 and 1 (inclusive). Used to determine whether to include the final
                                    block, which is typically smaller than the others. If the fractional size of the
                                    last block with respect to the requested blocksize >= partial_block_cutoff, the
                                    block is included. Set to 0 to always discard partial blocks, set to 0 to always
                                    include

        Returns
            -block standard error (BSE) - Standard error of sample from block size. BSE = std(block means)/sqrt(nblocks)
    '''
    # determine if last block should be included
    data_size = data.size
    last_block_size = (data_size % blocksize)
    last_block_fraction_size =  last_block_size / data.size
    if last_block_size  < partial_block_cutoff_size and last_block_fraction_size > 0:  # mod  = 0 if perfect division
        data_size -= last_block_size  # if cutting off last block, just reduce arange size

    data_range = np.arange(0, data_size, blocksize)

    M = data_range.size    # number of blocks. This is determined AFTER deciding to keep last block or not
    means = np.zeros(M)
    for index, start in enumerate(data_range):
        means[index] = data[start:start + blocksize].mean()
    return np.std(means) / np.sqrt(M)


def block_average_range(data, block_range, partial_block_cutoff_size=0.5):
    '''
        Calculates standard errors from block averaging over a range of block sizes

        Parameters
            -data        - 1D numpy array of time-course data
            -block_range - 1D numpy array of block sizes to estimate SE for - must start at 1 or greater
            -partial_block_cutoff_size - treatment of last block - see description in block_average function

        Returns
            -block standard errors - 1D numpy array, size of block_range. SEs for each block size
    '''
    bse = np.zeros(block_range.size)
    for index, blocksize in enumerate(block_range):
        bse[index] = block_average(data, blocksize, partial_block_cutoff_size=partial_block_cutoff_size)
    return bse


def check_decorrelation(data, min_samples=10, corr_thresh=0):
    '''
        Takes a data set, figures out the maximum allowable blocksize (totalsize / 10, or whatever other criteria the
        user specifies), then see if the sample actually decorrelates in that time. The basic indicator of convergence
        is whether or not the block averaging profile flattens out in this regime, but it can be unclear on two fronts.
            First, with not enough data, one can convince themself that the curve has flattened within noise when really
        they have only 2 or 3 points in the data set at that block. Limiting the block average curve to block sizes that
        provide at least 10 blocks should stop that issue, and let you know if you are actually converged with that
        amount of data. So - if your curve is still rising at the end of this plot, you likely do not have enough data.
            Second, when one has data that is actually decorrelated from frame to frame (or within a few frames), the
        block average curve will not show it's typical asymptote. This should be a good thing, you've got great
        sampling! But without a clear curve how can you tell it's a decorrelated sample and not some analysis error?
        One check is to run an acf alongside the block average. If the acf shows a rapid (within a few frame taus)
        decrease to 0, you're golden.

        Parameters:
            data - 1D numpy array
            min_samples - data must have at LEAST this many samples in block averaging, sets upper bound on block size
                          as data.size / min_samples
            corr_thresh - for an acf, used to report when the acf falls BELOW this level for the first time. Indicates
                          that the sample is decorrelated at this time lag
    '''

    n_obs = data.size

    # round will help to clean up end of dataset issues. If halfway or more to another block, will add that block.
    # Otherwise will keep blocksize lower
    max_block_size = int(np.round(n_obs / min_samples))

    ba_data = block_average_range(data, np.arange(1, max_block_size))
    acf_data = acf(data, nlags=max_block_size)

    is_decorrelated = np.any(acf_data <= corr_thresh)

    if is_decorrelated:
        decorr_frame = np.argmax(acf_data < corr_thresh)
    else:
        decorr_frame = None

    f, axarr = plt.subplots(2, sharex=True)

    axarr[0].set_ylabel('BSE')
    axarr[0].plot(np.arange(1, ba_data.size + 1), ba_data)
    if is_decorrelated:
        axarr[0].plot([decorr_frame, decorr_frame], [ba_data.min(), ba_data.max()], 'k--')

    axarr[1].set_ylabel('ACF')
    axarr[1].set_xlabel('Block size (top) / tau (bot)')
    axarr[1].plot(np.arange(acf_data.size), acf_data)   # nlags + 1, with lag=0
    axarr[1].plot([0, max_block_size], [corr_thresh, corr_thresh])
    plt.show()
