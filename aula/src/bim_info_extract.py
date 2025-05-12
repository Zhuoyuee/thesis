import numpy as np, json, plyfile, hashlib
from pathlib import Path
from typing import List

# === Utility: generate 32-bit hash from string ===
def fast_hash(s: str) -> int:
    return int(hashlib.md5(s.encode()).hexdigest()[:8], 16)

# === Recursive mesh extractor ===
def extract_mesh_data(obj, patch_list: List[dict], parent_meta=None):
    if not isinstance(obj, dict):
        return

    speckle_type = obj.get("speckle_type", "")

    # If it's a Mesh, extract geometry
    if speckle_type.endswith("Mesh") and "vertices" in obj and "faces" in obj:
        verts = np.array(obj["vertices"], dtype=np.float32).reshape(-1, 3)
        faces_raw = obj["faces"]
        faces = []

        i = 0
        while i < len(faces_raw):
            count = faces_raw[i]
            if count == 3:
                faces.append(faces_raw[i+1:i+4])
                i += 4
            else:
                i += count + 1

        patch_id = fast_hash(obj.get("id", str(len(patch_list))))
        patch_list.append({
            "verts": verts,
            "faces": np.array(faces, dtype=np.int32),
            "id": patch_id,
            "meta": {
                "id": obj.get("id", ""),
                "name": obj.get("name", ""),
                "category": obj.get("category", ""),
                "type": speckle_type,
                **(parent_meta or {})  # inherit parent element info if present
            }
        })

    # Look inside displayValue, elements, children, etc.
    for k, v in obj.items():
        if k in ["displayValue", "elements", "children", "@displayValue"]:
            if isinstance(v, list):
                for item in v:
                    extract_mesh_data(item, patch_list, parent_meta=obj)
            elif isinstance(v, dict):
                extract_mesh_data(v, patch_list, parent_meta=obj)
        elif isinstance(v, list):
            for item in v:
                extract_mesh_data(item, patch_list)
        elif isinstance(v, dict):
            extract_mesh_data(v, patch_list)

# === Export function ===
def export_to_ply_and_json(raw_obj, ply_path: Path, json_path: Path):
    patches = []
    extract_mesh_data(raw_obj, patches)

    if not patches:
        print(" No mesh data found.")
        return

    all_verts = []
    semantics = {}
    for patch in patches:
        verts = patch["verts"]
        patch_id = patch["id"]
        patch_tag = np.full((len(verts), 1), patch_id, dtype=np.uint32)
        rec = np.rec.fromarrays(
            [verts[:, 0], verts[:, 1], verts[:, 2], patch_tag[:, 0]],
            names="x,y,z,patch_id", formats="f4,f4,f4,u4"
        )
        all_verts.append(rec)
        semantics[str(patch_id)] = patch["meta"]

    verts_all = np.concatenate(all_verts)
    ply_el = plyfile.PlyElement.describe(verts_all, "vertex")
    plyfile.PlyData([ply_el], text=False).write(str(ply_path))
    json_path.write_text(json.dumps(semantics, indent=2))

    print(f"Exported: {len(verts_all)} vertices from {len(patches)} patches")
    print(f"→ PLY:   {ply_path}")
    print(f"→ JSON:  {json_path}")

# === Usage ===
if __name__ == "__main__":
    from speckle_stream import fetch_latest_raw_object  # must return the raw dict
    raw_obj = fetch_latest_raw_object()
    export_to_ply_and_json(raw_obj, Path(r"C:\Users\wangz\HBIM\bim_aula.ply"), Path(r"C:\Users\wangz\HBIM\bim_aula_semantics.json"))


