import numpy as np
import pandas as pd
from plyfile import PlyData, PlyElement
from sklearn.neighbors import KDTree

def assign_patch_id_from_neighbors(input_ply_path, output_ply_path, leftover_id=11):
    # Load PLY
    ply_data = PlyData.read(input_ply_path)
    vertex_data = ply_data['vertex'].data
    df = pd.DataFrame(vertex_data)

    # Separate coordinates and IDs
    coords = df[['x', 'y', 'z']].to_numpy()
    patch_ids = df['patch_id'].to_numpy()

    # Find leftovers and labeled sets
    leftover_mask = patch_ids == leftover_id
    labeled_mask = patch_ids != leftover_id

    leftover_coords = coords[leftover_mask]
    labeled_coords = coords[labeled_mask]
    labeled_ids = patch_ids[labeled_mask]

    # Build KDTree and query nearest patch_id
    tree = KDTree(labeled_coords)
    _, indices = tree.query(leftover_coords, k=1)
    nearest_patch_ids = labeled_ids[indices[:, 0]]

    # Replace leftover patch_ids with nearest neighbor's patch_id
    patch_ids[leftover_mask] = nearest_patch_ids
    df['patch_id'] = patch_ids

    # Define structure for PLY
    dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
        ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
        ('patch_id', 'i4')
    ]
    structured_array = np.array([tuple(row) for row in df.to_numpy()], dtype=dtype)
    ply_element = PlyElement.describe(structured_array, 'vertex')
    PlyData([ply_element], text=True).write(output_ply_path)

    print(f" Leftover points reassigned and saved to: {output_ply_path}")


assign_patch_id_from_neighbors(
    input_ply_path=r"C:\Users\wangz\Documents\HK_cc\HK_clean_label.ply",
    output_ply_path=r"C:\Users\wangz\Documents\HK_cc\HK_label_all.ply",
    leftover_id=11
)
