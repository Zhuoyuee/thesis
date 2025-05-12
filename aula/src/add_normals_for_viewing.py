def convert_ply_to_hk_format(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    try:
        header_end_idx = next(i for i, line in enumerate(lines) if line.strip() == "end_header")
    except StopIteration:
        raise ValueError("PLY file header is malformed or missing 'end_header'.")

    body = lines[header_end_idx + 1:]

    new_header = [
        "ply\n",
        "format ascii 1.0\n",
        f"element vertex {len(body)}\n",
        "property float x\n",
        "property float y\n",
        "property float z\n",
        "property uchar red\n",
        "property uchar green\n",
        "property uchar blue\n",
        "property float nx\n",
        "property float ny\n",
        "property float nz\n",
        "property int patch_id\n",
        "end_header\n"
    ]

    with open(output_path, 'w') as f:
        f.writelines(new_header)
        for line in body:
            cols = line.strip().split()
            if len(cols) < 7:
                continue
            x, y, z, r, g, b, patch_id = cols
            f.write(f"{x} {y} {z} {r} {g} {b} 0 0 0 {patch_id}\n")


if __name__ == "__main__":
    convert_ply_to_hk_format(r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_patchid.ply",
                             r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_patchid_normal.ply")
