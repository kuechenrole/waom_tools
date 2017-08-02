from netCDF4 import Dataset
from numpy import *

# Find all of the CICE grid points which are land (or ice shelf) on 3 sides.
# Sea ice can grow in these isolated points but cannot escape due to CICE's
# coastal boundary conditions, so it gets crazy thick (like 2 km thick).
# Print the indices of these points to the screen. This script assumes a
# periodic boundary in the longitude direction.
# Input: cice_kmt_file = path to CICE land mask file, created using cice_grid.py
def find_isolated_points (grd_file):

    # Read land mask
    id = Dataset(grd_file, 'a')
    mask_old = id.variables['mask_rho'][:,:]
    mask_new = mask_old.copy()
    nb_modif=0

    # Double loop, can't find a cleaner way to do this
    for j in range(1,size(mask_old,0)-1):
        for i in range(1,size(mask_old,1)-1):
            # Check for unmasked points
            if mask_old[j,i] == 1:
                neighbours = array([mask_old[j,i-1], mask_old[j,i+1], mask_old[j-1,i], mask_old[j+1,i]])
                # Blocked on at least 3 sides
                if sum(neighbours) < 1:
                    print("i=" + str(i+1) + ', j=' + str(j+1))
                    mask_new[j,i]=0
                    nb_modif+=1
    print("number modified = ", nb_modif)

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
    rmask = asarray(rmask)
    assert rmask.ndim == 2, 'rmask must be a 2D array'
    assert all((rmask==0)|(rmask==1)), 'rmask array must contain only ones and zeros.'

    umask = rmask[:, :-1] * rmask[:, 1:]
    vmask = rmask[:-1, :] * rmask[1:, :]
    pmask = rmask[:-1, :-1] * rmask[:-1, 1:] * rmask[1:, :-1] * rmask[1:, 1:]

    return umask, vmask, pmask

# Command-line interface
if __name__ == "__main__":

    grd_file = input("Path to ROMS grid file: ")
    find_isolated_points(grd_file)
