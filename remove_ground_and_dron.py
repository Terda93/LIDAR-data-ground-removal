import numpy as np

GRID_BOX_SIZE = 1.8
TRESHOLD = 0.45


def make_grid(points):
    '''

    :param 
        points : Nx3 ndarray of points
    :return: points devided to grid, NxMx3 ndarray

    '''
    x_max = int(np.ceil((np.abs(np.max(points[:,0]))))/GRID_BOX_SIZE)
    y_max = int(np.ceil((np.abs(np.max(points[:,1]))))/GRID_BOX_SIZE)
    x_min = int(np.ceil((np.abs(np.min(points[:,0]))))/GRID_BOX_SIZE)
    y_min = int(np.ceil((np.abs(np.min(points[:,1]))))/GRID_BOX_SIZE)
    x_size = x_min + x_max
    y_size = y_min + y_max
    x = points[:,0]
    y = points[:,1]
    grid = np.zeros((int(x_size*y_size), np.shape(points)[0], 3))
    for i in range(x_size):
        for j in range(y_size): 
            x_test = np.where(x < (i - x_min))
            y_test = np.where(y < (j-y_min))
            common = np.intersect1d(x_test, y_test)
            shape = np.shape(common)
            grid[i*x_size + (j+y_min), :shape[0], :] = points[common]
    sums = np.sum(np.sum(grid, axis = 2), axis = 1)
    grid = np.delete(grid, np.where(sums == 0)[0], axis=0)
    return grid

def make_grid1(points):
    '''

    :param 
        points : Nx3 ndarray of points
    :return: points devided to grid, NxMx3 ndarray

    '''
    x_max = int(np.ceil((np.abs(np.max(points[:,0]))))/GRID_BOX_SIZE)
    y_max = int(np.ceil((np.abs(np.max(points[:,1]))))/GRID_BOX_SIZE)
    x_min = int(np.ceil((np.abs(np.min(points[:,0]))))/GRID_BOX_SIZE)
    y_min = int(np.ceil((np.abs(np.min(points[:,1]))))/GRID_BOX_SIZE)
    x_size = x_min + x_max
    y_size = y_min + y_max
    x = points[:,0]
    y = points[:,1]
    grid = np.zeros((int(x_size*y_size), np.shape(points)[0], 3))
    #print(x_size,y_size)
    #print(y_min)
    for i in range(x_size):
        for j in range(y_size): 
            x_test1 = np.where(x < (GRID_BOX_SIZE*i - x_min))
            x_test2 = np.where(x >= (GRID_BOX_SIZE*(i-1) - x_min))
            #x_test = np.where(x < (i - x_min))
            y_test1 = np.where(y < (GRID_BOX_SIZE*j-y_min))
            y_test2 = np.where(y >= (GRID_BOX_SIZE*(j-1)-y_min))
            x_test = np.intersect1d(x_test1,x_test2)
            y_test = np.intersect1d(y_test1,y_test2)
            common = np.intersect1d(x_test, y_test)
            shape = np.shape(common)
            #print(shape[0])
            grid[i*y_size + j, :shape[0], :] = points[common]
    sums = np.sum(np.sum(grid, axis = 2), axis = 1)
    grid = np.delete(grid, np.where(sums == 0)[0], axis=0)
    return grid


def label_ground_points(grid):
    '''

    :param 
        points : points devided to grid, NxMx3 ndarray
    :return: points labeled as ground,  Nx3 ndarray

    '''
    ground_pts = np.zeros((1,3))
    grid_shape = np.shape(grid)
    for i in range(grid_shape[0]):
        all_points = grid[i, :,:]
        #print(np.shape(all_points))
        real_points = np.delete(all_points, np.where(all_points == [0,0,0]), axis=0)
        if(np.shape(real_points)[0] == 0):
            continue
        min_point = np.min(real_points[:, 2])
        ground_points = real_points[np.where(real_points[:,2] < (min_point+TRESHOLD))]
        ground_pts = np.append(ground_pts, ground_points, axis = 0)
        ground_pts = np.unique(ground_pts, axis = 0)
    return ground_pts


def remove_dron(points, distance):
    '''

    :param 
        points : Nx3 ndarray of points
        distances: Nx1 ndarray of points distances from [0,0,0]

    :return: points without dron points

    '''
    distance_not_zero_idx = np.where(distance != 0)
    distance_not_zero = distance[distance_not_zero_idx]
    distance_smaller_than = np.where(distance_not_zero >= 0.35)
    points_without_zero = points[np.where(distance!=0)[0]]
    points = points_without_zero[distance_smaller_than]
    return points

def remove_ground(points, ground):
    mask = np.isin(points,ground)
    points = np.delete(points, np.where(mask == [True,True,True])[0], axis=0)
    return points