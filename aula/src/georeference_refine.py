'''
second time
(85589.88, 446498.53) (85569.99, 446483.49)
(85655.72, 446554.75) (85563.63, 446568.94)
(85535.69, 446634.06, 12.35) (85425.24, 446510.87, 12.07)
(85500.66, 446586.29, 12.37) (85448.58, 446454.90, 12.09)
(85442.33, 446685.88, 10.64) (85332.14, 446458.89, 9.91)
(85442.49, 446658.91, 10.58) (85345.89, 446425.64, 9.7)

    source_points = np.array([
        [85589.88, 446498.53],
        [85655.72, 446554.75],
        [85535.69, 446634.06],
        [85500.66, 446586.29],
        [85442.33, 446685.88],
        [85442.49, 446658.91]
    ])

    target_points = np.array([
        [85569.99, 446483.49],
        [85563.63, 446568.94],
        [85425.24, 446510.87],
        [85448.58, 446454.90],
        [85332.14, 446458.89],
        [85345.89, 446425.64]
    ])

Third time
source_points = np.array([
    [85577.75, 446476.66, 14.13],
    [85556.18, 446461.06, 7.02],
    [85509.3, 446509.38, 6.46],
    [85569.31, 446569.71, 9.10],
    [85475.5, 446509.70, -0.16],
    [85331.54, 446456.05, 10.27],
    [85345.47, 446421.75, 10.27],
    [85334.52, 446420.56, 2.28],
    [85387.37, 446425.96, 7.5]
])


target_points = np.array([
    [85578.26, 446481.65, 13.90],
    [85556.60, 446466.10, 6.78],
    [85509.49, 446514.28, 6.10],
    [85569.15, 446574.09, 8.76],
    [85476.26, 446513.05, -0.29],
    [85332.19, 446459.50, 10.52],
    [85346.22, 446425.19, 10.40],
    [85335.15, 446423.95, 2.28],
    [85380.3, 446429.86, 7.38]
])
'''

import numpy as np
import pdal
import json


def compute_transformation_matrix(source_points, target_points):
    """
    Computes the transformation matrix to align MLS with AHN, preserving previous georeferencing.

    Parameters:
    - source_points: np.array of shape (N,3) → MLS (current round)
    - target_points: np.array of shape (N,3) → AHN (reference)

    Returns:
    - PDAL-compatible transformation matrix as a string
    """

    # Compute centroids
    centroid_source = np.mean(source_points, axis=0)
    centroid_target = np.mean(target_points, axis=0)

    # Center the points
    P = source_points - centroid_source
    Q = target_points - centroid_target

    # Compute covariance matrix
    H = np.dot(P.T, Q)

    # Compute SVD for rotation
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # Ensure no reflection
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = np.dot(Vt.T, U.T)

    # Compute translation
    t = centroid_target - np.dot(R, centroid_source)

    # Construct 4x4 transformation matrix
    T = np.eye(4)
    T[:3, :3] = R  # Rotation (3D)
    T[:3, 3] = t  # Translation

    print("Computed 3D Transformation Matrix:")
    print(T)

    # Return matrix formatted for PDAL
    return " ".join(map(str, T.flatten()))


def transform_laz_with_pdal(input_file, output_file, transformation_matrix):
    """
    Applies the transformation matrix to the MLS point cloud using PDAL.

    Parameters:
    - input_file (str): Path to input LAZ file
    - output_file (str): Path to output transformed LAZ file
    - transformation_matrix (str): 4x4 matrix formatted for PDAL
    """
    pipeline_json = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": input_file
            },
            {
                "type": "filters.transformation",
                "matrix": transformation_matrix
            },
            {
                "type": "writers.las",
                "filename": output_file,
                "a_srs": "EPSG:28992"  # Assigning the correct projection
            }
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    print("Transformation applied and saved to:", output_file)


# # --- Step 1: Prepare Points ---
# source_points = np.array([
#     [85555.8, 446465.47, 6.83],
#     [85577.41, 446480.8, 13.83],
#     [85478.16, 446437.85, 7.06],
#     [85475.47, 446437.05, 8.22],
#     [85478.74, 446433.9, 11.75],
#     [85374.79, 446424.28, 5.35],
#     [85316.69, 446464.29, 10.02],
#     [85421.63, 446516.29, -0.9],
#     [85568.65, 446574.13, 8.73]
# ])
#
# target_points = np.array([
#     [85556.6, 446446.1, 6.78],
#     [85578.1, 446481.3, 13.93],
#     [85479.3, 446438.03, 7.08],
#     [85476.43, 446436.95, 8.25],
#     [85479.77, 446433.85, 11.81],
#     [85375.49, 446424.03, 5.32],
#     [85317.28, 446463.85, 9.82],
#     [85422.74, 446516.16, -0.89],
#     [85569.15, 446574.09, 8.76]
# ])
#
# # --- Step 2: Compute Transformation ---
# pdal_matrix = compute_transformation_matrix(source_points, target_points)
#
# # --- Step 3: Apply Transformation ---
# input_file = "C:/Users/wangz/thesis/MLS_AULA_georeference_2.laz"
# output_file = "C:/Users/wangz/thesis/MLS_AULA_georeference_5.laz"
# transform_laz_with_pdal(input_file, output_file, pdal_matrix)

cc_matrix = "1.0 0.005 0.001 0.0 -0.005 1.0 0.0 0.0 -0.001 -0.0 1.0 0.0 3.319 -2.341 -0.426 1.0"
transform_laz_with_pdal("C:/Users/wangz/thesis/MLS_AULA_georeference_2.laz", "C:/Users/wangz/thesis/MLS_AULA_georeference_7.laz", cc_matrix)

