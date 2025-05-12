from plyfile import PlyData, PlyElement
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def color_points_by_cluster(input_ply_path, output_ply_path, id_column='patch_id'):
    # Load PLY to DataFrame
    ply = PlyData.read(input_ply_path)
    df = pd.DataFrame(ply['vertex'].data)

    if id_column not in df.columns:
        raise ValueError(f"'{id_column}' not found in {input_ply_path}")

    # Get all unique cluster IDs (as integers)
    cluster_ids = df[id_column].astype(int).unique()
    cluster_ids.sort()

    # Generate distinct colors using a colormap
    colormap = plt.get_cmap('tab20')  # Good for discrete clusters
    color_map = {
        cid: (np.array(colormap(i % 20)[:3]) * 255).astype(np.uint8)
        for i, cid in enumerate(cluster_ids)
    }

    # Assign RGB by cluster ID
    df['red']   = df[id_column].astype(int).map(lambda x: color_map[x][0])
    df['green'] = df[id_column].astype(int).map(lambda x: color_map[x][1])
    df['blue']  = df[id_column].astype(int).map(lambda x: color_map[x][2])

    # Define output dtype
    dtype = []
    for name in df.columns:
        if df[name].dtype == 'uint8':
            dtype.append((name, 'u1'))
        else:
            dtype.append((name, 'f4'))

    array = np.array([tuple(row) for row in df.to_numpy()], dtype=dtype)
    PlyData([PlyElement.describe(array, 'vertex')], text=True).write(output_ply_path)

    print(f" Colorized point cloud saved to: {output_ply_path}")

# Example usage:
# color_points_by_cluster(r"C:\Users\wangz\monastery\phone_scan\HK_phone_id.ply", r"C:\Users\wangz\monastery\phone_scan\HK_phone_id_viewer.ply")

#
color_points_by_cluster(r"C:\Users\wangz\Documents\spc_aula\aula_patchid.ply", r"C:\Users\wangz\Documents\spc_aula\aula_patcj_color_view.ply")