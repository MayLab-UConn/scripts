import numpy as np
import matplotlib.pyplot as plt

'''
    Contains a bunch of tips and tricks for making publication-quality figures.
'''
# ----------------------------------------------------------------------------------------------------------------------
# matplotlib default values
# ----------------------------------------------------------------------------------------------------------------------

# matplotlib has default values for pretty much any parameter you can play with. To view these, take a look at
# plt.rcParams - it's basically a dictionary of parameters. For instance, you can look at the default linestyle with:
plt.rcParams['lines.linestyle']

# The cool thing about this is you can change the defaults at the top of your script (or in a configuration file, won't)
# get into that here - and those parameters will be consistent throughout the script. Within rcParams are subcategories
# such as text, xtick, ytick, and options within those subcategories. For instance, the 'lines' category has options
# 'color', 'linestyle', 'linewidth', and so on. To change one of these, use the rc command
plt.rc('lines', linestyle=':')    # set default to dotted lines
plt.figure()
plt.plot([0, 1], [0, 1])
plt.show()

# So if you have a bunch of configuration options, you can apply them once at the top of your script instead of
# during the plotting part. Remember that these are only setting the default configurations - ie if you set a general
# font size with rc, but want a different size font in one specific part of a figure, you can override the default
# with the command to build that part of the figure!

# Many (most) of the options pointed out further in this script can have their defaults changed in your rc params - and
# it's super nice to have your own defaults to simply copy over when starting a new plotting script.


# ----------------------------------------------------------------------------------------------------------------------
# plt.figure() options
# ----------------------------------------------------------------------------------------------------------------------

# When you create a new figure with plt.figure(), the default size of the figure is provided by your rcParams object.
# ie, plt.rcParams['figure.figsize']. You can supply a nonstandard sized figure using the figsize option
smallfig = plt.figure(figsize=(3, 2))
largefig = plt.figure(figsize=(10, 6))
plt.show()
# The figsize is a tuple of (width, height), in inches
# Note that you can always drag and resize your figures in-window, but their true representation is based off the
# figsize and the resolution - so if you just enlarge a figure by dragging the box corner,you could get resolution
# issues. Another parameter to play with here is the resolution, controlled with dpi (dots per inch). My default
# value is 100, you might want to increase it for a very high-res figure.
highresfig = plt.figure(dpi=200)
plt.show()
# For both of the above parameters, you should look at the guidelines for whatever journal you want to submit to -
# typically they will have limitations on both figure size and resolution.


# ----------------------------------------------------------------------------------------------------------------------
# Errorbars
# ----------------------------------------------------------------------------------------------------------------------

# some sample data
sample_xdata = np.arange(20)
sample_ydata = sample_xdata + (np.random.rand(20) - 0.5) * 4
sample_error = 3 * np.random.rand(20)


# plt.errorbar is similar to plt.plot or plt.scatter with a few differences. This first command makes a lousy plot
plt.figure()
plt.errorbar(sample_xdata,
             sample_ydata,
             yerr=sample_error)   # can have xerr as well
plt.title("Lousy errorbar plot")
plt.show()

# Some problems with the above figure - A) it's a line plot with no points. You might want lines, but a more common
# case is you want points, such as a scatter. B) The errorbars have no caps, which is a weird default in matplotlib.

plt.figure()
plt.errorbar(sample_xdata,
             sample_ydata,
             yerr=sample_error,
             fmt='bo',   # matlab style, color then linestyle
             capsize=5)  # set the caps
plt.title("Better errorbar plot")
plt.show()

# You can play around with the errorbar color separate from the point color. In a crowded figure, I like to make the
# errors a light grey

plt.figure()
plt.errorbar(sample_xdata,
             sample_ydata,
             yerr=sample_error,
             fmt='bo',
             capsize=5,
             ecolor="0.7")
plt.title("Better errorbar plot")
plt.show()


# -------------------------------------------------------------------------------------------------------------------
# Boxes, spines, ticks, and labels
# -------------------------------------------------------------------------------------------------------------------

# The entire box can be made invisible
fig = plt.figure()
ax = plt.subplot()
ax.plot(sample_xdata, sample_ydata, 'ro-')
ax.set_title("No box")
ax.axis('off')
plt.show()

# Or subsets of the box - A common one is to turn off the right and top sides of the box
fig = plt.figure()
ax = plt.subplot()
ax.plot(sample_xdata, sample_ydata, 'ro-')
ax.set_title("Top and right sides gone")
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()

# You can set custom ticks
fig = plt.figure()
ax = plt.subplot()
ax.plot(sample_xdata, sample_ydata, 'ro-')
ax.set_xticks([1, 5, 13, 18.5])
plt.show()

# You can even label the ticks with text
fig = plt.figure()
ax = plt.subplot()
ax.plot(sample_xdata, sample_ydata, 'ro-')
ax.set_xticks([1, 5, 13, 18.5])
ax.set_xticklabels(['one', 'five', 'thirteen', 'whatever'])  # needs to be same size as number of xticks
plt.show()
