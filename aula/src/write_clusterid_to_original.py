from plyfile import PlyData, PlyElement
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree

def merge_patch_id_and_normals(
    original_ply_path,
    segmented_ply_path,
    output_ply_path,
    keep_normals=True
):
    # Load original cloud (with RGB, maybe normals)
    orig_ply = PlyData.read(original_ply_path)
    df_orig = pd.DataFrame(orig_ply['vertex'].data)

    # Load segmented cloud (with patch_id, maybe normals)
    seg_ply = PlyData.read(segmented_ply_path)
    df_seg = pd.DataFrame(seg_ply['vertex'].data)

    # Match nearest neighbors
    tree = KDTree(df_seg[['x', 'y', 'z']].values)
    _, indices = tree.query(df_orig[['x', 'y', 'z']].values, k=1)

    # Assign patch_id from nearest
    df_orig['patch_id'] = df_seg.iloc[indices.flatten()]['patch_id'].astype('float32').values

    # Handle normals
    if keep_normals and all(n in df_orig.columns for n in ['nx', 'ny', 'nz']):
        nx = df_orig['nx'].astype('float32').values
        ny = df_orig['ny'].astype('float32').values
        nz = df_orig['nz'].astype('float32').values
    elif keep_normals and all(n in df_seg.columns for n in ['nx', 'ny', 'nz']):
        nx = df_seg.iloc[indices.flatten()]['nx'].astype('float32').values
        ny = df_seg.iloc[indices.flatten()]['ny'].astype('float32').values
        nz = df_seg.iloc[indices.flatten()]['nz'].astype('float32').values
    else:
        nx = np.zeros(len(df_orig), dtype='float32')
        ny = np.zeros(len(df_orig), dtype='float32')
        nz = np.zeros(len(df_orig), dtype='float32')

    # Prepare DataFrame for export
    df_out = pd.DataFrame({
        'x': df_orig['x'].astype('float32'),
        'y': df_orig['y'].astype('float32'),
        'z': df_orig['z'].astype('float32'),
        'red': df_orig['red'].astype('uint8'),
        'green': df_orig['green'].astype('uint8'),
        'blue': df_orig['blue'].astype('uint8'),
        'nx': nx,
        'ny': ny,
        'nz': nz,
        'patch_id': df_orig['patch_id']
    })

    # Define structured dtype
    dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
        ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
        ('patch_id', 'f4')
    ]

    array = np.array([tuple(row) for row in df_out.to_numpy()], dtype=dtype)
    PlyData([PlyElement.describe(array, 'vertex')], text=True).write(output_ply_path)

    print(f"Output saved: {output_ply_path}")


merge_patch_id_and_normals(
    original_ply_path=r"C:\Users\wangz\monastery\phone_scan\HK_pc_phone.ply",
    segmented_ply_path=r"C:\Users\wangz\Documents\HK_cc\HK_label_all.ply",
    output_ply_path=r"C:\Users\wangz\monastery\phone_scan\HK_phone_id.ply"
)
