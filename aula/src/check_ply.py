def inspect_ply(path):
    import numpy as np

    print(f"Inspecting: {path}")
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    try:
        header_end = next(i for i, line in enumerate(lines) if line.strip() == 'end_header')
    except StopIteration:
        print(" No 'end_header' found.")
        return

    header = lines[:header_end + 1]
    body = lines[header_end + 1:]
    expected_cols = None

    for line in header:
        if line.startswith('property'):
            expected_cols = expected_cols + 1 if expected_cols else 1

    print(f" Header ends at line: {header_end}")
    print(f" Expected columns per line: {expected_cols}")
    print(f" Total data lines: {len(body)}")

    min_xyz = np.array([np.inf, np.inf, np.inf])
    max_xyz = np.array([-np.inf, -np.inf, -np.inf])
    invalid_lines = 0
    total_valid = 0

    for i, line in enumerate(body):
        if not line.strip():
            continue
        cols = line.strip().split()
        if len(cols) != expected_cols:
            print(f"  Line {i + header_end + 1} has {len(cols)} columns: {cols}")
            invalid_lines += 1
            continue
        try:
            x, y, z = float(cols[0]), float(cols[1]), float(cols[2])
            if not all(np.isfinite([x, y, z])):
                print(f"  Non-finite coordinate at line {i + header_end + 1}: {x}, {y}, {z}")
                invalid_lines += 1
                continue
            min_xyz = np.minimum(min_xyz, [x, y, z])
            max_xyz = np.maximum(max_xyz, [x, y, z])
            total_valid += 1
        except Exception as e:
            print(f"  Error parsing line {i + header_end + 1}: {e}")
            invalid_lines += 1

    print(f" Valid points: {total_valid}")
    print(f" Invalid points: {invalid_lines}")
    print(f" Bounding Box Min: {min_xyz}")
    print(f" Bounding Box Max: {max_xyz}")

# Example usage:
inspect_ply(r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_down30.ply")
