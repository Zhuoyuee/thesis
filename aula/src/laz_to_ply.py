import pdal
import json


def convert_laz_to_ply(input_laz, output_ply):
    """
    Converts a LAZ file to PLY format using PDAL.

    Parameters:
    - input_laz (str): Path to input LAZ file.
    - output_ply (str): Path to save the PLY file.
    """
    pipeline_json = {
        "pipeline": [
            {"type": "readers.las", "filename": input_laz},
            {"type": "writers.ply", "filename": output_ply}
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    print(f"Converted LAZ to PLY: {output_ply}")


# Example usage
convert_laz_to_ply(
    "C:/Users/wangz/thesis/AULA_merge/AULA_merged.laz",
    "C:/Users/wangz/thesis/AULA_merge/AULA_merged.ply"
)
