import matplotlib.pyplot as plt
import matplotlib.image as im
import numpy as np

'''
    This script makes a 3-panel plot of some sample data, with panel A being a VMD image.

    Panels B and C are identical to the plot_3_panel_figure script, and I've stripped out the explanatory notes for
    those panels. The only new important stuff here is the panel A section, and we've also included the matplotlib.image
    module
'''

# sample data for plotting - for example purposes
panelB_xdata = np.arange(50)
panelB_ydata = np.ones(50) * 10 + (np.random.rand(50) - 0.5) * 3
panelC_xdata = np.arange(20)
panelC_ydata = panelC_xdata + (np.random.rand(20) - 0.5) * 4
panelC_error = 3 * np.random.rand(20)


plt.rc('font',  size=8)
plt.rc('axes',  titlesize=12)
plt.rc('axes',  labelsize=12)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)


fig, (ax_A, ax_B, ax_C) = plt.subplots(1, 3 , figsize=(11, 3))
# subplots (1,3) indicates that we'll have one row, 3 columns - hence 3 axes objects
# figsize is in inches, across by down. You may want to play around with this to get a desirable aspect ratio

# -------------------------------------------------------------------------------------------------------------------
# panel A
# -------------------------------------------------------------------------------------------------------------------

# Images are super easy to import using the matplotlib.image module
image = im.imread("sample_figure_for_embedding.png")
# Then, imshow is super easy to use for embedding the image in a plot. You can plt.imshow to embed it into the entire
# figure, or axis.imshow for one panel.
# The only complication here is the optional aspect argument. You can pass imshow aspect="auto", "equal", or a scalar.
# and it'll decide how to stretch the figure over the resulting space. Note that for some reason, some combinations of
# this can throw of the panel label, and you may have to adjust the x and y position of the axis.text() command
ax_A.imshow(image, aspect="equal")

# I typically don't like having axes on image panels, so this turns them off
ax_A.axis("off")
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


plt.show()
# fig.savefig('sample_files/3_panel_figure/sample.png')
