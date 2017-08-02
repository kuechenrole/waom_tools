from netCDF4 import Dataset
from sys import argv
from numpy import *
from calc_z import *

# Calculates the spacial distribution of rx1 from given ROMS
# grid file and s-coordinate controling parameters amd saves the rx1 field
# to a netCDF file
# Usage:
# python calc_rx1.py grid_path theta_s theta_b hc N Vstretching(2 or 4) out_file
# 
# Origin: Kaitlin Naughten

def calc_rx1 (grid_path, theta_s, theta_b, hc, N, Vstretching, out_file):

    # read grid variables
    id = Dataset(grid_path, 'r')
    lon_2d = id.variables['lon_rho'][:,:]
    lat_2d = id.variables['lat_rho'][:,:]
    h = id.variables['h'][:,:]
    zice = id.variables['zice'][:,:]
    mask_rho = id.variables['mask_rho'][:,:]
    id.close()

    # calculate s-level depth and stretching curves
    z, sc_r, Cs_r = calc_z(h, zice, theta_s, theta_b, hc, N, None, Vstretching)
    for k in range(N):
        tmp = z[k,:,:]
        tmp[mask_rho==0] = NaN
        z[k,:,:] = tmp

    rx1_3d_i = abs((z[1:,1:,1:]-z[1:,1:,:-1]+z[:-1,1:,1:]-z[:-1,1:,:-1])/(z[1:,1:,1:]+z[1:,1:,:-1]-z[:-1,1:,1:]-z[:-1,1:,:-1]))
    rx1_3d_j = abs((z[1:,1:,1:]-z[1:,:-1,1:]+z[:-1,1:,1:]-z[:-1,:-1,1:])/(z[1:,1:,1:]+z[1:,:-1,1:]-z[:-1,1:,1:]-z[:-1,:-1,1:]))
    rx1_3d = maximum(rx1_3d_i, rx1_3d_j)
    rx1_tmp = amax(rx1_3d, axis=0)

    rx1 = zeros(shape(lon_2d))
    rx1[1:,1:] = rx1_tmp
    rx1[0,:] = rx1[1,:]
    rx1[:,0] = rx1[:,1]
    rx1 = ma.masked_where(isnan(rx1), rx1)

    id = Dataset(out_file, 'w')
    id.createDimension('xi_rho', size(lon_2d,1))
    id.createDimension('eta_rho', size(lon_2d,0))
    id.createVariable('rx1', 'f8', ('eta_rho', 'xi_rho'))
    id.variables['rx1'][:,:] = rx1
    id.close()

def main():

    script=argv[0]
    
    grid_path = argv[1]
    theta_s = float(argv[2])
    theta_b = float(argv[3])
    hc = float(argv[4])
    N = int(argv[5])
    Vstretching = int(argv[6])
    out_file = argv[7]

    calc_rx1 (grid_path, theta_s, theta_b, hc, N, Vstretching, out_file)
    
if __name__ == "__main__":
    
    main()

