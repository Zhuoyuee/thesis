import open3d as o3d
import numpy as np
from plyfile import PlyData
import struct


def read_ply(file_path):
    plydata = PlyData.read(file_path)

    # Extract the main element (typically 'vertex')
    vertex = plydata['vertex']

    # Print Metadata
    print("--- Metadata ---")
    print(f"Number of points: {len(vertex)}")
    print(f"Available properties: {vertex.properties}")

    # Identify All Attributes
    attribute_names = vertex.data.dtype.names
    print("\n--- Point Attributes ---")
    print(f"Attributes: {attribute_names}")

    # Print First 10 Points with All Attributes
    print("\n--- First 10 Points ---")
    for i in range(min(10, len(vertex))):
        point = {attr: vertex[i][attr] for attr in attribute_names}
        print(f"Point {i}: {point}")

    # Check for Georeferencing
    print("\n--- Georeferencing Check ---")
    if 'x' in attribute_names and 'y' in attribute_names and 'z' in attribute_names:
        sample_point = vertex[0]
        sample_coords = (sample_point['x'], sample_point['y'], sample_point['z'])
        print(f"Sample Coordinates: {sample_coords}")
        if max(abs(sample_coords)) > 1000:  # Arbitrary threshold
            print("Points likely georeferenced (large coordinate values detected).")
        else:
            print("Points likely in a local coordinate system (small coordinate values).")
    else:
        print("No coordinates found to determine georeferencing.")


def inspect_ply_with_normals_check(file_path):
    print(f"Inspecting PLY file: {file_path}\n")

    # Load the PLY file
    pcd = o3d.io.read_point_cloud(file_path)

    # Check for normals
    if pcd.has_normals():
        normals = np.asarray(pcd.normals)

        print("\n--- Normals Check ---")
        # Use a tolerance to check for near-zero normals
        all_zero_normals = np.all(np.isclose(normals, 0), axis=1)
        if np.all(all_zero_normals):
            print("All normals are zero (or close to zero within tolerance).")
        else:
            print("Some normals are non-zero.")
            print(f"First 10 normals:\n{normals[:10]}")
    else:
        print("No normals found in the PLY file.")

    print("\n--- End of Inspection ---")

# Example usage
inspect_ply_with_normals_check(r"C:\Users\www\Desktop\thesis\Share\AULA.ply")



# Example usage
#read_ply(r"C:\Users\www\Desktop\thesis\Share\AULA.ply")

#Attributes: ('x', 'y', 'z', 'nx', 'ny', 'nz', 'f_dc_0', 'f_dc_1', 'f_dc_2', 'f_rest_0', 'f_rest_1', 'f_rest_2', 'f_rest_3', 'f_rest_4', 'f_rest_5', 'f_rest_6', 'f_rest_7', 'f_rest_8', 'f_rest_9', 'f_rest_10', 'f_rest_11', 'f_rest_12', 'f_rest_13', 'f_rest_14', 'f_rest_15', 'f_rest_16', 'f_rest_17', 'f_rest_18', 'f_rest_19', 'f_rest_20', 'f_rest_21', 'f_rest_22', 'f_rest_23', 'f_rest_24', 'f_rest_25', 'f_rest_26', 'f_rest_27', 'f_rest_28', 'f_rest_29', 'f_rest_30', 'f_rest_31', 'f_rest_32', 'f_rest_33', 'f_rest_34', 'f_rest_35', 'f_rest_36', 'f_rest_37', 'f_rest_38', 'f_rest_39', 'f_rest_40', 'f_rest_41', 'f_rest_42', 'f_rest_43', 'f_rest_44', 'opacity', 'scale_0', 'scale_1', 'scale_2', 'rot_0', 'rot_1', 'rot_2', 'rot_3')
