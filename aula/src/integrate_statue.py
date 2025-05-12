from plyfile import PlyData, PlyElement
import numpy as np

def prepare_patch_data(patch_path, patch_id):
    """Reads a patch PLY and returns structured array with dummy normals and patch_id."""
    ply = PlyData.read(patch_path)
    v = ply['vertex'].data
    n = len(v)

    # Create structured array with required format
    dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
        ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
        ('patch_id', 'i4')
    ]
    arr = np.empty(n, dtype=dtype)
    arr['x'] = v['x']
    arr['y'] = v['y']
    arr['z'] = v['z']
    arr['red'] = v['red']
    arr['green'] = v['green']
    arr['blue'] = v['blue']
    arr['nx'] = arr['ny'] = arr['nz'] = 0.0
    arr['patch_id'] = patch_id

    return arr

def read_main_ply_as_lines(main_path):
    """Reads the main file as text and separates header and body."""
    with open(main_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_end = next(i for i, line in enumerate(lines) if line.strip() == 'end_header')
    header = lines[:header_end + 1]
    body = lines[header_end + 1:]
    return header, body

def parse_main_data_to_structured(body_lines):
    """Parses raw body lines into structured array matching the patch format."""
    n = len(body_lines)
    dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
        ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
        ('patch_id', 'i4')
    ]
    arr = np.empty(n, dtype=dtype)

    for i, line in enumerate(body_lines):
        parts = line.strip().split()
        arr[i] = (
            float(parts[0]), float(parts[1]), float(parts[2]),
            int(parts[3]), int(parts[4]), int(parts[5]),
            float(parts[6]), float(parts[7]), float(parts[8]),
            int(parts[9])
        )
    return arr

def merge_main_and_patches(main_path, patch_paths_with_ids, output_path):
    # Step 1: Read large main PLY manually
    header, body = read_main_ply_as_lines(main_path)
    print(f"✔ Read main file with {len(body)} lines")

    main_data = parse_main_data_to_structured(body)
    print(f"✔ Parsed main data into structured array")

    # Step 2: Read patches and tag with patch_id
    patch_data = []
    for patch_path, pid in patch_paths_with_ids:
        arr = prepare_patch_data(patch_path, pid)
        patch_data.append(arr)
        print(f"✔ Loaded patch {patch_path} with {len(arr)} points")

    # Step 3: Combine and write
    all_points = np.concatenate([main_data] + patch_data)
    ply_element = PlyElement.describe(all_points, 'vertex')
    PlyData([ply_element], text=True).write(output_path)

    print(f"Merged and written to: {output_path} (Total points: {len(all_points)})")

# Example usage
if __name__ == "__main__":
    merge_main_and_patches(
        main_path=r"C:\Users\wangz\Documents\spc_aula\aula_big_plys\aula_patchid_normal.ply",
        patch_paths_with_ids=[
            (r"C:\Users\wangz\Documents\spc_aula\added_patch\43_statue2.ply", 43),
            (r"C:\Users\wangz\Documents\spc_aula\added_patch\44_tudelft.ply", 44)
        ],
        output_path=r"C:\Users\wangz\Documents\spc_aula\aula_big_plys\aula_id_with_statue3.ply"
    )



