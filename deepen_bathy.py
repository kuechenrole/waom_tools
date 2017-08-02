import numpy as np
from netCDF4 import Dataset

def deepen_bathy(grid_file,min_depth):
    
    id = Dataset(grid_file,'a')
    h_old = id.variables['h'][:,:]
    zice = id.variables['zice'][:,:]
    mask = id.variables['mask_rho'][:,:]
    nbModif = 0
  # calculate watercolumn thickness and mask with land mask
    wc = h_old + zice
    h_new=h_old.copy()
    for iEta in range(np.size(h_old,0)):
        for iXi in range(np.size(h_old,1)):
            if (mask[iEta,iXi]==1 and wc[iEta,iXi]<min_depth):
                h_new[iEta,iXi] = h_old[iEta,iXi] + (min_depth - wc[iEta,iXi])
                nbModif += 1

    print('     nbModif=', nbModif)

    id.variables['h'][:,:]= h_new
        
    id.close()


# Command-line interface
if __name__ == "__main__":

    grid_file='/home/ubuntu/bigStick/waom10Grids/waom10_MinDepth50m_SmoothDeep0.2.nc'
    min_depth = 50.0

    deepen_bathy(grid_file,min_depth)
