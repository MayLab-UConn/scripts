import matplotlib.pyplot as plt
import numpy as np

'''
    This script makes a 3-panel plot of some sample data, and is hopefully fully annotated so that every instruction
    is put in context.
'''

# sample data for plotting - for example purposes
panelA_xdata = np.arange(10)
panelA_ydata = panelA_xdata ** 2
panelB_xdata = np.arange(50)
panelB_ydata = np.ones(50) * 10 + (np.random.rand(50) - 0.5) * 3
panelC_xdata = np.arange(20)
panelC_ydata = panelC_xdata + (np.random.rand(20) - 0.5) * 4
panelC_error = 3 * np.random.rand(20)


# You can set default font sizes for the different aspects of the plot with rc. This way you don't have to specify
# a fontsize for each piece of text, and changing these values will change the whole plot. HOWEVER, you can still
# manually select a font size for any specific label as per usual - it will override the default options!
plt.rc('font',  size=8)
plt.rc('axes',  titlesize=12)
plt.rc('axes',  labelsize=12)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

# pyplot as a "figure" object, which is basically the frame. For simple plots, you can directly plot to it using
# eg plt.plot, plt.scatter. For more complicated things such as a multipanel figure, you'll be plotting using axis
# handles - here I've labeled them ax_A, ax_B, and ax_C for panels A, B, and C.

fig, (ax_A, ax_B, ax_C) = plt.subplots(1, 3 , figsize=(11, 3))
# subplots (1,3) indicates that we'll have one row, 3 columns - hence 3 axes objects
# figsize is in inches, across by down. You may want to play around with this to get a desirable aspect ratio

# -------------------------------------------------------------------------------------------------------------------
# panel A
# -------------------------------------------------------------------------------------------------------------------


ax_A.plot(panelA_xdata, panelA_ydata, 'ro-', label='sample A')             # axis plot is similar in syntax to plt.plot
ax_A.set_xlim(-.05, 11)                                                    # equivalent to plt.xlim()
ax_A.set_ylim(0, 11)                                                       # equivalent to plt.ylim()
ax_A.set_xlabel('some data (nm)')                                          # equivalent to plt.xlabel()
ax_A.set_ylabel('polynomial')                                              # equivalent to plt.ylabel()
ax_A.set_xticks((3, 6, 9))                                                 # equivalent to plt.xticks()
ax_A.set_yticks((20, 40, 60, 80, 100))                                     # equivalent to plt.yticks()
ax_A.legend(loc=2)                                                         # uses labels from plot - location can be decided by you using loc

# these two commands are to set the rightand top boundaries invisible - if desired. You may want the full box, but
ax_A.spines['right'].set_visible(False)
ax_A.spines['top'].set_visible(False)

# This sets the panel A label in the top right corner. The first two numbers are the relative position of the text.
# So setting them to 0, 0, would put the text exactly at the bottom left of the panel. Setting x to -.25 puts the
# text to the LEFT of the panel, and y=1.05 sets it to the top, slightly above the figure. You may have to play around
# with the actual values - depending on the size of the y label, you might need to push it up, down, left, or right
# for a pretty alignment. Also be careful - if the labels are too far away from the figure, they might be cut off. You
# can expand the figure using the pad option of the tight_layout() command - see the end of this script

# The A is the actual text, fontsize is up to you. I'm not sure about the transform option, but it works so don't touch
# it unless you know what you're doing
ax_A.text(-0.25, 1.05, 'A', fontsize=16, transform=ax_A.transAxes)
# -------------------------------------------------------------------------------------------------------------------
# panel B
# -------------------------------------------------------------------------------------------------------------------

ax_B.plot(panelB_xdata, panelB_ydata, 'k-', label='some legend thing')
ax_B.set_xlim(-1, 51)
ax_B.set_ylim(5, 15)
ax_B.set_xlabel('data points')
ax_B.set_ylabel('random noise')
ax_B.set_xticks((10, 20, 30, 40, 50))
ax_B.set_yticks((8, 10, 12))
ax_B.legend(loc=2)
ax_B.spines['right'].set_visible(False)
ax_B.spines['top'].set_visible(False)
ax_B.text(-0.25, 1.05, 'B', fontsize=16, transform=ax_B.transAxes)

# -------------------------------------------------------------------------------------------------------------------
# panel C
# -------------------------------------------------------------------------------------------------------------------

ax_C.errorbar(panelC_xdata, panelC_ydata, yerr=panelC_error, fmt='bo', capsize=5, ecolor='k', label='C legend')
ax_C.set_xlim(-4, 24)
ax_C.set_ylim(-4, 24)
ax_C.set_xlabel('time')
ax_C.set_ylabel('data with errors')
ax_C.set_xticks((0, 5, 10, 15, 20))
ax_C.set_yticks((0, 5, 10, 15, 20))
ax_C.legend(loc=2)
ax_C.spines['right'].set_visible(False)
ax_C.spines['top'].set_visible(False)
ax_C.text(-0.25, 1.05, 'C', fontsize=16, transform=ax_C.transAxes)


# fig.tight_layout is typically the command you want. I'm not 100% sure about how pyplot works without it. The pad
# option is necessary if you have things out of the axes (like we do with out ABC labels) - you might need to play
# around with the pad size to include all your labels. You can also do h_pad and w_pad, separatel but regular pad works
# fine for me
fig.tight_layout(pad=2)

fig.savefig('sample.png')
