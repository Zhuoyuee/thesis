import pdal
import json
import open3d as o3d
import numpy as np

def pack_rgb(red, green, blue):
    """Pack R, G, B into a float as PCL expects"""
    rgb = (red.astype(np.uint32) << 16) | (green.astype(np.uint32) << 8) | blue.astype(np.uint32)
    return np.frombuffer(rgb.astype(np.uint32).tobytes(), dtype=np.float32)

def convert_laz_to_pcd(input_laz, output_pcd):
    # Step 1: Load LAZ
    pipeline_json = {
        "pipeline": [{"type": "readers.las", "filename": input_laz}]
    }
    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    arrays = pipeline.arrays[0]

    # Step 2: Scale and offset
    scale = pipeline.metadata["metadata"]["readers.las"]["scale"]
    offset = pipeline.metadata["metadata"]["readers.las"]["offset"]
    xyz = np.vstack((
        arrays['X'] * scale[0] + offset[0],
        arrays['Y'] * scale[1] + offset[1],
        arrays['Z'] * scale[2] + offset[2]
    )).T

    # Step 3: Pack RGB if available
    if all(c in arrays.dtype.names for c in ['Red', 'Green', 'Blue']):
        red = arrays['Red'] >> 8  # Convert from 16-bit to 8-bit
        green = arrays['Green'] >> 8
        blue = arrays['Blue'] >> 8
        rgb_packed = pack_rgb(red, green, blue)
        colors = rgb_packed.reshape(-1, 1)
        points_rgb = np.hstack((xyz, colors))
    else:
        points_rgb = xyz

    # Step 4: Create and write PCD
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_rgb[:, :3])
    if points_rgb.shape[1] == 4:
        pcd.colors = o3d.utility.Vector3dVector(np.vstack((red, green, blue)).T / 255.0)  # Optional for viewing

    o3d.io.write_point_cloud(output_pcd, pcd, write_ascii=False, compressed=False)
    print(f"✔ Exported with packed RGB: {output_pcd}")


convert_laz_to_pcd(
    input_laz="C:/Users/wangz/thesis/AULA_merge/AULA_merged.laz",
    output_pcd="C:/Users/wangz/thesis/AULA_merge/AULA_merged.pcd"
)
