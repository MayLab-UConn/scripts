import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

''' This script has a (hopefully) well-documented example on how to make an animation/video of a dataset.

    The example data set we'll use is from Alder lab - a system for which fluorescense intensity is modulated
    by additions of chemicals at different timepoints. We'll animate the timecourse
'''
# loading the data.
anim_data = np.loadtxt('sample_files/animations/animation_data.csv', delimiter=',')
anim_data[:, 1] = anim_data[:, 1] / np.max(anim_data[:, 1])   # normalize intensity
adp_points = [300, 500, 700]   # these are the timepoints where ADP is added - we'll plot some lines to indicate them

# setting up the basics of the figure - these won't change with the animation
anim_fig = plt.figure()
plt.xlim(-10, 1000)
plt.ylim(0.5, 1.1)
plt.xlabel('time (s)')
plt.ylabel('Relative fluorescence intensity')
plt.plot([100, 100], [0.5, 1], 'k--', alpha=0.3)   # some lines to indicate when things is added
plt.plot([300, 300], [0.5, 1], 'k--', alpha=0.3)
plt.plot([500, 500], [0.5, 1], 'k--', alpha=0.3)
plt.plot([700, 700], [0.5, 1], 'k--', alpha=0.3)

# The best way to have an animation is to have a set of data that is updated every frame. We'll start it empty, and
# then add data points as the animation goes along
data = plt.scatter([], [], 5)


# This is our update function. It should take a parameter corresponding to the frame number. You can name the function
# whatever you want - notice that it's specified further down in the FuncAnimation function, so if you want to name
# it something else
def anim_update(i):
    data.set_offsets(anim_data[:i, :])  # when this is called, populates "data" up to the ith frame


# This is the function call that makes the animation
ani_obj = animation.FuncAnimation(anim_fig,                      # first input is the figure handle
                                  anim_update,                   # second input is the update function
                                  frames=anim_data.shape[0],     # number of frames (i values to anim_update)
                                  interval=15)                   # delay between frames

plt.show()

# ani_obj.save('sample_files/animations/sample.mp4')
