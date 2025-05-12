import open3d as o3d


def convert_ply_ascii_to_binary(input_path, output_path):
    """
    Converts an ASCII PLY file to binary using Open3D.

    Parameters:
        input_path (str): Path to input ASCII .ply
        output_path (str): Path to output binary .ply
    """
    try:
        pcd = o3d.io.read_point_cloud(input_path)
        success = o3d.io.write_point_cloud(output_path, pcd, write_ascii=False)
        if success:
            print(f"Saved binary PLY to: {output_path}")
        else:
            print("Write operation failed.")
    except Exception as e:
        print(f"Failed to convert: {e}")


# if __name__ == "__main__":
#     convert_ply_ascii_to_binary(r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_patchid_normal.ply",
#                                 r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_id_bi.ply")

if __name__ == "__main__":
    convert_ply_ascii_to_binary(r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_down30_clean.ply",
                                r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_down30_bi.ply")

