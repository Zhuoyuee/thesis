import pdal
import json
import numpy as np
from plyfile import PlyData, PlyElement

def laz_to_ply_pcl_style(input_laz, output_ply):
    import pdal
    import numpy as np
    from plyfile import PlyData, PlyElement
    import json

    pipeline_json = {
        "pipeline": [{"type": "readers.las", "filename": input_laz}]
    }
    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    arrays = pipeline.arrays[0]

    x = arrays['X'].astype(np.float32)
    y = arrays['Y'].astype(np.float32)
    z = arrays['Z'].astype(np.float32)

    # 🟥 Color fix: normalize if values > 255
    def scale_color(c):
        if c.max() > 255:
            return (c / 256).clip(0, 255).astype(np.uint8)
        else:
            return c.astype(np.uint8)

    if all(k in arrays.dtype.names for k in ['Red', 'Green', 'Blue']):
        red = scale_color(arrays['Red'])
        green = scale_color(arrays['Green'])
        blue = scale_color(arrays['Blue'])
    else:
        red = green = blue = np.zeros_like(x, dtype=np.uint8)

    vertex_data = np.empty(x.shape[0], dtype=[
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
    ])
    vertex_data['x'], vertex_data['y'], vertex_data['z'] = x, y, z
    vertex_data['red'], vertex_data['green'], vertex_data['blue'] = red, green, blue

    el = PlyElement.describe(vertex_data, 'vertex')
    PlyData([el], text=False).write(output_ply)
    print("✅ PLY with color written to:", output_ply)




# if __name__ == "__main__":
#     laz_to_ply_pcl_style(
#         input_laz = "C:/Users/wangz/thesis/AULA_merge/AULA_building_separated.laz",
#         output_ply = "C:/Users/wangz/thesis/AULA_merge/AULA_sep.ply"
#     )
#
laz_to_ply_pcl_style(
        input_laz = r"C:\Users\wangz\monastery\HK_down_clean1.laz",
        output_ply = "C:/Users/wangz/monastery\HK_down_clean.ply"
    )



# laz_to_ply_pcl_style(
#         input_laz = r"C:\Users\wangz\thesis\AULA_merge\AULA_merged.laz",
#         output_ply = r"C:\Users\wangz\thesis\AULA_merge\AULA_clib_merged.ply"
#     )