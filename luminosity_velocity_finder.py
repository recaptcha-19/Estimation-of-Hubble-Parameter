
mport astropy.units as u
from galaxy import galaxy
import numpy as np
import pandas as pd

#circle_stats.txt contains regions details as well as distance, receding velocity and luminosity density 
stuff = pd.read_csv("circle_stats.txt")
stuff['receding_velocity'] = np.zeros(14)
stuff['lum_density'] = np.zeros(14)
stuff['error_lum_density'] = np.zeros(14)
receding_velocities = []
lum_density = []
error_lum_density = []

for i in range(12):
    name = stuff['galaxy_name'][i]
    print(name)
    type_of_data = stuff['type'][i]
    distance_mag = stuff['distance_mag'][i]
    distance_error = stuff['distance_error'][i]
    galaxy_object = galaxy(name, type_of_data, [distance_mag, distance_error])
    f = np.loadtxt(name + ".txt")
    vel, lum = f[:,0], f[:,1]
    galaxy_velocity = galaxy_object.velocity_calculator(vel, lum)
    print(galaxy_velocity)
    receding_velocities.append(galaxy_velocity.value)

    #obtain sum_pix and npix values from name + "_stats.txt"
    g = open(name + "_stats.txt")
    contents = g.readlines()
    x = contents[11].split('\t')
    del x[-1]
    del x[0]
    sum_pix, npix = float(x[0]), float(x[1])

    a = stuff[stuff['galaxy_name'] == name]
    mean_median, mean_stddev = a.values[0][1], a.values[0][2]
    lum, error = galaxy_object.lum_density_calculator(sum_pix, npix, mean_median, mean_stddev)
    lum_density.append(lum.value)
    error_lum_density.append(error.value)

    del galaxy_object
    g.close()

#assigning proper units to the desired quantities and storing luminosity density and receding velocity in the same text file
receding_velocities = receding_velocities*u.m/u.s
lum_density = lum_density*u.W/u.Hz
error_lum_density*u.W/u.Hz
np.asarray(receding_velocities)
np.asarray(lum_density)
np.asarray(error_lum_density)

stuff['lum_density'][:12] = lum_density
stuff['error_lum_density'][:12] = error_lum_density
stuff['receding_velocity'][:12] = receding_velocities

stuff.to_csv("circle_stats.txt")