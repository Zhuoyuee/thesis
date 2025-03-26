import pdal
import json


def filter_classification(mls_file, ahn_file, output_file, distance_threshold=0.1):
    """
    Merges MLS and AHN while keeping only AHN points classified as Buildings (Classification = 6).

    - Keeps MLS RGB
    - Uses only AHN points with Classification = 6
    - Removes duplicate points based on threshold

    Parameters:
    - mls_file (str): Path to the MLS LAZ file (keeps RGB).
    - ahn_file (str): Path to the AHN LAZ file (provides building classification).
    - output_file (str): Path to save the merged point cloud.
    - distance_threshold (float): Minimum allowed distance between points to avoid duplicates.
    """
    pipeline_json = {
        "pipeline": [
            # Read MLS (keeps RGB)
            {"type": "readers.las", "filename": mls_file},

            # Read AHN (provides classification)
            {"type": "readers.las", "filename": ahn_file},

            # Filter AHN to keep only buildings (classification = 6)
            {"type": "filters.range",
             "limits": "Classification[6:6]"},

            # Merge MLS with filtered AHN
            {"type": "filters.merge"},

            # Remove close duplicates
            {"type": "filters.outlier",
             "method": "radius",
             "radius": distance_threshold,
             "min_k": 1},

            # Write final output
            {"type": "writers.las", "filename": output_file, "a_srs": "EPSG:28992"}
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    print(f"Merged MLS + AHN Buildings Only (Classification 6) saved to: {output_file}")

def merge_laz(mls_file, ahn_file, output_file):
    """
    Merges two LAZ files (MLS + AHN) into a single file.

    - Includes both files fully.
    - Preserves attributes (RGB, classification, etc.).

    Parameters:
    - mls_file (str): Path to the MLS LAZ file.
    - ahn_file (str): Path to the AHN LAZ file.
    - output_file (str): Path to save the merged point cloud.
    """
    pipeline_json = {
        "pipeline": [
            {"type": "readers.las", "filename": mls_file},
            {"type": "readers.las", "filename": ahn_file},
            {"type": "filters.merge"},
            {"type": "writers.las",
             "filename": output_file,
             "a_srs": "EPSG:28992"}
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    print(f"Merged LAZ file saved to: {output_file}")


# Example usage
merge_laz(
    "C:/Users/wangz/thesis/MLS_AULA_georeference_2.laz",
    "C:/Users/wangz/thesis/AULA_merge/AULA_building_AHN.laz",
    "C:/Users/wangz/thesis/AULA_merge/AULA_merged.laz"
)
