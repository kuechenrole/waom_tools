from netCDF4 import Dataset
from numpy import *
from matplotlib.pyplot import *
from cmocean.cm import *


def velo_mag(his_file,level,fig_name):

    # Read data
    id = Dataset(his_file, 'r')
    u = id.variables['u'][-1,level,:-1,:]
    v = id.variables['v'][-1,level,:,:-1]
    h = id.variables['h'][:-1,:-1]
    zice = id.variables['zice'][:-1,:-1]
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
    #calc watercolumn thickness, wc gradient and magnitude of wc gradient
    wc = h + zice
    wcGrad = gradient(wc)
    magGrad = sqrt(wcGrad[0]**2+wcGrad[1]**2)

    # Mask with land mask
    mag_masked = ma.masked_where(mask==0, mag)
    magGrad_masked = ma.masked_where(mask==0, magGrad)
    # Convert to spherical coordinates
    #x = -(lat+90)*cos(lon*deg2rad+pi/2)
    #y = (lat+90)*sin(lon*deg2rad+pi/2)

    lev = linspace(0,amax(mag_masked),num=10)

    # Plot
    fig = figure(figsize=(16,12))
    #fig.add_subplot(1,1,1, aspect='equal')
    pcolormesh(mask,cmap=gray)
    contour(magGrad,5,colors='k',alpha=0.2)
    pcolormesh(mag_masked,cmap=speed,vmax=5.0)
    cbar = colorbar(ticks=arange(0,amax(mag_masked),0.5))
    cbar.ax.tick_params(labelsize=20)
    title('Velocity magnitude at sigma level '+str(level)+' in (cm/s)', fontsize=30)
    axis('off')
    #tight_layout()
    show()
    fig.savefig(fig_name,bbox_inches='tight',dpi=200)

    
# Command-line interface
if __name__ == "__main__":

    his_file = input("Path to ROMS his file: ")
    level = int(input("sigma level:"))
    fig_name = input("Filename for figure: ")
    velo_mag(his_file,level, fig_name)    
