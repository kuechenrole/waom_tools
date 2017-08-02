from netCDF4 import Dataset
from numpy import *
from matplotlib.pyplot import *
from cmocean.cm import *

# Creates a circumpolar Antarctic plot of bathymetry.
# Follows the same process as circumpolar_plot.py, but since h is not
# time-dependent, it requires a special case.
# Input:
# grid_path = path to ROMS grid file
# fig_name = filename for figure
def h_circumpolar (grid_path, fig_name):

    # Read data
    id = Dataset(grid_path, 'r')
    h = id.variables['h'][:,:]
    zice = id.variables['zice'][:,:]
    mask = id.variables['mask_rho'][:,:]
    id.close()

    # calculate watercolumn thickness and mask with land mask
    wc = h + zice
    wc = ma.masked_where(mask==0, wc)

    #lev = linspace(0,amax(wc),num=50)
    #lev = linspace(0,1000,num=50)

    # Plot
    fig = figure(figsize=(16,12))
    pcolormesh(mask,cmap=gray)
    pcolormesh(wc,cmap=deep)
    cbar = colorbar()
    cbar.ax.tick_params(labelsize=20)
    title('Water column thickness (m)', fontsize=30)
    axis('off')
    ylim(0, len(mask[:,0]))
    xlim(0, len(mask[0,:]))


    show()
    #savefig(fig_name)


# Command-line interface
if __name__ == "__main__":

    grid_path = input("Path to ROMS grid file: ")
    fig_name = input("Filename for figure: ")
    h_circumpolar(grid_path, fig_name)    
