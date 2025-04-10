import pdal
import json

def clean_and_downsample(input_laz, output_laz,
                              sample_radius=0.02,   # 2mm
                              mean_k=12,
                              std_ratio=0.8):
    """
    Clean a LAZ point cloud using SOR and downsample using sample filter.

    Parameters:
    - input_laz: str, input .laz path
    - output_laz: str, output .laz path
    - sample_radius: float, min distance between points
    - mean_k: int, neighbors for SOR
    - std_ratio: float, threshold for SOR
    """
    pipeline = {
        "pipeline": [
            input_laz,
            {
                "type": "filters.outlier",
                "method": "statistical",
                "mean_k": mean_k,
                "multiplier": std_ratio
            },
            {
                "type": "filters.sample",
                "radius": sample_radius
            },
            output_laz
        ]
    }

    pipeline_json = json.dumps(pipeline)
    pipeline = pdal.Pipeline(pipeline_json)
    pipeline.execute()

    print(f"Finished: cleaned and sampled point cloud saved to {output_laz}")
    return pipeline



clean_and_downsample(r"C:\Users\wangz\thesis\AULA_merge\AULA_clipped.laz", r"C:\Users\wangz\thesis\AULA_merge\AULA_clippep_down.laz")
