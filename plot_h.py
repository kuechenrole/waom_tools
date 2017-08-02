from netCDF4 import Dataset
from numpy import *
from matplotlib.pyplot import *
from cmocean.cm import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
# Creates a circumpolar Antarctic plot of bathymetry.
# Follows the same process as circumpolar_plot.py, but since h is not
# time-dependent, it requires a special case.
# Input:
# grid_path = path to ROMS grid file
# fig_name = filename for figure
# Grid parameters
#theta_s = 4.0
#theta_b = 0.9
#hc = 20
#N = 31
def h_circumpolar(gridfile,fig_name):
    deg2rad = pi/180

    # Read data
    id = Dataset(gridfile, 'r')
    data = id.variables['h'][1:-1,1:-1]
    mask = id.variables['mask_rho'][1:-1,1:-1]
    id.close()

    # Mask with land mask
    h_masked = ma.masked_where(mask==0, data)

    # Convert to spherical coordinates
    #x = -(lat+90)*cos(lon*deg2rad+pi/2)
    #y = (lat+90)*sin(lon*deg2rad+pi/2)

    #lev = linspace(0,amax(data),num=50)

    # Plot
    fig = figure(figsize=(16,12))
    #fig.add_subplot(1,1,1, aspect='equal')
    pcolormesh(mask,cmap=gray)
    pcolormesh(h_masked,cmap=deep,vmin=0,vmax=6000)
    cbar = colorbar(ticks=arange(0,6500,500))
    cbar.ax.tick_params(labelsize=20)
    title('Bathymetry (m)', fontsize=30)
    axis('off')
    ylim(0, len(mask[:,0]))
    xlim(0, len(mask[0,:]))

    #tight_layout()
    show()
    fig.savefig(fig_name,bbox_inches='tight',dpi=200)

# Command-line interface
if __name__ == "__main__":

    grid_path = input("Path to ROMS grid file: ")
    fig_name = input("Filename for figure: ")
    h_circumpolar(grid_path, fig_name)    
