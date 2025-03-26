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

# Example usage with your four points
clip_laz_wkt(r"C:\Users\wangz\thesis\37EN2_11.laz",
             r"C:\Users\wangz\thesis\AULA_AHN_clipped1.laz",
             [(85288, 446487), (85340, 446359), (85626, 446472), (85574, 446596)])
