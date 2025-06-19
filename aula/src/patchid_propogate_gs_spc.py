import numpy as np
from plyfile import PlyData, PlyElement
from scipy.spatial import cKDTree

def propagate_patch_id(spc_path, gs_path, output_path, spc_patch_col_index=9):
    # Load SPC
    spc_ply = PlyData.read(spc_path)
    spc_data = spc_ply["vertex"].data
    spc_xyz = np.stack([spc_data['x'], spc_data['y'], spc_data['z']], axis=-1)
    patch_ids = np.array([row[spc_patch_col_index] for row in spc_data], dtype=np.int32)

    print("SPC loaded.")
    print(f"SPC total points: {len(spc_xyz)}")
    unique_patch_ids = np.unique(patch_ids)
    print("Unique patch IDs in SPC:", unique_patch_ids)

    # Build KDTree
    tree = cKDTree(spc_xyz)

    # Load GS
    gs_ply = PlyData.read(gs_path)
    gs_data = gs_ply["vertex"].data
    gs_xyz = np.stack([gs_data['x'], gs_data['y'], gs_data['z']], axis=-1)

    print("GS loaded.")
    print(f"GS total points: {len(gs_xyz)}")

    # Nearest neighbor query
    distances, indices = tree.query(gs_xyz, k=1)
    assigned_patch_ids = patch_ids[indices]

    print(f"Nearest neighbor distances - min: {distances.min()}, max: {distances.max()}, median: {np.median(distances)}")
    unique_assigned = np.unique(assigned_patch_ids)
    print("Unique patch IDs assigned to GS:", unique_assigned)

    # Extend GS structured array with new int32 patch_id column
    gs_dtype = gs_data.dtype.descr + [('patch_id', 'i4')]
    gs_with_patch = np.empty(len(gs_data), dtype=gs_dtype)
    for name in gs_data.dtype.names:
        gs_with_patch[name] = gs_data[name]
    gs_with_patch['patch_id'] = assigned_patch_ids

    # Write output
    PlyData([PlyElement.describe(gs_with_patch, 'vertex')], text=False).write(output_path)
    print(f"Output written to {output_path}")


# Example usage:
propagate_patch_id(r"C:\Users\wangz\Documents\HK_GS\HK_pc_aligned.ply",
                   r"C:\Users\wangz\Documents\HK_GS\HK_GS_clip_by_bbx.ply",
                   r"C:\Users\wangz\Documents\HK_GS\HK_GS_patchid_int.ply")
