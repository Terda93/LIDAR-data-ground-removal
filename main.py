import pprint
import open3d as o3d
import numpy as np
import pcl
from pypcd import pypcd
import os
import random
from BartekVojta.ground_removal_kitti import *
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
    print("--- %s seconds ---" % (time.time() - start_time))
    #print(real_points)
    #print(np.shape(real_points))

        #min = np.min(grid[i,])      

    #print(grid)
    #print(points[np.where(depth==0)[0]])
    '''
    start_time = time.time()
    test = remove_ground(points)
    print(np.shape(test))
    #help =  np.setdiff1d(points,test)
    colors = np.zeros((np.shape(points)[0], np.shape(points)[1]),dtype=np.float64)
    colors[:] = [255,255,0]
    
    mask = np.isin(points,test)
    
    #help = np.where(mask != [True,True,True], points,[0,0,0])
    colors[np.where(mask == [True,True,True])[0]] = [0,255,0]
    #print(depth.tolist())
    #print(np.shape(depth))
    #points = np.delete(points, np.where(depth != 0)[0], axis=0)
    #points = points[np.where(depth!=0)[0]]
    
    
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.io.write_point_cloud("test.pcd", pcd)
    print("--- %s seconds ---" % (time.time() - start_time))
    '''
    '''
    #print(points.tolist())
    #sortedArr = points[points[:,0].argsort()]
    #sortedArr = sortedArr[sortedArr[:,1].argsort()]
    '''
    '''
    colors = np.zeros((np.shape(points)[0], np.shape(points)[1]),dtype=np.float64)
    colors[:] = [255,120,120]
    colors[outl] = [0,255,0]
    colors[inl] = [0,255,0]
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.io.write_point_cloud("colors.pcd", pcd)
    '''
    #print("succed_f")
    #print(points[0])
    #print(np.asarray(pcd.points))
    #o3d.visualization.draw_geometries([pcd])
    #o3d.io.write_point_cloud("colors.pcd", pcd)
    #pc_data = pcd_test.pc_data
    #print(pcd_test.fields)
    #print(pc_data['x'])
    #pc_data['a']
    #print(pc_data)
    #print(type(pc_data))
    #print(np.shape(pc_data['x']))
    #pc_data['a'] = np.ndarray((np.shape(pc_data['x'])[0],3))
    #print(pc_data['x'])
    #print(type(pc_data['ring']))
    #print("succed")

    #print(np.asarray(pcd_test.point))
    #print(pcd)
    #points = np.asarray(pcd.points)
    #print("succed")
    #print(np.shape(points))
    #colors = np.zeros((np.shape(points)[0], np.shape(points)[1]),dtype=np.float64)
    #print("succed")
    #colors[:90000] = [0,255,0]
    #print("succed")
    #colors[90000:] = [255,255,0]
    #print("succed")
    #pcd.colors = o3d.utility.Vector3dVector(colors)
    #print("succed_f")
    #print(points[0])
    #print(np.asarray(pcd.points))
    #o3d.visualization.draw_geometries([pcd])
    #o3d.io.write_point_cloud("colors.pcd", pcd)
    '''
    pc = pypcd.PointCloud.from_path("/home/terda93/git/slam_datasets/forest/bagfiles/my_forest4/1651738515.007457803.pcd")
    pprint.pprint(pc.get_metadata())
    print(np.shape(pc.pc_data['x']))
    points = np.zeros((np.shape(pc.pc_data['x'])[0], 3))
    points[:, 0] = pc.pc_data['x']
    points[:,1] = pc.pc_data['y']
    points[:,2] = pc.pc_data['z']
    print(points)
    #pprint.pprint(pc.pc_data)
    '''
    #print(pc.fields)
    #pc_data = pc.pc_data
    #print(pc_data['intensity'])
    #scan = np.fromfile("/home/terda93/git/slam_datasets/forest/bagfiles/my_forest4/1651738515.007457803.pcd")
    #print(np.shape(scan))

    #pcd = PointCloud()
    #pcd.points = Vector3dVector(np_points)
    #pcd.colors = Vector3dVector(np_colors)