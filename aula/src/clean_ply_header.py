def normalize_ply(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # Strip trailing whitespace (e.g., '\r\n' → '\n')
    clean_lines = [line.rstrip('\r\n') + '\n' for line in lines]

    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(clean_lines)

    print(f"Normalized PLY saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    normalize_ply(
        input_path=r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_down30.ply",
        output_path=r"C:\Users\wangz\Documents\spc_viewer\spc_viewer\public\aula_down30_clean.ply"
    )
