import os, json
from pathlib import Path
from plyfile import PlyData, PlyElement
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree

def assign_patch_ids_from_folder(original_ply, clips_folder, output_ply, output_json, default_patch_id=-1):
    # Load the original point cloud
    orig_ply = PlyData.read(original_ply)
    df_orig = pd.DataFrame(orig_ply['vertex'].data)

    # Initialize 'patch_id' if not present
    if 'patch_id' not in df_orig.columns:
        df_orig['patch_id'] = default_patch_id

    coords_orig = df_orig[['x', 'y', 'z']].to_numpy()
    tree = KDTree(coords_orig)

    print(f" Original cloud has {len(df_orig)} points")
    patch_dict = {}

    # Loop through all PLYs in the folder
    for fname in sorted(os.listdir(clips_folder)):
        if not fname.endswith('.ply'):
            continue

        try:
            patch_id_str, label = fname.replace('.ply', '').split('_', 1)
            patch_id = int(patch_id_str)
        except ValueError:
            print(f"⚠ Skipping invalid filename: {fname}")
            continue

        fpath = os.path.join(clips_folder, fname)
        clip_ply = PlyData.read(fpath)
        df_clip = pd.DataFrame(clip_ply['vertex'].data)
        coords_clip = df_clip[['x', 'y', 'z']].to_numpy()

        # Nearest neighbor matching
        dist, idx = tree.query(coords_clip, k=1)
        idx = idx.flatten()

        df_orig.loc[idx, 'patch_id'] = patch_id
        patch_dict[str(patch_id)] = label

        print(f" Assigned patch_id={patch_id} to {len(idx)} points [{label}]")

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
    PlyData([PlyElement.describe(array, 'vertex')], text=True).write(str(output_ply))
    Path(output_json).write_text(json.dumps(patch_dict, indent=2))

    print(f"\n Done! Output written to:\n  • PLY  → {output_ply}\n  • JSON → {output_json}")

# === Example usage ===
if __name__ == "__main__":
    assign_patch_ids_from_folder(
        original_ply=r"C:\Users\wangz\thesis\AULA_merge\AULA_clippep_clean.ply",
        clips_folder=r"C:\Users\wangz\Documents\spc_aula\patch_aula",
        output_ply=r"C:\Users\wangz\Documents\spc_aula\aula_patchid.ply",
        output_json=r"C:\Users\wangz\Documents\spc_aula\patch_id_semantics.json"
    )
