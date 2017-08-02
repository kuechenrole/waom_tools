from netCDF4 import Dataset
from numpy import *
from matplotlib.pyplot import *
from cmocean.cm import *

# Make a circumpolar plot of ice shelf melt rates averaged over the last year
# of simulation.
# Input:
# file_path = path to ROMS ocean averages file, containing at least 1 year of
#             5-day averaged output
# save = optional boolean to save the figure to a file, rather than display it
#        on screen
# fig_name = if save=True, filename for figure
def ismr_plot (file_path, save=False, fig_name=None):

    # Read the grid
    id = Dataset(file_path, 'r')
    mask = id.variables['mask_rho'][:,:]
    zice = id.variables['zice'][:,:]
    ismr = mean(id.variables['m'][:,:,:], axis=0)*60*60*24*365
    id.close()

    # Mask the open ocean and land out of the melt rates
    ismr = ma.masked_where(zice==0, ismr)
    ismr = ma.masked_where(mask==0, ismr)

    # Set colour map
    # Values for change points
    #cmap_vals = array([-0.1, 0, 1, 2, 5, 8])
    # Colours for change points
    # (blue, white, yellow-orange, red-orange, dark red, purple)
    #cmap_colors = [(0.26, 0.45, 0.86), (1, 1, 1), (1, 0.9, 0.4), (0.99, 0.59, 0.18), (0.5, 0.0, 0.08), (0.96, 0.17, 0.89)]
    # Map to 0-1
    #cmap_vals_norm = (cmap_vals + 0.1)/(8 + 0.1)
    # Combine into a list
    #cmap_list = []
    #for i in range(size(cmap_vals)):
    #    cmap_list.append((cmap_vals_norm[i], cmap_colors[i]))
    # Make colour map    
    #mf_cmap = LinearSegmentedColormap.from_list('melt_freeze', cmap_list)
    # Set levels
    #lev = linspace(-0.1, 8, num=100)

    # Get land/zice mask
    #open_ocn = copy(mask_rho)
    #open_ocn[zice!=0] = 0
    #land_zice = ma.masked_where(open_ocn==1, open_ocn)

    # Convert grid to spherical coordinates
    #x = -(lat+90)*cos(lon*deg2rad+pi/2)
    #y = (lat+90)*sin(lon*deg2rad+pi/2)
    # Find centre in spherical coordinates
    #x_c = -(lat_c+90)*cos(lon_c*deg2rad+pi/2)
    #y_c = (lat_c+90)*sin(lon_c*deg2rad+pi/2)
    # Build a regular x-y grid and select the missing circle
    #x_reg, y_reg = meshgrid(linspace(-nbdry, nbdry, num=1000), linspace(-nbdry, nbdry, num=1000))
    #land_circle = zeros(shape(x_reg))
    #land_circle = ma.masked_where(sqrt((x_reg-x_c)**2 + (y_reg-y_c)**2) > radius, land_circle)

    # Set up plot
    fig = figure(figsize=(16,12))
    pcolormesh(mask,cmap=gray)
    pcolormesh(ismr,cmap=thermal,vmin=100)
    #ax = fig.add_subplot(1,1,1, aspect='equal')
    #fig.patch.set_facecolor('white')
    # First shade land and zice in grey (include zice so there are no white
    # patches near the grounding line where contours meet)
    #contourf(x, y, land_zice, 1, colors=(('0.6', '0.6', '0.6')))
    # Fill in the missing circle
    #contourf(x_reg, y_reg, land_circle, 1, colors=(('0.6', '0.6', '0.6')))
    # Now shade the melt rate
    #contourf(x, y, ismr, lev, cmap=mf_cmap, extend='both')
    cbar = colorbar()#ticks=arange(0,8+1,1))
    cbar.ax.tick_params(labelsize=20)
    # Add a black contour for the ice shelf front
    #rcParams['contour.negative_linestyle'] = 'solid'
    #contour(x, y, zice, levels=[min_zice], colors=('black'))
    ylim(0, len(mask[:,0]))
    xlim(0, len(mask[0,:]))

    title('Ice shelf melt rate (m/y), annual average', fontsize=30)
    axis('off')

    # Finished
    if save:
        savefig(fig_name)
    else:
        show()

        
# Command-line interface
if __name__ == "__main__":

    file_path = input("Path to ocean averages file, containing at least 1 year of 5-day averages: ")
    action = input("Save figure (s) or display in window (d)? ")
    if action == 's':
        save = True
        fig_name = input("File name for figure: ")
    elif action == 'd':
        save = False
        fig_name = None
    # Make the plot
    ismr_plot(file_path, save, fig_name)
    
