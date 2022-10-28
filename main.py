import pprint
import open3d as o3d
import numpy as np
import os
import random
from copy import copy
import time
from remove_ground_and_dron import *
from pcdIO import *



if __name__ == "__main__":
    #pcd = load_pcd("/home/terda93/git/slam_datasets/forest/bagfiles/my_forest4/1651738515.007457803.pcd")
    #pcd = load_pcd("/home/terda93/git/slam_datasets/forest/bagfiles/my_forest4/1651738552.829550165.pcd")
    pcd = load_pcd("/home/terda93/git/slam_datasets/forest/bagfiles/my_forest4/1651738522.626975236.pcd")
    pcd_test = copy(pcd)
    pcd_test2 = copy(pcd)
    print(pcd)
    pcd_test.points = prepare_points(np.zeros((1, 3),dtype=np.float64))
    points = pcd_to_array(pcd)
    print(points)
    distance = np.asarray(pcd.compute_point_cloud_distance(pcd_test))
    
    points = remove_dron(points, distance)
    
    pcd.points = prepare_points(points)
    print(pcd)
    
    
    
    start_time = time.time()

    grid = make_grid1(points)
    ground_points = label_ground_points(grid)
    points = remove_ground(points, ground_points)
    pcd.points = prepare_points(points)
    print(np.shape(points))
    to_delete = np.zeros((1,3))
    sum = 0
    
    print(np.min(points[:, 2]),np.max(points[:, 2]))
    possible_ground = points[points[:,2] < 0]
    #mean = np.mean(possible_ground)
    #possible_ground = possible_ground[possible_ground[:,2] < mean]
    print(np.shape(possible_ground))

    
    for i in range(np.shape(possible_ground)[0]):
        #print(points[i,:])
        pcd_test.points = o3d.utility.Vector3dVector([possible_ground[i, :]])
        #print(np.asarray(pcd_test.points))
        point_distances = np.asarray(pcd.compute_point_cloud_distance(pcd_test))
        pred = np.shape(point_distances)[0]
        point_distances = point_distances[point_distances > 0.5]
        po = np.shape(point_distances)[0]
        if (pred - po) < 6:
            #print(pred,po)
            sum +=1
            to_delete = np.append(to_delete, [possible_ground[i,:]], axis = 0)
    

    #grid1 = make_grid1(points)
    #ground_points1 = label_ground_points1(grid1)

    #colors = np.zeros((np.shape(points)[0], np.shape(points)[1]),dtype=np.float64)
    #colors[:] = [255,255,0]
    #mask = np.isin(points,to_delete)
    #colors[np.where(mask == [True,True,True])[0]] = [0,0,255]
    #pcd.colors = prepare_colors(colors)

    points = remove_ground(points, to_delete)
    pcd.points = prepare_points(points)
    print(sum)

    save_pcd("ground6.pcd", pcd)
    print("--- %s seconds ---" % (time.time() - start_time)
