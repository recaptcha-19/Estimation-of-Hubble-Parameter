import numpy as np

def sort(string):
    f = np.loadtxt(string)
    vel, lum = f[:,0], f[:,1]
    args = np.argsort(lum)
    vel_lum, lum_sorted = vel[args], lum[args]
    return vel_lum[-1], lum_sorted[-1]

sorted_lum = sort("ngc_2903.txt")
print(sorted_lum)
    



