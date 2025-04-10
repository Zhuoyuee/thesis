import pandas as pd
import numpy as np
from plyfile import PlyData, PlyElement
import json

def clean_ply_id(input_ply_path, output_ply_path, output_legend_path):
    # Load PLY
    ply_data = PlyData.read(input_ply_path)
    vertex_data = ply_data['vertex'].data
    df = pd.DataFrame(vertex_data)

    # Define standard geometry/color/normal fields
    keep_cols = ['x', 'y', 'z', 'red', 'green', 'blue', 'nx', 'ny', 'nz']
    meta_cols = [col for col in df.columns if col not in keep_cols]

    patch_ids = []
    id_to_name = {}
    label_counter = 0

    # Scan from right to left (to prioritize most recently added scalar fields)
    for i, row in df.iterrows():
        assigned = False
        for col in reversed(meta_cols):
            if not np.isnan(row[col]):
                name = col.replace("scalar_", "")
                if name not in id_to_name.values():
                    id_to_name[label_counter] = name
                    label_counter += 1
                id_num = [k for k, v in id_to_name.items() if v == name][0]
                patch_ids.append(id_num)
                assigned = True
                break
        if not assigned:
            patch_ids.append(99)  # Unlabeled / leftover

    # Build clean dataframe
    df_clean = df[keep_cols].copy()
    df_clean['patch_id'] = patch_ids

    # Round floats to 6 decimals for clean output
    for col in ['x', 'y', 'z', 'nx', 'ny', 'nz']:
        df_clean[col] = df_clean[col].round(6)

    # Define dtype and write new PLY
    dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
        ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
        ('patch_id', 'i4')
    ]
    structured_array = np.array([tuple(row) for row in df_clean.to_numpy()], dtype=dtype)
    ply_element = PlyElement.describe(structured_array, 'vertex')
    PlyData([ply_element], text=True).write(output_ply_path)

    # Save patch ID legend
    with open(output_legend_path, 'w') as f:
        json.dump(id_to_name, f, indent=2)

    print(f"✅ Cleaned PLY saved: {output_ply_path}")
    print(f"✅ Patch legend saved: {output_legend_path}")

# Example usage:
# clean_and_export_ply_with_patch_id(
#     input_ply_path="merged_planes_with_labels.ply",
#     output_ply_path="cleaned_patch_cloud.ply",
#     output_legend_path="patch_legend.json"
# )

clean_ply_id(
    input_ply_path=r"C:\Users\wangz\Documents\HK_cc\labeled.ply",
    output_ply_path=r"C:\Users\wangz\Documents\HK_cc\HK_clean_label.ply",
    output_legend_path=r"C:\Users\wangz\Documents\HK_cc\HK_clusterID_label1.json"
)
