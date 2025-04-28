import pdal
import json
from shapely.geometry import Polygon
from shapely import wkt as shapely_wkt

def clip_laz_polygon(input_laz: str, output_laz: str, points: list, z_min: float = None, z_max: float = None, buffer_distance: float = 0.0):
    """
    Clips a LAZ file using a polygon (with optional buffer) and optional Z range.

    Parameters:
    - input_laz (str): Path to input LAZ file.
    - output_laz (str): Path to output clipped LAZ.
    - points (list): List of (x, y) coordinates.
    - z_min (float, optional): Minimum Z value.
    - z_max (float, optional): Maximum Z value.
    - buffer_distance (float, optional): Buffer distance in meters (default: 0.0)
    """

    # Create Shapely polygon and apply buffer
    poly = Polygon(points)
    buffered_poly = poly.buffer(buffer_distance)
    wkt_polygon = buffered_poly.wkt

    # Build PDAL pipeline
    pipeline_steps = [
        input_laz,
        {"type": "filters.crop", "polygon": wkt_polygon}
    ]

    if z_min is not None and z_max is not None:
        pipeline_steps.append({
            "type": "filters.range",
            "limits": f"Z[{z_min}:{z_max}]"
        })

    pipeline_steps.append(output_laz)

    pipeline_json = {"pipeline": pipeline_steps}
    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()

    print(f" Clipped to buffered polygon{' + Z range' if z_min is not None and z_max is not None else ''}. Saved to: {output_laz}")

# clip_laz_3d(
#     input_laz=r"C:\Users\wangz\monastery\HK_clipped.laz",
#     output_laz=r"C:\Users\wangz\monastery\HK_clipped1.laz",
#     points=[
#         (-0.83, 0.90),
#         (0.46, 0.90),
#         (0.46, 2.18),
#         (-0.83, 2.18)
#     ],
#     z_min=-0.1,
#     z_max=1.5
# )

# ((85577.41, 446480.79) (85568.72, 446574.19)(85562.07, 446573.34)(85473.75, 446515.92)(85459, 446471.05)(85459.47,446458.72)
#  (85506.32, 446472.35)(85552.51, 446476.91)(85562.73, 446478.21))

# clip_laz_polygon(
#     input_laz=r"C:\Users\wangz\thesis\AULA_merge\library_MLS.laz",
#     output_laz=r"C:\Users\wangz\thesis\AULA_merge\lib_MLS_clipped.laz",
#     points=[(85577.41, 446480.79), (85568.72, 446574.19), (85562.07, 446573.34),
#             (85473.75, 446515.92), (85459, 446471.05), (85459.47, 446458.72),
#             (85506.32, 446472.35), (85552.51, 446476.91), (85562.73, 446478.21)],
#     buffer_distance=0.05  # 5 cm
# )

# clip_laz_polygon(
#     input_laz=r"C:\Users\wangz\thesis\AULA_merge\AULA_building_separated.laz",
#     output_laz=r"C:\Users\wangz\thesis\AULA_merge\AULA_clipped.laz",
#     points=[(85343.11, 446409.72),(85319.41, 446471.17),(85433.36, 446524.02),(85458.38, 446456.23)],
# )
clip_laz_polygon(
    input_laz=r"C:\Users\wangz\monastery\HK_clipped1.laz",
    output_laz=r"C:\Users\wangz\monastery\HK_clipped2.laz",
    points=[(-0.34, 2.03),(-0.75, 1.55),(-0.07, 0.99),(0.33, 1.48)],
    buffer_distance = 0.05
)