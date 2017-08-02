import numpy as np
from netCDF4 import Dataset

def remove_ice(grid_file,box):
    
    id = Dataset(grid_file,'a')
    h = id.variables['h'][:,:]
    zice = id.variables['zice'][:,:]
    retZice=zice.copy() 
    nbModif = 0

    [imin,jmin,imax,jmax]=box
    imax=imax+1
    jmax=jmax+1

    for iEta in range(jmin,jmax):
        for iXi in range(imin,imax):
           retZice[iEta,iXi]=0.0
           nbModif += 1

    print('     nbModif=', nbModif)
        
    id.variables['zice'][:,:]= retZice
    id.close()# Command-line interface
if __name__ == "__main__":

    grid_file='../waom10Grids/waom10_MinDepth20m_rx10.3_SmoothDeep0.2_KillIce.nc'
    box1=[351,17,390,37]
    box2=[60,490,80,507]
    box3=[31,402,44,458]
    box4=[565,257,569,262]
    
    boxes=[box1,box2,box3,box4]
    for box in boxes:
        remove_ice(grid_file,box)
