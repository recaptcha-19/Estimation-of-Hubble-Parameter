import numpy as np
import astropy.units as u
import pandas as pd

class galaxy:

    def __init__(self, name, type_of_data, distance):
        self.name = name
        self.type = type_of_data
        self.vel = 0
        self.dist = distance
        self.rot_vel = np.zeros((2))
        self.lum_density = np.zeros((2))
        #2 elements in array, one for error 

    def velocity_calculator(self, vel, lum):
        #vel and lum refer to hydrogen line frequency/velocity corresponding to Doppler shift and surface brightness respectively
        if self.type == 'velocity':
            vel = vel*u.m/u.s
            vel = vel.to(u.km/u.s)
            galaxy_vel =  sum(vel*lum)/sum(lum)
            self.vel = galaxy_vel

        #f_obs and f_rest refer to observed and rest frequency respectively
        if self.type == 'frequency':
            f_obs = vel*u.Hz
            c = 3*10**8*u.m/u.s
            f_rest = 1.42040580*10**9*u.Hz
            velocity = c*(1 - (f_obs/f_rest)**2)/(1 + (f_obs/f_rest)**2)
            velocity = velocity.to(u.km/u.s)
            galaxy_vel =  sum(velocity*lum)/sum(lum)
            self.vel = galaxy_vel
        
        return self.vel

    def lum_density_calculator(self, sum_pix, npix, mean_median, mean_stddev):
        Jansky = 10**-26*u.W/((u.m)**2*u.Hz)
        Mpc = u.parsec*10**6
        self.dist = np.asarray(self.dist)
        self.dist = self.dist*Mpc
        
        mean_median = mean_median*10**6*Jansky/u.sr
        mean_stddev = mean_stddev*10**6*Jansky/u.sr
        sum_pix = sum_pix*10**6*Jansky/u.sr

        mean_median = mean_median/8
        mean_stddev = mean_stddev/8
        signal = sum_pix - npix*mean_median
        error = mean_stddev*np.sqrt(npix)

        self.dist = self.dist.to(u.m)
        #removing the dependence on solid angles
        pixel_size = 0.75*u.arcsec
        pixel_area = (pixel_size**2).to(u.sr)
        signal = signal*pixel_area
        error = error*pixel_area

        if self.dist[0] == 0:
            return signal, error

        #converting signal and error to luminosity densities
        self.lum_density = self.lum_density*u.W/u.Hz
        self.lum_density[0] = signal*4*np.pi*self.dist[0]**2
        
        #error propagation
        self.lum_density[1] = (2*self.dist[1].value/self.dist[0].value + error.value/signal.value)*self.lum_density[0]

        print("Luminosity density: {} {}".format(self.lum_density[0].value, self.lum_density[0].unit)) 
        print("Error: {} {}".format(self.lum_density[1], self.lum_density[1].unit))      

        return self.lum_density[0], self.lum_density[1]

    def __del__(self):
        print("Successfully destroyed object")