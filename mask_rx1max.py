import numpy as np
from netCDF4 import Dataset

def mask_rx1(grid_file,rx1_file,rx1_max):
    
    id = Dataset(rx1_file,'r')
    rx1 = id.variables['rx1'][:,:]
    id.close()

    id = Dataset(grid_file,'a')
    mask_old = id.variables['mask_rho'][:,:]
    mask_new = mask_old.copy()
    nbModif = 0

#    for point in np.nditer(mask_old,op_flags=['readwrite']):
#        if rx1[point.index]>rx1_max:
#            point[...]=1
    for iEta in range(np.size(mask_old,0)):
        for iXi in range(np.size(mask_old,1)):
            if (rx1[iEta,iXi]>rx1_max):
                mask_new[iEta,iXi] = 0
                nbModif += 1

    print('     nbModif=', nbModif)
        
    id.variables['mask_rho'][:,:]= mask_new
    id.close()# Command-line interface
if __name__ == "__main__":

    grid_file='/home/ubuntu/bigStick/waom10Grids/sledge_grd.nc'
    rx1_file='/home/ubuntu/bigStick/waom10Grids/rx1Smooth.nc'
    rx1_max = 70.0

    mask_rx1(grid_file,rx1_file,rx1_max) 
