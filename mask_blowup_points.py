import numpy as np
from netCDF4 import Dataset

def mask_box(grid_file,box):
    
    id = Dataset(grid_file,'a')
    zice = id.variables['zice'][:,:]
    mask_old = id.variables['mask_rho'][:,:]
    mask_new = mask_old.copy()
    nbModif = 0

    [imin,jmin,imax,jmax]=box
    imax=imax+1
    jmax=jmax+1

    for iEta in range(jmin,jmax):
        for iXi in range(imin,imax):
            if (mask_old[iEta,iXi]==1 and zice[iEta,iXi]<0.0):
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

    grid_file='/home/ubuntu/bigStick/waom10Grids/waom10_MinDepth50m_SmoothDeep0.2_box.nc'

    box1=[351,17,390,37]
    box2=[60,490,80,507]
    box3=[37,432,37,432]
    box4=[40,458,40,458]
    box5=[565,257,569,262]

    boxes=[box1,box2,box3,box4,box5]
    for box in boxes:
        mask_box(grid_file,box)

