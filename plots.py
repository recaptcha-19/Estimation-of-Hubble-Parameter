import numpy as np
import matplotlib.pyplot as plt
from galaxy import galaxy
import pandas as pd
import astropy.units as u
from scipy.optimize import curve_fit

def line(x,H_0,k):
    return H_0*x + k

#obtaining the distance of the galaxy from luminosity density values
def distance(v_rot, error_v_rot, flux_density, error_flux_density):
    lum_density_estimate = A*v_rot.value**beta
    lum_density_estimate = lum_density_estimate*u.W/u.Hz
    error_lum_density_estimate = (beta*error_v_rot/v_rot)*lum_density_estimate
    distance = np.sqrt(lum_density_estimate/(4*np.pi*flux_density))
    error_distance = (distance/2)*(error_flux_density/flux_density + error_lum_density_estimate/lum_density_estimate)
    distance = distance.to(Mpc)
    error_distance = error_distance.to(Mpc)
    return distance, error_distance

def parameter_finder(name):
    g = open(name + "_stats.txt")
    contents = g.readlines()
    x = contents[11].split('\t')
    del x[-1]
    del x[0]
    sum_pix, npix = float(x[0]), float(x[1])
    mean_median_value = stuff.loc[stuff['galaxy_name'] == name]['mean_median']
    mean_stddev_value = stuff.loc[stuff['galaxy_name'] == name]['mean_stddev']
    mean_median = mean_median_value.iloc[0]
    mean_stddev = mean_stddev_value.iloc[0]
    return sum_pix, npix, mean_median, mean_stddev

Mpc = u.pc*10**6

#obtaining the rotational velocity and luminosity density of known galaxies
stuff = pd.read_csv("circle_stats.txt")
rot_vel, error_rot_vel = stuff['rot_vel'], stuff['error_rot_vel']
lum_density, error_lum_density = stuff['lum_density'], stuff['error_lum_density']
x = np.where(rot_vel == 0.00)

rot_vel = rot_vel.values
error_rot_vel = error_rot_vel.values
lum_density = lum_density.values
error_lum_density = error_lum_density.values

rot_vel = np.delete(rot_vel, [4,6,11])
error_rot_vel = np.delete(error_rot_vel, [4,6,11])
lum_density = np.delete(lum_density, [4,6,11])
error_lum_density = np.delete(error_lum_density, [4,6,11])

#obtaining the Tully-Fisher relation
z = np.polyfit(np.log(rot_vel)[0:9], np.log(lum_density)[0:9], 1)
plt.scatter(np.log(rot_vel)[0:9], np.log(lum_density)[0:9])
plt.plot(np.log(rot_vel), z[1] + z[0]*np.log(rot_vel))
plt.xlabel('ln v_rot (m/s)')
plt.ylabel('ln L_v (W/Hz)')
plt.title('Tully-Fisher relation')
plt.show()
   
A = np.exp(z[1])
beta = z[0]

rot_vel, error_rot_vel = rot_vel*u.m/u.s, error_rot_vel*u.m/u.s
lum_density, error_lum_density =  lum_density*u.W/u.Hz, error_lum_density*u.W/u.Hz

#finding distances to two galaxies; NGC 628 and NGC 2903 and estimating the Hubble parameter
ngc_628 = galaxy("ngc_628", "velocity", [0,0])
sum_pix_628, npix_628, mean_median_628, mean_stddev_628 = parameter_finder("ngc_628")
flux_density_628, error_flux_density_628 = ngc_628.lum_density_calculator(sum_pix_628, npix_628, mean_median_628, mean_stddev_628)

rot_vel_628 = (stuff.loc[stuff['galaxy_name'] == "ngc_628"]["rot_vel"]).iloc[0]
rot_vel_628 *= u.m/u.s
error_rot_vel_628 = (stuff.loc[stuff['galaxy_name'] == "ngc_628"]["error_rot_vel"]).iloc[0]
error_rot_vel_628 *= u.m/u.s
ngc_628_distance, ngc_628_distance_error = distance(rot_vel_628, error_rot_vel_628, flux_density_628, error_flux_density_628)
vel_628, lum_628 = np.loadtxt("ngc_628.txt")[:,0], np.loadtxt("ngc_628.txt")[:,1] 
ngc_628_velocity = ngc_628.velocity_calculator(vel_628, lum_628)
print(ngc_628_velocity)
print(ngc_628_distance)
ngc_2903 = galaxy("ngc_2903", "velocity", [0,0])
sum_pix_2903, npix_2903, mean_median_2903, mean_stddev_2903 = parameter_finder("ngc_2903")
flux_density_2903, error_flux_density_2903 = ngc_2903.lum_density_calculator(sum_pix_2903, npix_2903, mean_median_2903, mean_stddev_2903)

rot_vel_2903 = (stuff.loc[stuff['galaxy_name'] == "ngc_2903"]["rot_vel"]).iloc[0]
rot_vel_2903 *= u.m/u.s
error_rot_vel_2903 = (stuff.loc[stuff['galaxy_name'] == "ngc_2903"]["error_rot_vel"]).iloc[0]
error_rot_vel_2903 *= u.m/u.s
ngc_2903_distance, ngc_2903_distance_error = distance(rot_vel_2903, error_rot_vel_2903, flux_density_2903, error_flux_density_2903)
vel_2903, lum_2903 = np.loadtxt("ngc_2903.txt")[:,0], np.loadtxt("ngc_2903.txt")[:,1] 
ngc_2903_velocity = ngc_2903.velocity_calculator(vel_2903, lum_2903)
print(ngc_2903_velocity)
print(ngc_2903_distance)

x = np.array([ngc_628_distance.value, ngc_2903_distance.value])
y = np.array([ngc_628_velocity.value, ngc_2903_velocity.value])
    
popt, pcov = curve_fit(line, x, y)
H_0 = popt[0]*u.km/(u.s*Mpc)
print("Hubble constant is {}".format(H_0))
