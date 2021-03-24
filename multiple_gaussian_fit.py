#program to fit multiple Gaussian functions to a plot of surface brightness vs velocity/frequency 
#and obtain the rotational velocity of the galaxy along with error magnitudes

import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def multiple_gaussian(x, *guess):
    sum = 0
    for i in range(0, len(guess)-2, 3):
        a = guess[i] 
        mu = guess[i+1] 
        sigma = guess[i+2] 
        sum += a*np.exp(-0.5*((x - mu)/sigma)**2)
    return sum

f = np.loadtxt("ngc_2903.txt")
vel, lum = f[:,0], f[:,1]
vel, lum = vel[::-1], lum[::-1]
'''if name == "ngc_3198.txt":
    f_rest = 1.42040580*10**9
    c = 3*10**8
    vel = c*(1 - (vel/f_rest)**2)/(1 + (vel/f_rest)**2)'''

args = np.argsort(lum)
vel_lum, lum_sorted = vel[args], lum[args]

#finding peaks in the surface brightness vs velocity graph
x1, y1 = vel, lum
peaks = find_peaks(y1, height = 6*10**-4, prominence = 5*10**-5)
peaks_pos = x1[peaks[0]]
print("No of peaks is {}".format(np.shape(peaks_pos)))
peaks_heights = peaks[1]['peak_heights'] 
plt.plot(x1,y1)
plt.scatter(peaks_pos, peaks_heights, marker = 'x', c = 'red', s = 50)
plt.grid()
plt.show()

#fitting the Gaussians using the knowledge of the no of peaks
guess = [4*10**-5, 3.75*10**5, 0.25*10**5, 10**-5, 4.75*10**5, 10**5, 10**-5, 7.25*10**5, 10**5]
#guess = [2*10**-5, 4.75*10**5, 5*10**4, 2*10**-5, 7*10**5, 0.5*10**5]
params, pcov = curve_fit(multiple_gaussian, x1, y1, p0 = guess, maxfev = 10000)
print(params)
print(np.sqrt(np.diag(pcov)))
plt.plot(x1, y1)
plt.plot(x1, multiple_gaussian(x1, *params))
plt.grid()
plt.show()

#finding the rotational velocity of the galaxy and its error 
y_1 = peaks_heights[0]/2
y_2 = peaks_heights[-1]/2
a_1, mu_1, sigma_1 = params[0:3]
a_2, mu_2, sigma_2 = params[-3:]
x_1 = mu_1 - sigma_1*np.sqrt(2*np.log(a_1/y_1))
x_2 = mu_2 + sigma_2*np.sqrt(2*np.log(a_2/y_2))
fwhm = x_2 - x_1
a_1_error, mu_1_error, sigma_1_error = np.sqrt(np.diag(pcov))[0:3]
a_2_error, mu_2_error, sigma_2_error = np.sqrt(np.diag(pcov))[-3:]
x_1_error = mu_1_error + (sigma_1_error/sigma_1 + a_1_error/(2*a_1))*sigma_1*np.sqrt(2*np.log(a_1/y_1))
x_2_error = mu_2_error + (sigma_2_error/sigma_2 + a_2_error/(2*a_2))*sigma_2*np.sqrt(2*np.log(a_2/y_2))
fwhm_error = x_1_error + x_2_error

print("Rotational velocity: {}".format(fwhm))
print("Error: {}".format(fwhm_error))



    



