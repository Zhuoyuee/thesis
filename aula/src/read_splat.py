import struct


def inspect_binary_splat(file_path, attribute_format, num_attributes):
    """
    Reads and inspects a binary SPLAT file.

    :param file_path: Path to the binary SPLAT file.
    :param attribute_format: Struct format string for unpacking attributes.
    :param num_attributes: Number of attributes per point.
    """
    print(f"Inspecting Binary SPLAT file: {file_path}\n")

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        # Calculate the size of each point
        point_size = struct.calcsize(attribute_format)

        # Ensure the file size aligns with the expected structure
        num_points = len(data) // point_size
        if len(data) % point_size != 0:
            print("Warning: File size does not perfectly align with the expected point structure.")

        print("--- Metadata ---")
        print(f"Number of points: {num_points}")
        print(f"Point size (bytes): {point_size}")
        print(f"Attribute format: {attribute_format}\n")

        # Read and unpack the first 10 points
        print("--- First 10 Points ---")
        for i in range(min(10, num_points)):
            start = i * point_size
            end = start + point_size
            point = struct.unpack(attribute_format, data[start:end])
            print(f"Point {i}: {point}")

        print("\n--- End of Inspection ---")
    except Exception as e:
        print(f"Error reading the binary SPLAT file: {e}")


# Example usage
# Attribute format: Assuming each point has 3 floats for x, y, z
# Modify the format string to match your SPLAT file structure
attribute_format = 'fff'  # 3 floats (x, y, z)
num_attributes = 3
inspect_binary_splat(r"C:\Users\www\Desktop\thesis\Share\AULA.splat", attribute_format, num_attributes)