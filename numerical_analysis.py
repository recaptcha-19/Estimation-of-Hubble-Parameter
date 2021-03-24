#program to calculate flux density and velocity with which a galaxy moves away from earth and their errors

import numpy as np
import matplotlib.pyplot as plt 
import astropy.units as u

Jansky = 10**-26*u.W/((u.m)**2*u.Hz)

def numerical_analysis(name, sum_pix, npix, mean_median, mean_stddev, type_of_data, distance):
    distance = np.asarray(distance)
    distance = distance*u.parsec
    mean_median = mean_median*10**6*Jansky/u.sr
    mean_stddev = mean_stddev*10**6*Jansky/u.sr
    sum_pix = sum_pix*10**6*Jansky/u.sr

    mean_median = mean_median/8
    mean_stddev = mean_stddev/8
    signal = sum_pix - npix*mean_median
    error = mean_stddev*np.sqrt(npix)
    
    signal = signal*0.75*(180/(np.pi*3600))
    error = error*0.75*(180/(np.pi*3600))
    print(signal)
    print(error)

    distance = distance.to(u.m)

    #conversion is done, but sr is still retained; convert them to luminosity densities
    lum_signal = signal*u.sr*4*np.pi*distance[0]**2
    print(lum_signal.unit)
    flux_error = error*u.sr
    lum_error = (2*distance[1].value + flux_error.value)*u.W/u.Hz

    f = np.loadtxt(name + ".txt")
    #f[:,0] -> velocity/frequency, f[:,1] -> surface brightness
    brightness = f[:,1]
    if type_of_data == "velocity":
        velocity = f[:,0]*u.m/u.s
        velocity.to(u.km/u.s)

    else:
        f_obs = f[:,0]*u.Hz
        c = 3*10**8*u.m/u.s
        f_rest = 1.42040580*10**9*u.Hz
        velocity = c*(1 - (f_obs/f_rest)**2)/(1 + (f_obs/f_rest)**2)
    
    #Velocity with which the galaxy moves away from us
    galaxy_vel = np.sum(velocity*brightness)/np.sum(brightness)
    print(galaxy_vel)
    return lum_signal, lum_error

lum_signal, lum_error = numerical_analysis(name = "ngc_2903", sum_pix = 134365.42, npix = 367971, mean_median = -0.019770268, mean_stddev = 0.06018012, type_of_data = "velocity", distance = np.array([3.4, 0.2]))

print("Luminosity: {} {}".format(lum_signal.value, lum_signal.unit)) 
print("Error: {} {}".format(lum_error.value, lum_error.unit))



    

    







    

