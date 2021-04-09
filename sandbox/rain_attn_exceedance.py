#!/usr/bin/env python3

import sys, os
import itur
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import warnings
import argparse
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    #--------START Command Line option parser------------------------------------------------------
    parser = argparse.ArgumentParser(description="Rain Attenuation Exceedance Calculator",
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
    fs.add_argument("--o_name", dest = "o_name", action = "store", type = str, default='Rain_Attenuation_Exceedance' , help = "Output File Base Name")
    fs.add_argument("--save_fig", dest = "save_fig", action = "store", type = int, default=0 , help = "Save Figure, 0=No, 1=Yes")

    parser.add_argument("--freq",  dest = "freq",  action = "store", type = float, default=1575.42e6 , help = "Operating Frequency [Hz]")
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

    #elevations=[1,2,3,4,5,6,7,8,9,10]
    elevations=np.linspace(1,10,10)

    #f = 22.5 * u.GHz    # Link frequency
    #f = 1.57543 * u.GHz    # Link frequency
    f = args.freq / 1e9 * u.GHz #Link frequency
    D = 0.1 * u.m       # Antenna diameters

    rain_attn = {}
    # Define unavailabilities vector
    unavailabilities = np.logspace(-1.5, 1.5, 100)
    for el in elevations:
        print("Computing Rain Attenuation for Elevation = {:2.1f}".format(el))
        A_g, A_c, A_r, A_s, A_t = [], [], [], [], []
        for idx, p in enumerate(unavailabilities):
            a_g, a_c, a_r, a_s, a_t = itur.atmospheric_attenuation_slant_path(gs_lat, gs_lon,
                                                                            f, el, p, D,
                                                                            return_contributions=True)
            A_g.append(a_g.value)
            A_c.append(a_c.value)
            A_r.append(a_r.value)
            A_s.append(a_s.value)
            A_t.append(a_t.value)
        rain_attn["{:2.1f}".format(el)] = A_r

    print("\n")
    # Plot the results

    xinch = 7
    yinch = 4
    fig1=plt.figure(1, figsize=(xinch,yinch/.8))
    ax = fig1.add_subplot(1,1,1)
    #ax.semilogx(unavailabilities, A_g, label='Gaseous attenuation')
    #ax.semilogx(unavailabilities, A_c, label='Cloud attenuation')
    for el in elevations:
        print("Plotting Rain Attenuation for Elevation = {:2.1f}".format(el))
        lbl_str='El={:2.1f}'.format(el)
        ax.semilogx(unavailabilities, rain_attn["{:2.1f}".format(el)], label=lbl_str+"$^{\circ}$")
    #ax.semilogx(unavailabilities, A_s, label='Scintillation attenuation')
    #ax.semilogx(unavailabilities, A_t, label='Total atmospheric attenuation')

    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlabel('Percentage of time attenuation value is exceeded [%]')
    ax.set_ylabel('Attenuation [dB]')
    title_str = 'Rain Attenuation Exceedance'

    # place a text box in upper left in axes coords
    #subtitle_str = "GS Location: {:s}\n{:2.6f}, {:2.6f}".format(gs_name, gs_lat, gs_lon)
    subtitle_str = "GS Location: {:s}\n".format(gs_name)
    subtitle_str += "{:2.6f}".format(gs_lat) + "$^{\circ}$, "
    subtitle_str += "{:2.6f}".format(gs_lon) + "$^{\circ}$"
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.15, 0.95, subtitle_str, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    ax.set_title(title_str, fontsize=10,fontweight="bold")
    #plt.suptitle(title_str, fontsize=12, fontweight="bold")
    ax.grid(which='both', linestyle=':')
    plt.legend()
    plt.show()
    if args.save_fig:
        print("Saving Figure: ", fig_path)
        fig1.savefig(fig_path)
