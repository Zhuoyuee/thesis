from plyfile import PlyData, PlyElement
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree

def assign_patch_ids_by_clips(original_ply, clip_plys, clip_ids, output_ply):
    # Load original point cloud
    orig_ply = PlyData.read(original_ply)
    df_orig = pd.DataFrame(orig_ply['vertex'].data)

    if 'patch_id' not in df_orig.columns:
        raise ValueError("Original file must already contain a 'patch_id' field.")

    coords_orig = df_orig[['x', 'y', 'z']].to_numpy()
    tree = KDTree(coords_orig)

    print(f"Original cloud has {len(df_orig)} points")

    for clip_path, patch_id in zip(clip_plys, clip_ids):
        clip_ply = PlyData.read(clip_path)
        df_clip = pd.DataFrame(clip_ply['vertex'].data)
        coords_clip = df_clip[['x', 'y', 'z']].to_numpy()

        dist, idx = tree.query(coords_clip, k=1)
        idx = idx.flatten()
        df_orig.loc[idx, 'patch_id'] = patch_id

        print(f"Updated {len(idx)} points to patch_id={patch_id}")

    # Define output dtype
    dtype = []
    for col in df_orig.columns:
        if df_orig[col].dtype == 'uint8':
            dtype.append((col, 'u1'))
        elif col == 'patch_id':
            dtype.append((col, 'i4'))
        else:
            dtype.append((col, 'f4'))

    array = np.array([tuple(row) for row in df_orig.to_numpy()], dtype=dtype)
    PlyData([PlyElement.describe(array, 'vertex')], text=True).write(output_ply)

    print(f"Output written to: {output_ply}")



assign_patch_ids_by_clips(
    original_ply=r"C:\Users\wangz\monastery\phone_scan\HK_phone_id.ply",
    clip_plys=[r"C:\Users\wangz\Documents\HK_cc\seg\HK_plate_side.ply", r"C:\Users\wangz\Documents\HK_cc\seg\HK_plate1.ply", r"C:\Users\wangz\Documents\HK_cc\seg\HK_plate2.ply"],
    clip_ids=[9, 10, 11],
    output_ply=r"C:\Users\wangz\monastery\phone_scan\HK_id_refined.ply"
)
