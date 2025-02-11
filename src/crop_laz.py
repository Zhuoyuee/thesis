import pdal
import json


def crop_laz(input_laz, output_laz, bounding_box):
    """
    Crops a LAZ point cloud file to the given bounding box (EPSG:28992).

    Parameters:
        input_laz (str): Path to the input LAZ file.
        output_laz (str): Path to the output cropped LAZ file.
        bounding_box (tuple): (min_x, min_y, max_x, max_y) in EPSG:28992.

    Returns:
        None
    """
    min_x, min_y, max_x, max_y = bounding_box

    pipeline_json = {
        "pipeline": [
            input_laz,
            {
                "type": "filters.crop",
                "bounds": f"([{min_x},{max_x}],[{min_y},{max_y}])"
            },
            output_laz
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()


# Example usage
bounding_box = (85265.06, 446394.49, 85641.79, 446603.71)
crop_laz("input.laz", "output_cropped.laz", bounding_box)

# 52.003421, 4.371624
# 52.001588, 4.377152

