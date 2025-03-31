import pdal
import json

def clip_laz_wkt(input_laz: str, output_laz: str, points: list):
    """
    Clips a LAZ file using a Well-Known Text (WKT) polygon.

    Parameters:
    - input_laz (str): Path to the input LAZ file.
    - output_laz (str): Path to save the clipped LAZ file.
    - points (list): List of (x, y) coordinates defining the clipping polygon.

    Example:
    clip_laz_wkt("input.laz", "clipped_output.laz",
                 [(85288, 446487), (85340, 446359), (85626, 446472), (85574, 446596)])
    """
    # Convert points to WKT polygon format
    wkt_polygon = "POLYGON ((" + ", ".join(f"{x} {y}" for x, y in points) + f", {points[0][0]} {points[0][1]}))"

    pipeline_json = {
        "pipeline": [
            input_laz,
            {
                "type": "filters.crop",
                "polygon": wkt_polygon
            },
            output_laz
        ]
    }

    pipeline_str = json.dumps(pipeline_json)

    pipeline = pdal.Pipeline(pipeline_str)
    pipeline.execute()

    print(f"WKT Polygon-clipped LAZ file saved to {output_laz}")

# # Example usage with your four points
# clip_laz_wkt(r"C:\Users\wangz\thesis\37EN2_11.laz",
#              r"C:\Users\wangz\thesis\AULA_AHN_clipped1.laz",
#              [(85288, 446487), (85340, 446359), (85626, 446472), (85574, 446596)])


def clip_laz_3d(input_laz: str, output_laz: str, points: list, z_min: float, z_max: float):
    """
    Clips a LAZ file using a 2.5D polygon and Z (height) bounds.

    Parameters:
    - input_laz (str): Path to input LAZ file.
    - output_laz (str): Path to output clipped LAZ.
    - points (list): List of (x, y) coordinates defining the 2D polygon.
    - z_min (float): Minimum Z value to include.
    - z_max (float): Maximum Z value to include.
    """
    wkt_polygon = "POLYGON ((" + ", ".join(f"{x} {y}" for x, y in points) + f", {points[0][0]} {points[0][1]}))"

    pipeline_json = {
        "pipeline": [
            input_laz,
            {
                "type": "filters.crop",
                "polygon": wkt_polygon
            },
            {
                "type": "filters.range",
                "limits": f"Z[{z_min}:{z_max}]"
            },
            output_laz
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    print(f"✅ Clipped to polygon + Z range. Saved to: {output_laz}")


clip_laz_3d(
    input_laz=r"C:\Users\wangz\monastery\HK_clipped.laz",
    output_laz=r"C:\Users\wangz\monastery\HK_clipped1.laz",
    points=[
        (-0.83, 0.90),
        (0.46, 0.90),
        (0.46, 2.18),
        (-0.83, 2.18)
    ],
    z_min=-0.1,
    z_max=1.5
)