from plyfile import PlyData


def inspect_ply(file_path):
    ply_data = PlyData.read(file_path)
    vertex_data = ply_data['vertex']

    print(f"Inspecting file: {file_path}")
    print(f"Number of vertices: {len(vertex_data)}")
    print("Properties:")

    for name in vertex_data.data.dtype.names:
        dtype = vertex_data.data.dtype[name]
        print(f"  - {name}: {dtype}")

    print("\nSample values (first 3 points):")
    for i in range(min(3, len(vertex_data))):
        print({name: vertex_data[i][name] for name in vertex_data.data.dtype.names})
    print("=" * 50)


# Replace with your actual paths
# inspect_ply(r"C:\Users\wangz\monastery\HK_points.ply")
# inspect_ply(r"C:\Users\wangz\monastery\HK_GS.ply")
inspect_ply(r"C:\Users\wangz\monastery\phone_scan\HK_pc_phone.ply")
# inspect_ply(r"C:\Users\wangz\thesis\AULA_merge\AULA_sep.ply")
#