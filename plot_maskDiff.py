from netCDF4 import Dataset
from numpy import *
from matplotlib.pyplot import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cmocean.cm import *
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
def h_circumpolar(gridfile,gridfile_smooth,fig_name):

    # Read data
    id = Dataset(gridfile, 'r')
    mask_old = id.variables['mask_rho'][1:-1,1:-1]
    id.close()

    # Read data
    id = Dataset(gridfile_smooth, 'r')
    mask_new = id.variables['mask_rho'][1:-1,1:-1]
    id.close()

    #calh difference
    mask_diff=ma.masked_where(mask_old==0,mask_new-mask_old)
    #lev = linspace(0,amax(data),num=50)

    # Plot
    fig = figure(figsize=(16,12))
    #fig.add_subplot(1,1,1, aspect='equal')
    pcolormesh(-mask_old,cmap=gray)
    pcolormesh(mask_diff)
    #pcolormesh(h_masked,cmap=deep,vmin=0,vmax=1800)
    #cbar = colorbar(ticks=arange(0,1900,100))
    #cbar.ax.tick_params(labelsize=20)
    title('mask_new- mask_old', fontsize=30)
    axis('off')
    ylim(0, len(mask_old[:,0]))
    xlim(0, len(mask_old[0,:]))

    #tight_layout()
    show()
    fig.savefig(fig_name,bbox_inches='tight',dpi=200)

# Command-line interface
if __name__ == "__main__":

    grid_path = input("Path to ROMS grid file: ")
    grid_path_smooth = input("Path to ROMS grid file masked: ")
    fig_name = input("Filename for figure: ")
    h_circumpolar(grid_path, grid_path_smooth, fig_name)    
