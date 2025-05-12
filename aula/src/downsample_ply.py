import numpy as np
from plyfile import PlyData, PlyElement

def downsample_ply(input_path, output_path, keep_patch_id=1, downsample_ratio=0.3):
    """
    Downsamples an ASCII PLY file using plyfile. Keeps all points with patch_id == keep_patch_id,
    downsamples the rest by downsample_ratio, and writes a valid PLY file.
    """
    ply = PlyData.read(input_path)
    vertex = ply['vertex'].data

    # Convert structured array to NumPy record array for easier indexing
    all_data = np.array(vertex)

    # Safety check: must contain patch_id
    if 'patch_id' not in all_data.dtype.names:
        raise ValueError("Input PLY file must contain a 'patch_id' property.")

    # Split into keep and downsample sets
    keep_mask = all_data['patch_id'] == keep_patch_id
    keep_data = all_data[keep_mask]
    candidate_data = all_data[~keep_mask]

    # Downsample
    num_candidates = len(candidate_data)
    sample_size = int(num_candidates * downsample_ratio)
    if sample_size > 0:
        sampled_data = np.random.choice(candidate_data, size=sample_size, replace=False)
    else:
        sampled_data = np.empty(0, dtype=all_data.dtype)

    # Combine and shuffle
    final_data = np.concatenate([keep_data, sampled_data])
    np.random.shuffle(final_data)

    # Create PlyElement and write
    vertex_element = PlyElement.describe(final_data, 'vertex')
    PlyData([vertex_element], text=True).write(output_path)

    print(f"Original points: {len(all_data)}")
    print(f"Kept all {len(keep_data)} points with patch_id == {keep_patch_id}")
    print(f"Sampled {sample_size} of {num_candidates} other points")
    print(f"Final downsampled file written to: {output_path}")

if __name__ == "__main__":
    downsample_ply(
        input_path=r"C:\Users\wangz\Documents\spc_aula\aula_big_plys\aula_id_with_statue3.ply",
        output_path=r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_down30.ply",
        keep_patch_id=1,
        downsample_ratio=0.3
    )
