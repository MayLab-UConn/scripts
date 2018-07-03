import numpy as np


def load_xvg(file, comments=('#', '@'), dims=3, return_time_data=False):
    ''' Loads an xvg file, created from gromacs. For a typical gromacs-derived xvg giving information on
        n particles with m dimensions to the data, the format is c1=time, c2 to c2 + m = data on first particle, and
        so on. Each row is a time point. Will throw out time point unless specified

        Parameters
            file             - path to xvg file
            comments         - comments to ignore from header. "#" and "@" typically handle it
            dims             - dimensions of data. Ie for every particle, how many pieces of information
            return_time_data - boolean. If true, returns a tuple of (data, time)
        Returns
            data             - nframes * nparticles * ndims
            times            - (optional) nframes array of times, same units as in xvg file
    '''

    data = np.loadtxt(file, dtype=float, comments=comments)
    if (data.shape[1] - 1) % dims > 0:
        raise ValueError("(dims * n_particles) + 1 does not equal number of columns in xvg")

    return_data = data[:, 1:].reshape(data.shape[0], int((data.shape[1] - 1) / dims), dims)
    if return_time_data:
        times = data[:, 0]
        return return_data, times
    else:
        return return_data
