from numpy import *

# Given ROMS grid variables, calculate Cartesian integrands dx and dy.
# Input:
# lon, lat = 2D arrays containing values for latitude and longitude, with
#            dimension latitude x longitude
# Output:
# dx, dy = 2D arrays (dimension latitude x longitude) containing Cartesian
#          integrands
def cartesian_grid_2d (lon_u, lat_u, lon_v, lat_v):

    # Radius of the Earth in metres
    r = 6.371e6
    # Degrees to radians conversion factor
    deg2rad = pi/180.0

    dx=empty([530,630])
    dy=empty([530,630])
    #index = lon_u<0.0
    #lon_u[index]+=360

    #index = lon_v<0.0
    #lon_v[index]+=360

    # Harversine distance following http://www.movable-type.co.uk/scripts/latlong.html
    phi1=lat_u[1:-1,:-1]*deg2rad
    phi2=lat_u[1:-1,1:]*deg2rad
    lambda1=lon_u[1:-1,:-1]*deg2rad
    lambda2=lon_u[1:-1,1:]*deg2rad
    a = sin((phi2-phi1)/2) * sin((phi2-phi1)/2) + cos(phi1) * cos(phi2) * sin((lambda2-lambda1)/2) * sin((lambda2-lambda1)/2)
    c = 2 * arctan2(sqrt(a), sqrt(1-a))
    dx_tmp = r * c

    phi1=lat_v[:-1,1:-1]*deg2rad
    phi2=lat_v[1:,1:-1]*deg2rad
    lambda1=lon_v[:-1,1:-1]*deg2rad
    lambda2=lon_v[1:,1:-1]*deg2rad
    a = sin((phi2-phi1)/2) * sin((phi2-phi1)/2) + cos(phi1) * cos(phi2) * sin((lambda2-lambda1)/2) * sin((lambda2-lambda1)/2)
    c = 2 * arctan2(sqrt(a), sqrt(1-a))
    dy_tmp = r * c

    dx[1:-1,1:-1]=dx_tmp
    dx[0,:]=dx[1,:]
    dx[-1,:]=dx[-2,:]
    dx[:,0]=dx[:,1]
    dx[:,-1]=dx[:,-2]
    dy[1:-1,1:-1]=dy_tmp
    dy[0,:]=dy[1,:]
    dy[-1,:]=dy[-2,:]
    dy[:,0]=dy[:,1]
    dy[:,-1]=dy[:,-2]
    return dx, dy
