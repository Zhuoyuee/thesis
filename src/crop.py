import laspy
import numpy as np


def crop_laz(input_laz, output_laz, bbox):
    """
    Crops a LAZ file to the given bounding box and saves it as a new LAZ file.

    Parameters:
        input_laz (str): Path to the input LAZ file.
        output_laz (str): Path to the output cropped LAZ file.
        bbox (tuple): Bounding box in (min_x, min_y, max_x, max_y) in EPSG:28992.

    Returns:
        None
    """
    # Read the input LAZ file
    las = laspy.read(input_laz)

    # Extract x, y coordinates
    x, y = las.x, las.y

    # Apply bounding box filter
    mask = (x >= bbox[0]) & (x <= bbox[2]) & (y >= bbox[1]) & (y <= bbox[3])

    # Create a new LAS file with the same point format
    cropped_las = laspy.LasData(las.header)

    # Only keep points inside the bounding box
    cropped_las.points = las.points[mask]

    # Save the cropped LAZ file
    cropped_las.write(output_laz)

    print(f"Cropped LAZ file saved to: {output_laz}")


# Example usage:
bounding_box_28992 = (85265.06, 446394.49, 85641.79, 446603.71)
crop_laz(r"C:\Users\www\Desktop\thesis\AULA_AHN5\2023_C_37EN2.LAZ",
         r"C:\Users\www\Desktop\thesis\AULA_AHN5\AULA.laz",
         bounding_box_28992)
