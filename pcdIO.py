import open3d as o3d
import numpy as np


def load_pcd(path):
    pcd = o3d.io.read_point_cloud(path)
    return pcd

def save_pcd(name,pcd):
    o3d.io.write_point_cloud(name, pcd)

def pcd_to_array(pcd):
    return np.asarray(pcd.points)

def prepare_colors(colors):
    return o3d.utility.Vector3dVector(colors)

def prepare_points(points):
    return o3d.utility.Vector3dVector(points)