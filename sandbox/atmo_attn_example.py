#!/usr/bin/env python3

import itur
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Ground station coordinates (Blacksburg, Hume)
lat_GS = 37.206831
lon_GS = -80.419138

el=10
#f = 22.5 * u.GHz    # Link frequency
f = 1.57543 * u.GHz    # Link frequency
D = 0.1 * u.m       # Antenna diameters



# Define unavailabilities vector
unavailabilities = np.logspace(-1.5, 1.5, 100)

# Compute the
A_g, A_c, A_r, A_s, A_t = [], [], [], [], []

for idx, p in enumerate(unavailabilities):
        a_g, a_c, a_r, a_s, a_t = itur.atmospheric_attenuation_slant_path(lat_GS, lon_GS,
                                                                          f, el, p, D,
                                                                          return_contributions=True)
        A_g.append(a_g.value)
        A_c.append(a_c.value)
        A_r.append(a_r.value)
        A_s.append(a_s.value)
        A_t.append(a_t.value)

# Plot the results
ax = plt.subplot(1,1,1)
#ax.semilogx(unavailabilities, A_g, label='Gaseous attenuation')
ax.semilogx(unavailabilities, A_c, label='Cloud attenuation')
ax.semilogx(unavailabilities, A_r, label='Rain attenuation')
#ax.semilogx(unavailabilities, A_s, label='Scintillation attenuation')
#ax.semilogx(unavailabilities, A_t, label='Total atmospheric attenuation')

ax.xaxis.set_major_formatter(ScalarFormatter())
ax.set_xlabel('Percentage of time attenuation value is exceeded [%]')
ax.set_ylabel('Attenuation [dB]')
ax.set_title('Rain and Cloud Attenuation Probabilities, Elevation={:2.1f} [deg]'.format(el))
ax.grid(which='both', linestyle=':')
plt.legend()
plt.show()
