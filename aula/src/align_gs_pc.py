import numpy as np
import pdal
import json
import numpy as np
import open3d as o3d


def compute_similarity_transformation_matrix(source_points, target_points):
    """
    Computes a similarity transformation matrix (scale + rotation + translation)
    to align source_points to target_points.

    Parameters:
    - source_points: np.array of shape (N,3)
    - target_points: np.array of shape (N,3)

    Returns:
    - PDAL-compatible 4x4 transformation matrix as a string
    """
    # Ensure numpy arrays
    source_points = np.asarray(source_points)
    target_points = np.asarray(target_points)

    # Compute centroids
    centroid_source = np.mean(source_points, axis=0)
    centroid_target = np.mean(target_points, axis=0)

    # Center the points
    P = source_points - centroid_source
    Q = target_points - centroid_target

    # Compute scaling factor
    norm_P = np.linalg.norm(P)
    norm_Q = np.linalg.norm(Q)
    scale = norm_Q / norm_P

    # Normalize P to have same scale as Q
    P_scaled = P * scale

    # Compute covariance matrix and SVD
    H = np.dot(P_scaled.T, Q)
    U, _, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # Correct for reflection
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = np.dot(Vt.T, U.T)

    # Compute translation
    t = centroid_target - np.dot(R, centroid_source * scale)

    # Build transformation matrix
    T = np.eye(4)
    T[:3, :3] = R * scale
    T[:3, 3] = t

    print("Computed Similarity Transformation Matrix:")
    print(T)

    # Format for PDAL
    return " ".join(map(str, T.flatten()))


from plyfile import PlyData, PlyElement
import numpy as np

def transform_gs_ply(input_file, output_file, matrix_str):
    """
    Transforms a Gaussian Splatting PLY file's coordinates while preserving all attributes.

    Parameters:
    - input_file: str, path to input .ply file
    - output_file: str, path to save transformed .ply
    - matrix_str: str, space-separated 4x4 transformation matrix
    """
    # Load transformation matrix
    matrix = np.fromstring(matrix_str, sep=' ').reshape((4, 4))

    # Read binary PLY with full attribute preservation
    ply = PlyData.read(input_file)
    vertex_data = ply['vertex'].data

    # Extract positions
    xyz = np.vstack([
        vertex_data['x'],
        vertex_data['y'],
        vertex_data['z'],
        np.ones(len(vertex_data))
    ])
    xyz_transformed = (matrix @ xyz)[:3].T

    # Copy original structured dtype and data
    new_vertices = np.empty(len(vertex_data), dtype=vertex_data.dtype)
    for name in vertex_data.dtype.names:
        new_vertices[name] = vertex_data[name]

    # Overwrite with transformed coordinates
    new_vertices['x'] = xyz_transformed[:, 0]
    new_vertices['y'] = xyz_transformed[:, 1]
    new_vertices['z'] = xyz_transformed[:, 2]

    # Save transformed point cloud, keeping binary format
    ply_out = PlyData([PlyElement.describe(new_vertices, 'vertex')], text=False)
    ply_out.write(output_file)

    print(f"Transformed GS .ply written to: {output_file}")


# if __name__ == "__main__":
#     source_points = np.array([
#         [-0.179246, -1.065793, 0.345715],  # A0
#         [1.980688, -1.115461, -0.357990],  # A1
#         [-0.369958, -0.506035, -0.361615],  # A2
#         [1.759537, -0.560766, -1.036584],  # A3
#         [0.158718, 0.167094, 1.221129],  # A4
#         [2.310064, 0.126198, 0.496316],  # A5
#     ])
#     target_points = np.array([
#         [0.042054, -0.374241, 1.231021],  # R0
#         [0.105754, 0.416942, 1.190727],  # R1
#         [0.315074, -0.389426, 1.047637],  # R2
#         [0.367187, 0.374009, 1.026431],  # R3
#         [-0.246731, -0.358255, 0.792702],  # R4
#         [-0.163694, 0.441966, 0.783128],  # R5
#     ])
#     input_file = r"C:\Users\wangz\Documents\HK_GS/HK_GS_clip_by_bbx.ply"
#     output_file = r"C:\Users\wangz\Documents\HK_GS/HK_GS_aligned_with_attr.ply"
#     pdal_matrix = compute_similarity_transformation_matrix(source_points, target_points)
#     transform_gs_ply(input_file, output_file, pdal_matrix)

if __name__ == "__main__":
    source_points = np.array([
        [0.042054, -0.374241, 1.231021],  # R0
        [0.105754, 0.416942, 1.190727],  # R1
        [0.315074, -0.389426, 1.047637],  # R2
        [0.367187, 0.374009, 1.026431],  # R3
        [-0.246731, -0.358255, 0.792702],  # R4
        [-0.163694, 0.441966, 0.783128],

    ])
    target_points = np.array([
        [-0.179246, -1.065793, 0.345715],  # A0
        [1.980688, -1.115461, -0.357990],  # A1
        [-0.369958, -0.506035, -0.361615],  # A2
        [1.759537, -0.560766, -1.036584],  # A3
        [0.158718, 0.167094, 1.221129],  # A4
        [2.310064, 0.126198, 0.496316],  # A5
    ])
    input_file = r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\HK_id_refined.ply"
    output_file = r"C:\Users\wangz\Documents\HK_GS/HK_pc_aligned.ply"
    pdal_matrix = compute_similarity_transformation_matrix(source_points, target_points)
    transform_gs_ply(input_file, output_file, pdal_matrix)
