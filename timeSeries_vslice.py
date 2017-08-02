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


def plot_vslice (file_path, timestep, variable, depth_min, depth_max, i_min, j_min, i_max, j_max, Vstretching, theta_s, theta_b, hc, N, lbound, ubound):

    #read grid and variable at timestep
    id = Dataset(file_path, 'r')
    h = id.variables['h'][:,:]
    zice = id.variables['zice'][:,:]
    mask = id.variables['mask_rho'][:,:]
    var = id.variables[variable]
    data = var[timestep,:,:,:]
    if hasattr(var, 'units'):
        unit=var.units
    else:
        unit='nondimensional'
    name = var.long_name
    id.close()

    #calc 3D field of depth values
    z_3d, sc_r, Cs_r = calc_z(h, zice, theta_s, theta_b, hc, N, None, Vstretching)

    #get a 3D land mask
    mask_3d = tile(mask,(N,1,1))

    #mask out land
    data_3d = ma.masked_where(mask_3d==0,data)

    #simple index array for later plotting
    idx_4d=np.indices(shape(data_3d),int)

    #extract values along this line (from stackoverflow)
    #make a line with num points
    num = int(sqrt(square(i_max-i_min)+square(j_max-j_min)))+1
    x,y=np.linspace(i_min,i_max,num),np.linspace(j_min,j_max,num)

    #extract values of 3d arrays along this line 
    z_2d =z_3d[:,y.astype(np.int),x.astype(np.int)]
    idx_3d =idx_4d[:,:,y.astype(np.int),x.astype(np.int)]
    data_2d =data_3d[:,y.astype(np.int),x.astype(np.int)]

    #convert index value to distance
    dist_2d=sqrt(square(idx_3d[1])+square(idx_3d[2]))

    #contour levels
    #lev=range(1,N)

    #Plot
    fig=figure(figsize=(18,6))
    pcolormesh(dist_2d,z_2d,data_2d,vmin=lbound,vmax=ubound)
    colorbar()
    title(name +" ("+ unit +") at timestep "+str(timestep+1)+" \n along the line "+str([i_min, j_min])+" to "+str([i_max, j_max])+" (grid coords [i,j])", fontsize=24)
    xlabel('Distance (km)')
    ylabel('Depth (m)')
    ylim([depth_min,depth_max])
    #fig.show()
    return fig


# Command-line interface
if __name__ == "__main__":

    file_path = input("Path to file: ")
    file_number = input("File number: ")
    start = int(input("Time step start: "))
    stop= int(input("Time step end: "))
    step= int(input("Time step step: "))
    variable = input("Variable to plot: ")
    bounds = input("Set bounds? (y/n): ")
    if bounds=='y':
        lb = float(input("lower bound: "))
        ub =float(input("upper bound: "))
    else:
        lb = None
        ub = None
    depth_min = -1*float(input("Deepest depth to plot (positive, metres): "))
    depth_max = -1*float(input("Shallowest depth to plot (positive, metres): "))
    i_min = int((input('i start (x_axis): ')))
    j_min = int((input('j start (x-axis): ')))
    i_max = int((input('i end (y-axis): ')))
    j_max = int((input('j end (yaxis): ')))
    Vstretching = 4#int(input("Vstretching (2 or 4): "))
    theta_s = 4.0#float(input("theta_s: "))
    theta_b = 0.9#float(input("theta_b: "))
    hc = 50.0#float(input("hc: "))
    N = 31#int(input("N: "))

    for timestep in range(start-1,stop,step):
        print('processing timestep '+str(timestep+1)+' of '+str(stop))
        try:
            fig = plot_vslice (file_path, timestep, variable, depth_min, depth_max, i_min, j_min, i_max, j_max, Vstretching, theta_s, theta_b, hc, N, lb, ub)
        except:
            print('End of file at timestep: '+str(timestep+1))
            break
        #fig.show()
        figname = variable +"_"+str(i_min)+str(j_min)+"_"+str(i_max)+str(j_max)+"_"+str(file_number)+"_"+str(timestep+1)+".png"
        print('save figure: '+figname)
        fig.savefig(figname, bbox_inches='tight')

    # Keep repeating until the user wants to exit
    while True:
        repeat = input("Make another plot series (y/n)? ")
        if repeat == 'y':
            while True:
                changes = input("Enter a parameter to change: (1) file, (2) time steps, (3) variable, (4) bounds, (5) depth, (6) start or end coordinate; or enter to continue: ")
                if len(changes) == 0:
                    break
                else:
                    if int(changes) == 1:
                        file_path = input("Path to file: ")
                        file_number = input("File number: ")
                    elif int(changes) == 2:
                        start = int(input("Time step start: "))
                        stop= int(input("Time step end: "))
                        step= int(input("Time step step: "))
                    elif int(changes) == 3:
                        variable = input("Variable to plot: ")
                    elif int(changes) == 4:
                        bounds = input("Set bounds? (y/n): ")
                        if bounds=='y':
                            lb = float(input("lower bound: "))
                            ub = float(input("upper bound: "))
                        else:
                            lb = None
                            ub = None
                    elif int(changes) == 5:
                        depth_min = -1*float(input("Deepest depth to plot (positive, metres): "))
                        depth_max = -1*float(input("Shallowest depth to plot (positive, metres): "))
                    elif int(changes) == 6:
                        i_min = int((input('i start (x_axis): ')))
                        j_min = int((input('j start (x-axis): ')))
                        i_max = int((input('i end (y-axis): ')))
                        j_max = int((input('j end (yaxis): ')))
            for timestep in range(start-1,stop,step):
                print('processing timestep '+str(timestep+1)+' of '+str(stop))
                try:
                    fig = plot_vslice (file_path, timestep, variable, depth_min, depth_max, i_min, j_min, i_max, j_max, Vstretching, theta_s, theta_b, hc, N,lb,ub)
                except:
                    print('End of file at timestep: '+str(timestep+1))
                    break
                #fig.show()
                figname = variable +"_"+str(i_min)+str(j_min)+"_"+str(i_max)+str(j_max)+"_"+str(file_number)+"_"+str(timestep+1)+".png"
                print('save figure: '+figname)
                fig.savefig(figname, bbox_inches='tight')
        else:
            break
