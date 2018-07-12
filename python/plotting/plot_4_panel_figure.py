import matplotlib.pyplot as plt
import numpy as np

'''
    This script makes a 4-panel plot of some sample data. Almost the same as making a 3 panel plot, but pay attention to
     the subplots command and the way the axes are accessed. I've taken out a bunch of the comments from the 3 panel
     figure, so if you see a command you don't understand, it might be documented in the "plot_3_panel_figure" file
'''

# sample data for plotting - for example purposes
panelA_xdata = np.arange(10)
panelA_ydata = panelA_xdata ** 2
panelB_xdata = np.arange(50)
panelB_ydata = np.ones(50) * 10 + (np.random.rand(50) - 0.5) * 3
panelC_xdata = np.arange(20)
panelC_ydata = panelC_xdata + (np.random.rand(20) - 0.5) * 4
panelC_error = 3 * np.random.rand(20)
panelD_xdata, panelD_ydata  = np.random.rand(20), np.random.rand(20)

# default font sizes
plt.rc('font',  size=8)
plt.rc('axes',  titlesize=12)
plt.rc('axes',  labelsize=12)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

# In the 3 panel plot, we expanded the axis object into 3 axes object variables. Here, we'll keep them as an array, so
# ax_array is actually a 2 x 2 matrix of axis objects, so panels A, B, C, and D are accessed through [0, 0], [0, 1],
# [1, 0], and [1, 1] for top-left, top-right, bot-left, and bot-right

fig, ax_array = plt.subplots(2, 2 , figsize=(11, 7))
# subplots (2, 2) indicates that we'll have 2 rows, 2 columns
# figsize is in inches, across by down. You may want to play around with this to get a desirable aspect ratio

# -------------------------------------------------------------------------------------------------------------------
# panel A
# -------------------------------------------------------------------------------------------------------------------

ax_array[0, 0].plot(panelA_xdata, panelA_ydata, 'ro-', label='sample A')
ax_array[0, 0].set_xlim(-.05, 11)
ax_array[0, 0].set_ylim(0, 11)
ax_array[0, 0].set_xlabel('some data (nm)')
ax_array[0, 0].set_ylabel('polynomial')
ax_array[0, 0].set_xticks((3, 6, 9))
ax_array[0, 0].set_yticks((20, 40, 60, 80, 100))
ax_array[0, 0].legend(loc=2)
ax_array[0, 0].spines['right'].set_visible(False)
ax_array[0, 0].spines['top'].set_visible(False)
ax_array[0, 0].text(-0.1, 1.05, 'A', fontsize=16, transform=ax_array[0, 0].transAxes)
# -------------------------------------------------------------------------------------------------------------------
# panel B
# -------------------------------------------------------------------------------------------------------------------

ax_array[0, 1].plot(panelB_xdata, panelB_ydata, 'k-', label='some legend thing')
ax_array[0, 1].set_xlim(-1, 51)
ax_array[0, 1].set_ylim(5, 15)
ax_array[0, 1].set_xlabel('data points')
ax_array[0, 1].set_ylabel('random noise')
ax_array[0, 1].set_xticks((10, 20, 30, 40, 50))
ax_array[0, 1].set_yticks((8, 10, 12))
ax_array[0, 1].legend(loc=2)
ax_array[0, 1].spines['right'].set_visible(False)
ax_array[0, 1].spines['top'].set_visible(False)
ax_array[0, 1].text(-0.1, 1.05, 'B', fontsize=16, transform=ax_array[0, 1].transAxes)

# -------------------------------------------------------------------------------------------------------------------
# panel C
# -------------------------------------------------------------------------------------------------------------------

ax_array[1, 0].errorbar(panelC_xdata, panelC_ydata, yerr=panelC_error, fmt='bo', capsize=5, ecolor='k', label='C legend')  # noqa
ax_array[1, 0].set_xlim(-4, 24)
ax_array[1, 0].set_ylim(-4, 24)
ax_array[1, 0].set_xlabel('time')
ax_array[1, 0].set_ylabel('data with errors')
ax_array[1, 0].set_xticks((0, 5, 10, 15, 20))
ax_array[1, 0].set_yticks((0, 5, 10, 15, 20))
ax_array[1, 0].legend(loc=2)
ax_array[1, 0].spines['right'].set_visible(False)
ax_array[1, 0].spines['top'].set_visible(False)
ax_array[1, 0].text(-0.1, 1.05, 'C', fontsize=16, transform=ax_array[1, 0].transAxes)

# -------------------------------------------------------------------------------------------------------------------
# panel D
# -------------------------------------------------------------------------------------------------------------------
ax_array[1, 1].scatter(panelD_xdata, panelD_ydata, marker='*', c='g')
ax_array[1, 1].set_xlim(-.1, 1.1)
ax_array[1, 1].set_ylim(-.1, 1.1)
ax_array[1, 1].set_xlabel('x')
ax_array[1, 1].set_ylabel('y')
ax_array[1, 1].set_xticks((0, 0.5, 1))
ax_array[1, 1].set_yticks((0, 0.5, 1))
ax_array[1, 1].spines['right'].set_visible(False)
ax_array[1, 1].spines['top'].set_visible(False)
ax_array[1, 1].text(-0.1, 1.05, 'D', fontsize=16, transform=ax_array[1, 1].transAxes)


fig.tight_layout(pad=2.5)


plt.show()
# fig.savefig('sample_files/4_panel_figure/sample.png')
