import numpy as np
from netCDF4 import Dataset

def mask_shallow(grid_file,max_depth):
    
    id = Dataset(grid_file,'a')
    h = id.variables['h'][:,:]
    zice = id.variables['zice'][:,:]

    mask_old = id.variables['mask_rho'][:,:]
    mask_new = mask_old.copy()
    nbModif = 0
  # calculate watercolumn thickness and mask with land mask
    wc = h + zice


#    for point in np.nditer(mask_old,op_flags=['readwrite']):
#        if rx1[point.index]>rx1_max:
#            point[...]=1
    for iEta in range(np.size(mask_old,0)):
        for iXi in range(np.size(mask_old,1)):
            if (mask_old[iEta,iXi]==1 and wc[iEta,iXi]<max_depth):
                mask_new[iEta,iXi] = 0
                nbModif += 1

    print('     nbModif=', nbModif)


    umask,vmask,pmask=uvp_masks(mask_new)

    id.variables['mask_rho'][:,:]= mask_new
    id.variables['mask_u'][:,:]= umask
    id.variables['mask_v'][:,:]= vmask
    id.variables['mask_psi'][:,:]= pmask
        
    id.close()

def uvp_masks(rmask):
    '''
    return u-, v-, and psi-masks based on input rho-mask
    
    Parameters
    ----------
    
    rmask : ndarray
        mask at CGrid rho-points
    
    Returns
    -------
    (umask, vmask, pmask) : ndarrays
        masks at u-, v-, and psi-points
    '''
    rmask = np.asarray(rmask)
    assert rmask.ndim == 2, 'rmask must be a 2D array'
    assert np.all((rmask==0)|(rmask==1)), 'rmask array must contain only ones and zeros.'

    umask = rmask[:, :-1] * rmask[:, 1:]
    vmask = rmask[:-1, :] * rmask[1:, :]
    pmask = rmask[:-1, :-1] * rmask[:-1, 1:] * rmask[1:, :-1] * rmask[1:, 1:]

    return umask, vmask, pmask


# Command-line interface
if __name__ == "__main__":

    grid_file='/home/ubuntu/bigStick/waom10Grids/waom10_MinDepth50m_rx10.3_SmoothDeep0.2_Sponge.nc'
    max_depth = 50.0

    mask_shallow(grid_file,max_depth)
