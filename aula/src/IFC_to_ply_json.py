"""
ifc2ply_semantics.py
Converts an IFC to:
   - model.ply           (XYZ + elem_id per vertex)
   - bim_semantics.json  {elem_id: {GlobalId, IfcType, Name, Props...}}
"""

import ifcopenshell, ifcopenshell.geom as geom
import numpy as np, json, plyfile, hashlib, pathlib

def fast_hash(guid: str) -> int:
    """Deterministic 32-bit code from a GlobalId (collision-free for <4 billion elems)."""
    return int(hashlib.md5(guid.encode()).hexdigest()[:8], 16)


def collect(ifc_path: pathlib.Path, ply_out: pathlib.Path, json_out: pathlib.Path):
    settings = geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    settings.set(settings.APPLY_DEFAULT_MATERIALS, False)

    ifc = ifcopenshell.open(str(ifc_path))
    for prod in ifc.by_type("IfcProduct"):
        if prod.Representation:
            print(prod.Representation.Representations[0].RepresentationType)
    tri_verts = []
    semantics = {}

    for prod in ifc.by_type("IfcProduct"):
        if not prod.Representation:
            continue
        gid = prod.GlobalId
        elem_id32 = fast_hash(gid)
        shape = geom.create_shape(settings, prod)
        verts = np.array(shape.geometry.verts).reshape(-1, 3)  # Important reshape
        tags = np.full(len(verts), elem_id32, dtype=np.uint32)

        tri_verts.append(np.rec.fromarrays(
            [verts[:, 0], verts[:, 1], verts[:, 2], tags],
            names="x,y,z,elem_id", formats="f4,f4,f4,u4"
        ))

        # Simple metadata without props
        semantics[str(elem_id32)] = {
            "GlobalId": gid,
            "IfcType": prod.is_a(),
            "Name": prod.Name,
            # no props because ifcopenshell.util.element is missing
        }

    verts_all = np.concatenate(tri_verts)
    ply = plyfile.PlyElement.describe(verts_all, "vertex")
    plyfile.PlyData([ply], text=False).write(str(ply_out))
    json_out.write_text(json.dumps(semantics, indent=2))

if __name__ == "__main__":

    ifc_file   = pathlib.Path(r"C:\Users\wangz\HBIM\AULA_lib.ifc")
    ply_output = pathlib.Path(r"C:\Users\wangz\HBIM\bim_aula1.ply")
    json_output= pathlib.Path(r"C:\Users\wangz\HBIM\bim_aula_semantics1.json")

    collect(ifc_file, ply_output, json_output)
