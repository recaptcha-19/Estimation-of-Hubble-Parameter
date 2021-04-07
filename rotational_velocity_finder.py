import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from galaxy import galaxy

def multiple_gaussian(x, *guess):
    sum = 0
    for i in range(0, len(guess)-2, 3):
        mu = guess[i] 
        sigma = guess[i+1] 
        a = guess[i+2] 
        sum += a*np.exp(-0.5*((x - mu)/sigma)**2)
    return sum

#finding peaks in the surface brightness vs velocity graph
def peak_finder(vel, lum, Height, Prominence):
    x1, y1 = vel, lum
    peaks = find_peaks(y1, height = Height, prominence = Prominence)
    peaks_pos = x1[peaks[0]]
    print("No of peaks is {}".format(np.shape(peaks_pos)))
    peaks_heights = peaks[1]['peak_heights'] 
    plt.plot(x1,y1)
    plt.scatter(peaks_pos, peaks_heights, marker = 'x', c = 'red', s = 50)
    plt.grid()
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Surface brightness (MJy/sr)')
    plt.show()
    return peaks_heights

#fitting the Gaussians using the knowledge of the no of peaks; guess size is 3*no of peaks
def multiple_gaussian_fit(vel, lum, guess):
    params, pcov = curve_fit(multiple_gaussian, vel, lum, p0 = guess, maxfev = 100000)
    error_params = np.sqrt(np.diag(pcov))
    plt.plot(vel, lum)
    plt.plot(vel, multiple_gaussian(vel, *params))
    plt.grid()
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Surface brightness (MJy/sr)')
    plt.show()
    return params, error_params

#finding the rotational velocity of the galaxy and its error 
ngc_2403 = galaxy("ngc_2403", "velocity", [9.2,0.2])
f = np.loadtxt("ngc_2403.txt")
vel, lum = f[:,0], f[:,1]
vel, lum = vel[::-1], lum[::-1]

if ngc_2403.type == "frequency":
    f_rest = 1.42040580*10**9
    c = 3*10**8
    vel = c*(1 - (vel/f_rest)**2)/(1 + (vel/f_rest)**2)

peaks_heights = peak_finder(vel, lum, 3*10**-4, 10**-5)
params, errors = multiple_gaussian_fit(vel, lum, [0.25*10**5, 2.5*10**4, 4*10**-5, 1.5*10**5, 10**5, 10**-5, 2.25*10**5, 0.5*10**5, 2*10**-5])
print(params)
print(errors)

#finding FWHM and error in rotational velocity
y_1 = peaks_heights[0]/2
y_2 = peaks_heights[-1]/2
sigma_1, mu_1, a_1 = params[0:3]
sigma_2, mu_2, a_2 = params[-3:]
x_1 = mu_1 - sigma_1*np.sqrt(2*np.log(a_1/y_1))
x_2 = mu_2 + sigma_2*np.sqrt(2*np.log(a_2/y_2))
fwhm = x_2 - x_1
sigma_1_error, mu_1_error, a_1_error = errors[0:3]
sigma_2_error, mu_2_error, a_2_error = errors[-3:]
x_1_error = mu_1_error + (sigma_1_error/sigma_1 + a_1_error/(2*a_1))*sigma_1*np.sqrt(2*np.log(a_1/y_1))
x_2_error = mu_2_error + (sigma_2_error/sigma_2 + a_2_error/(2*a_2))*sigma_2*np.sqrt(2*np.log(a_2/y_2))
fwhm_error = x_1_error + x_2_error

print("Rotational velocity: {} m/s".format(fwhm))
print("Error: {} m/s".format(fwhm_error))

