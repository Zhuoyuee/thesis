import os
import numpy as np
from plyfile import PlyData, PlyElement

def segment_gs_by_patchid_and_export(gs_path, output_dir):
    """
    Segments a GS PLY file by integer patch_id and exports each group to a new PLY file,
    excluding the patch_id column.

    Args:
        gs_path (str): Path to the input GS PLY file (with integer patch_id as last column).
        output_dir (str): Directory where segmented files will be saved.
    """
    # Load PLY
    gs_ply = PlyData.read(gs_path)
    gs_data = gs_ply["vertex"].data

    # Extract field names
    field_names = gs_data.dtype.names
    patch_id_col = field_names[-1]
    assert np.issubdtype(gs_data[patch_id_col].dtype, np.integer), "Last column must be integer patch_id"

    # Prepare export fields (exclude patch_id)
    export_fields = field_names[:-1]
    export_dtype = [(name, gs_data.dtype[name]) for name in export_fields]

    # Group by patch_id
    patch_ids = np.unique(gs_data[patch_id_col])
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(gs_path))[0]

    for pid in patch_ids:
        mask = gs_data[patch_id_col] == pid
        subset = gs_data[mask]

        # Remove patch_id column
        export_data = np.empty(len(subset), dtype=export_dtype)
        for name in export_fields:
            export_data[name] = subset[name]

        # Export
        filename = f"{base_name}_patch_{pid}.ply"
        filepath = os.path.join(output_dir, filename)
        PlyData([PlyElement.describe(export_data, 'vertex')], text=False).write(filepath)
        print(f"Saved patch {pid} to {filepath}")


segment_gs_by_patchid_and_export(r"C:\Users\wangz\Documents\HK_GS\HK_GS_patchid_int.ply",
                       r"C:\Users\wangz\Documents\HK_GS\gs_seg")