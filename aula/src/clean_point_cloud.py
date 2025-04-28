import laspy
import numpy as np
from sklearn.cluster import DBSCAN

def clean_laz_with_3d_dbscan(input_laz, output_laz, eps=1.0, min_samples=30):
    # failed for the library
    with laspy.open(input_laz) as file:
        las = file.read()
        x = las.x
        y = las.y
        z = las.z

    coords = np.column_stack((x, y, z))

    # Run DBSCAN in 3D
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    labels = db.labels_

    # Identify the largest cluster (excluding noise)
    unique, counts = np.unique(labels[labels != -1], return_counts=True)
    if len(counts) == 0:
        raise ValueError("No valid clusters found in the point cloud.")

    main_cluster_label = unique[np.argmax(counts)]
    keep_mask = labels == main_cluster_label

    # Filter points
    filtered_points = las.points[keep_mask]

    # Save cleaned file
    cleaned_las = laspy.LasData(las.header)
    cleaned_las.points = filtered_points
    cleaned_las.write(output_laz)

    print(f"Cleaned LAZ saved to: {output_laz} (kept {keep_mask.sum()} points)")


clean_laz_with_3d_dbscan(
    input_laz=r"C:\Users\wangz\thesis\AULA_merge\lib_MLS_clipped.laz",
    output_laz=r"C:\Users\wangz\thesis\AULA_merge\lib_cleaned.laz",
    eps=1.0,
    min_samples=30
)
