# Estimation of Hubble Parameter Project  

This is the estimation of Hubble parameter project using one of the rungs of the cosmic distance ladder, i.e. the Tully-Fisher relation. 

## Introduction

The cosmic distance ladder is a succession of measurements by which astronomers measure distances to objects in the universe. It is typically done by using an object of known brightness (also known as a *standard candle*). Knowing the apparent brightness as seen from earth and using the knowledge of the intrinsic brightness of the standard candle, the distance to unknown objects can be measured. 

If the receding velocity of the object and its distance are known, the Hubble parameter can be estimated from *Hubble's Law*:

<p align="center">
  <img src="https://latex.codecogs.com/gif.latex?v%20%3D%20H_0d" />
</p>

where ![](https://latex.codecogs.com/gif.latex?v) is the receding velocity of the galaxy and ![](https://latex.codecogs.com/gif.latex?d) is the distance to the galaxy in megaparsecs (Mpc). The Hubble constant is measured in km/s/Mpc.

The Tully Fisher relation relates the intrinsic luminosity of a galaxy to its rotational velocity by a power law:

<p align="center">
  <img src="https://latex.codecogs.com/gif.latex?L_%5Cnu%20%3D%20Av_%7Brot%7D%5E%5Cbeta" />
</p>

where ![](https://latex.codecogs.com/gif.latex?L_%5Cnu) represents the intrinsic luminosity of the galaxy at a specific wavelength and ![](https://latex.codecogs.com/gif.latex?v_%7Brot%7D) represents the rotational velocity of the galaxy. 

By manipulating and processing image data, one can obtain rotational velocities and apparent brightness of galaxies and thus, by employing the Tully-Fisher relation, estimate their distances and ultimately the Hubble parameter.


## Image Data and Properties of Galaxies

The project makes use of information and FITS images of different galaxies obtained from the [NASA/IPAC Extragalactic Database (NED)](https://ned.ipac.caltech.edu/byname). The dataset consists of images of two sets of galaxies, one with known distances and vice-versa. For each galaxy, there is a FITS image observed at an infrared wavelength of 3.6 ![](https://latex.codecogs.com/gif.latex?%5Cmu%20m), and a radio wavelength image that traces the hydrogen gas in the galaxies and can be used to measure the rotational velocities. 

The distances to galaxies have been obtained from Cepheid data analyzed by the [Hubble Space Telescope Key Project to Measure the Hubble Constant](https://www.stsci.edu/stsci/meetings/shst2/freedmanw.html). The inclinations to galaxies have been obtained from [The HI Nearby Galaxy Survey (THINGS)](https://www2.mpia-hd.mpg.de/THINGS/Overview.html).

The exact data used and a more detailed explanation of the procedure followed can be seen [here](https://github.com/recaptcha-19/Estimation-of-Hubble-Parameter/blob/master/experiment_tullyfisher_university.pdf)[^1].

## Procedure
* Choose a specific galaxy with a known distance and open its IR image in [SAOImage DS9](https://sites.google.com/cfa.harvard.edu/saoimageds9).
* Set an appropriate region for the galaxy (to measure the signal, i.e. the apparent brightness) and multiple small surrounding regions (to measure the noise which will be subtracted) as shown in the image. 
<p align="center">
  <img src="https://github.com/recaptcha-19/Estimation-of-Hubble-Parameter/blob/master/galaxy_regions.png" />
</p>



[^1]: by George J. Bendo and Ishmaeel Iqbal from the Jodrell Bank Centre for Astrophysics, The University of Manchester
