from sys import argv
from netCDF4 import Dataset
from numpy import *
from matplotlib.pyplot import *
from cmocean.cm import *


def velo_mag(his_file,level):

    # Read data
    id = Dataset(his_file, 'r')
    u = id.variables['u'][-1,-1,-1,:-1,:]
    v = id.variables['v'][-1,-1,-1,:,:-1]
    lon = id.variables['lon_rho'][:,:]
    lat = id.variables['lat_rho'][:,:]
    mask = id.variables['mask_rho'][:-1,:-1]
    id.close()

    #calc magnitude
    u2 = square(u)
    v2 = square(v)

    mag = sqrt(u2+v2)

    #convert to from m/s to cm/s
    mag = mag*100

    # Mask with land mask
    mag_masked = ma.masked_where(mask==0, mag)

    # Convert to spherical coordinates
    #x = -(lat+90)*cos(lon*deg2rad+pi/2)
    #y = (lat+90)*sin(lon*deg2rad+pi/2)

    lev = linspace(0,amax(mag_masked),num=10)

    # Plot
    fig = figure(figsize=(16,14))
    #fig.add_subplot(1,1,1, aspect='equal')
    pcolormesh(mask,cmap=gray)
    pcolormesh(mag_masked,cmap=speed)
    cbar = colorbar()
    cbar.ax.tick_params(labelsize=20)
    title('Velocity magnitude at sigma level '+str(level)+' in (cm/s)', fontsize=30)
    ylim(0, len(mask[:,0]))
    xlim(0, len(mask[0,:]))
    axis('off')
    #tight_layout()
    show()
    #fig.savefig(fig_name,bbox_inches='tight',dpi=200)
    
# Command-line interface
if __name__ == "__main__":

    his_file = argv[1]
    level = int(argv[2])
    velo_mag(his_file,level)    
