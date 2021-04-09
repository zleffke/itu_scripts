#!/usr/bin/env python3
""" This example shows how to compute the 'attenuation exceeded for 0.1 % of
time of the average year' vs. 'frequency' and 'elevation angle'
for a single location.

For the 'attenuation exceeded for 0.1 % of time of the average year' vs.
'frequency' case the link is assume to be a space-to-Earth link between
a ground station in Boston and a satellite in GEO orbit (slot 77W).

For the 'attenuation exceeded for 0.1 % of time of the average year' vs.
'elevation' case, the link operates at 22.5 GHz.

The receiver antenna has a 1.2 m diameter in both cases.
"""
import sys, os
import itur
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import argparse
import warnings
warnings.filterwarnings("ignore")


if __name__ == '__main__':
    #--------START Command Line option parser------------------------------------------------------
    parser = argparse.ArgumentParser(description="Cloud Attenuation Calculator",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    h_gs_lat    = "Ground Station Latitude [deg]"
    h_gs_lon    = "Ground Station Longitude [deg]"

    gs = parser.add_argument_group('Ground Station Parameters')
    gs.add_argument("--gs_name", dest = "gs_name", action = "store", type = str, default='BlacksburgVA' , help = "Ground Station Name")
    gs.add_argument("--gs_lat", dest = "gs_lat", action = "store", type = float, default='37.206831' , help = "Ground Station Latitude [deg]")
    gs.add_argument("--gs_lon", dest = "gs_lon", action = "store", type = float, default='-80.419138', help = "Ground Station Longitude [deg]")

    fs = parser.add_argument_group('Filesystem Parameters')
    o_path_default = os.getcwd() + '/output'
    fs.add_argument("--o_path", dest = "o_path", action = "store", type = str, default= o_path_default , help = "Output File Path")
    fs.add_argument("--o_name", dest = "o_name", action = "store", type = str, default='Cloud_Attenuation_vs_Elevation' , help = "Output File Base Name")
    fs.add_argument("--save_fig", dest = "save_fig", action = "store", type = int, default=0 , help = "Save Figure, 0=No, 1=Yes")

    parser.add_argument("--freq",  dest = "freq",  action = "store", type = float, default=1575.42e6 , help = "Operating Frequency [Hz]")
    parser.add_argument("--exceedance",  dest = "exceedance",  action = "store", type = float, default=1 , help = "Percent Exceedance [%]")
    args = parser.parse_args()
    #--------END Command Line option parser------------------------------------------------------
    os.system('reset')
    #print ('args:', args)
    o_path = args.o_path
    if not os.path.exists(o_path): os.makedirs(o_path)
    fig_path = o_path + "/" + args.o_name + "_" + args.gs_name + ".png"
    print("Figure Path:", fig_path)

    # Ground station coordinates (Blacksburg, Hume)
    gs_name = args.gs_name
    gs_lat  = args.gs_lat
    gs_lon  = args.gs_lon

    # Ground station coordinates (Blacksburg, Hume)
    lat_GS = 37.206831
    lon_GS = -80.419138

    f = args.freq / 1e9 * u.GHz #Link frequency
    D = 0.1 * u.m       # Antenna diameters
    p = args.exceedance
    el = np.linspace(1, 90, 100)
    #el[0] = 1e-10

    Ag, Ac, Ar, As, A =\
        itur.atmospheric_attenuation_slant_path(gs_lat, gs_lon, f, el, p, D,
                                                return_contributions=True)

    # Plot the results
    xinch = 7
    yinch = 4
    fig1=plt.figure(1, figsize=(xinch,yinch/.8))
    ax = fig1.add_subplot(1,1,1)
    #ax.plot(el, Ag, label='Gaseous attenuation')
    ax.plot(el, Ac, label='Cloud attenuation')
    #ax.plot(el, Ar, label='Rain attenuation')
    #ax.plot(el, As, label='Scintillation attenuation')
    #ax.plot(el, A, label='Total atmospheric attenuation')
    title_str = 'Worst Case ({:1.1f}%) Cloud Attenuation vs Elevation'.format(p)
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlabel('Elevation angle [deg]')
    ax.set_ylabel('Attenuation [dB]')
    subtitle_str = "GS Location: {:s}\n".format(gs_name)
    subtitle_str += "{:2.6f}".format(gs_lat) + "$^{\circ}$, "
    subtitle_str += "{:2.6f}".format(gs_lon) + "$^{\circ}$"
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.5, 0.9, subtitle_str, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    ax.set_title(title_str, fontsize=10,fontweight="bold")
    ax.grid(which='both', linestyle=':')
    #plt.legend()
    plt.show()
    if args.save_fig:
        print("Saving Figure: ", fig_path)
        fig1.savefig(fig_path)
