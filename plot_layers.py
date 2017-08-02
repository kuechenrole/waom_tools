# Plot the terrain-following vertical levels through a line given in
# roms grid coordinates [i_min,j_min] [i_max,j_max]
# This is a good way to test out different choices
# for vertical stretching parameters.
# Input:
# grid_path = path to ROMS grid file
# lon0 = longitude to interpolate to (-180 to 180)
# depth_min = deepest depth to plot (negative, in metres)
# Vstretching, theta_s, theta_b, hc, N = vertical stretching parameters (see
# *.in configuration file if unsure)

from netCDF4 import Dataset
from numpy import *
from matplotlib.pyplot import *
from calc_z import *


def plot_layers (grid_path, depth_min, depth_max, i_min, j_min, i_max, j_max, Vstretching, theta_s, theta_b, hc, N):

    #read grid
    id = Dataset(grid_path, 'r')
    h = id.variables['h'][:,:]
    zice = id.variables['zice'][:,:]
    mask = id.variables['mask_rho'][:,:]
    id.close()

    #calc 3D field of depth values
    z_3d, sc_r, Cs_r = calc_z(h, zice, theta_s, theta_b, hc, N, None, Vstretching)

    #get a 3D land mask
    mask_3d = tile(mask,(N,1,1))

    #simple array containing layer numbers
    layer_3d_tmp = zeros(shape(z_3d))
    for k in range(N):
        layer_3d_tmp[k,:] = k+1

    #mask out land
    layer_3d = ma.masked_where(mask_3d==0,layer_3d_tmp)

    #simple index array
    idx_4d=np.indices(shape(layer_3d),int)

    #extract values along this line (from stackoverflow)
    #make a line with num points
    num = int(sqrt(square(i_max-i_min)+square(j_max-j_min)))+1
    x,y=np.linspace(i_min,i_max,num),np.linspace(j_min,j_max,num)

    #extract values of 3d arrays along this line 
    z_2d =z_3d[:,y.astype(np.int),x.astype(np.int)]
    idx_3d =idx_4d[:,:,y.astype(np.int),x.astype(np.int)]
    layer_2d =layer_3d[:,y.astype(np.int),x.astype(np.int)]

    #convert index value to distance
    dist_2d=sqrt(square(idx_3d[1])+square(idx_3d[2]))*10.0

    #contour levels
    lev=range(1,N)

    #Plot
    fig=figure(figsize=(18,6))
    contour(dist_2d,z_2d,layer_2d,lev,colors='k')
    title("ROMS Vertical coordinates along the line from \n [i_min, j_min] = "+str([i_min, j_min])+"  to   [i_max, j_max] = "+str([i_max, j_max]), fontsize=24)
    xlabel('Distance (km)')
    ylabel('Depth (m)')
    ylim([depth_min,depth_max])
    fig.show()


# Command-line interface
if __name__ == "__main__":

    grid_path = input("Path to grid file: ")
    depth_min = -1*float(input("Deepest depth to plot (positive, metres): "))
    depth_max = -1*float(input("Shallowest depth to plot (positive, metres): "))
    i_min = int((input('i start (x_axis): ')))
    j_min = int((input('j start (x-axis): ')))
    i_max = int((input('i end (y-axis): ')))
    j_max = int((input('j end (yaxis): ')))
    Vstretching = int(input("Vstretching (2 or 4): "))
    theta_s = float(input("theta_s: "))
    theta_b = float(input("theta_b: "))
    hc = float(input("hc: "))
    N = int(input("N: "))
    plot_layers (grid_path, depth_min, depth_max, i_min, j_min, i_max, j_max, Vstretching, theta_s, theta_b, hc, N)

    # Keep repeating until the user wants to exit
    while True:
        repeat = input("Make another plot (y/n)? ")
        if repeat == 'y':
            while True:
                changes = input("Enter a parameter to change: (1) grid file, (2) depth, (3) start or end, (4) Vstretching, (5) theta_s, (6) theta_b, (7) hc, (8) N; or enter to continue: ")
                if len(changes) == 0:
                    break
                else:
                    if int(changes) == 1:
                        grid_path = input("Path to grid file: ")
                    elif int(changes) == 2:
                        depth_min = -1*float(input("Deepest depth to plot (positive, metres): "))
                        depth_max = -1*float(input("Shallowest depth to plot (positive, metres): "))
                    elif int(changes) == 3:
                        i_min = int((input('i start (x_axis): ')))
                        j_min = int((input('j start (x-axis): ')))
                        i_max = int((input('i end (y-axis): ')))
                        j_max = int((input('j end (yaxis): ')))
                    elif int(changes) == 4:
                        Vstretching = int(input("Vstretching (2 or 4): "))
                    elif int(changes) == 5:
                        theta_s = float(input("theta_s: "))
                    elif int(changes) == 6:
                        theta_b = float(input("theta_b: "))
                    elif int(changes) == 7:
                        hc = float(input("hc: "))
                    elif int(changes) == 8:
                        N = int(input("N: "))
            plot_layers (grid_path, depth_min, depth_max, i_min, j_min, i_max, j_max, Vstretching, theta_s, theta_b, hc, N)
        else:
            break
