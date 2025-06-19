import numpy as np
from plyfile import PlyData, PlyElement

def clip_ply_gs(bbx_source_path, gs_file_path, output_path):
    bbx_data = PlyData.read(bbx_source_path)
    bbx_xyz = np.stack([bbx_data["vertex"]["x"], bbx_data["vertex"]["y"], bbx_data["vertex"]["z"]], axis=-1)

    min_bbx = bbx_xyz.min(axis=0)
    max_bbx = bbx_xyz.max(axis=0)

    gs_ply = PlyData.read(gs_file_path)
    gs_data = gs_ply["vertex"].data
    gs_xyz = np.stack([gs_data['x'], gs_data['y'], gs_data['z']], axis=-1)

    mask = np.all((gs_xyz >= min_bbx) & (gs_xyz <= max_bbx), axis=1)
    filtered_data = gs_data[mask]

    filtered_element = PlyElement.describe(filtered_data, "vertex")
    PlyData([filtered_element], text=False).write(output_path)
    print(f"Filtered GS written to: {output_path}")



bbx_source_path = r"C:\Users\wangz\Documents\HK_GS/HK_GS_3 - cc_clip.ply"
gs_file_path = r"C:\Users\wangz\Documents\HK_GS/HK_GS_3.ply"
output_path = r"C:\Users\wangz\Documents\HK_GS/HK_GS_clip_by_bbx.ply"
clip_ply_gs(bbx_source_path, gs_file_path, output_path)