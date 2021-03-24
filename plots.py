#program to obtain the Tully-Fisher relation, and using the same, calculate the distances to a few galaxies using their flux densities 
#and hence estimate the Hubble parameter using thee known values of their velocities and distances

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numerical_analysis import numerical_analysis

#rotational velocities of galaxies
v_rot = np.array([[217321.54, 13137.96], 
[249086, 12297.55], 
[579259.52, 11300.73], 
[410604.03, 6259.86], 
[397569.92, 40810.21], 
[337300.52, 24331.08], 
[327589.24, 34442.63], 
[278291.81, 24215.56], 
[521106.23, 35033.27]])
np.sort(v_rot[:,0])

#luminosities of galaxies
lum = np.array([[3.33*10**18, 1.23*10**16], 
[2.23*10**18, 6.17*10**15], 
[2.96*10**19, 9.26*10**16], 
[1.66*10**19, 6.17*10**15], 
[8.92*10**18, 2.47*10**16], 
[2.34*10**19, 2.47*10**16], 
[1.61*10**19, 1.85*10**16], 
[2.21*10**19, 1.85*10**16], 
[3.90*10**19, 3.70*10**16]])
np.sort(lum[:,0])
velocity = v_rot[:,0]
luminosity = lum[:,0]

#obtaining the Tully-Fisher relation
z = np.polyfit(np.log(velocity), np.log(luminosity), 1)
print(z)
plt.scatter(np.log(velocity), np.log(luminosity))
plt.plot(np.log(velocity), z[1] + z[0]*np.log(velocity))
plt.show()
    
A = np.exp(z[1])
beta = z[0]

#obtaining the distance from from density values
def distance(v_rot, lum_density):
    luminosity = A*v_rot**beta
    distance = np.sqrt(luminosity/(4*np.pi*lum_density))
    return distance

ngc_628_distance = distance(478244.97, 8.959517373055649*10**-18)
ngc_2903_distance = distance(476000, 1.6147237513376122*10**-17)
ngc_2903_vel = 548641.1571541023
ngc_2903_distance = ngc_2903_distance*3.2407*10**-23 #converting to Mpc
ngc_628_distance = ngc_628_distance*3.2407*10**-23








