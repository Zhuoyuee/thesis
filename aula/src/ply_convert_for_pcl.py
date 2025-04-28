import numpy as np
from plyfile import PlyData
import open3d as o3d

def convert_ply_to_pcd(input_ply, output_pcd):
    # Read PLY using Open3D
    pcd = o3d.io.read_point_cloud(input_ply)
    print(f" Loaded {len(pcd.points)} points")

    # Save as PCD (binary format, PCL-compatible)
    o3d.io.write_point_cloud(output_pcd, pcd, write_ascii=False, compressed=False)
    print(f" Saved to {output_pcd}")

# Example usage
convert_ply_to_pcd(
    "C:/Users/wangz/monastery/phone_scan/HK_pc_phone.ply",
    "C:/Users/wangz/monastery/phone_scan/HK_pc_phone.pcd"
)
