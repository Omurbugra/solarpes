# Sitenin 3B dosyalarını açık Rhino dokümanından üretir.
#   export_main()    -> site/assets/school.glb + materials.json
#   export_details() -> site/assets/details/<anahtar>.glb + details.json
# Kullanım (Rhino MCP): doc=__rhino_doc__; exec(detail_lib); exec(build_details); exec(bu dosya); export_main(); export_details()
import os
import json
import shutil
import collections

SITE = r"C:\Users\Synho\Documents\Solarpes\site\assets"

GROUPS = [
    ("wall", ["SCHOOL_BUILDING::Walls_Plaster", "SCHOOL_BUILDING::Stone_Trim", "SCHOOL_FACADE_DETAILS::Vertical_Pilasters",
              "SCHOOL_FACADE_DETAILS::Pilaster_Joints", "SCHOOL_FACADE_DETAILS::Upper_Window_Bands"]),
    ("roof", ["SCHOOL_BUILDING::Roof_Tile"]),
    ("ground", ["SCHOOL_GROUND_FLOOR"]),
    ("window", ["SCHOOL_BUILDING::Glass", "SCHOOL_BUILDING::Window_Frame"]),
    ("shading", ["SCHOOL_SHADING::South_Horizontal", "SCHOOL_SHADING::East_Fins", "SCHOOL_SHADING::West_Fins"]),
    ("heatpump", ["SCHOOL_VRF"]),
    ("pvroof", ["SCHOOL_PV"]),
    ("pvshade", ["SCHOOL_SHADING::South_PV_Canopies"]),
    ("pvpark", ["SCHOOL_YARD::Parking_SE::PV_Modules", "SCHOOL_YARD::Parking_SE::Steel",
                "SCHOOL_YARD::Parking_SE::Electrical", "SCHOOL_YARD::Parking_SE::Lighting"]),
]
# Yalnızca çok ağır dekoratif objeler hafifçe seyreltilir.
REDUCE = {"SCHOOL_YARD::Bicycles": .3, "SCHOOL_YARD::Trees_Crown": .55, "SCHOOL_VRF::Front_Details::Fans": .45, "SCHOOL_YARD::People": .6}
BUST_RED = .18
SKIP = ("_REMOVED", "DETAILS", "SCHOOL_BUILDING::Interior")


def _grp(path):
    if path.startswith(SKIP):
        return None
    for g, ps in GROUPS:
        for p in ps:
            if path == p or path.startswith(p + "::"):
                return g
    return "ctx"


def _objmat(o, parent):
    a = o.Attributes
    src = a.MaterialSource
    if src == DO.ObjectMaterialSource.MaterialFromParent and parent is not None:
        return parent
    idx = a.MaterialIndex if src == DO.ObjectMaterialSource.MaterialFromObject else doc.Layers[a.LayerIndex].RenderMaterialIndex
    if idx >= 0:
        return doc.Materials[idx]
    col = a.ObjectColor if a.ColorSource == DO.ObjectColorSource.ColorFromObject else doc.Layers[a.LayerIndex].Color
    return ("col_%02x%02x%02x" % (col.R, col.G, col.B), col)


def _mname(m):
    return m[0] if isinstance(m, tuple) else (m.Name or ("m%d" % m.Index))


def _mesh_of(o, red, mat, mp, cache):
    k = (o.Id, red, _mname(mat))
    if k in cache:
        return cache[k]
    rm = list(o.GetMeshes(RG.MeshType.Render) or [])
    if not rm:
        g = o.Geometry
        if isinstance(g, RG.Extrusion):
            g = g.ToBrep()
        if isinstance(g, RG.Brep):
            rm = list(RG.Mesh.CreateFromBrep(g, mp) or [])
        elif isinstance(g, RG.Mesh):
            rm = [g]
    out = None
    if rm:
        m = RG.Mesh()
        for x in rm:
            m.Append(x)
        tex = None if isinstance(mat, tuple) else mat.GetTexture(DO.TextureType.Bitmap)
        if tex is not None:
            try:
                res = o.GetTextureMapping(tex.MappingChannelId)
                mapping, xf = res if isinstance(res, tuple) else (res, RG.Transform.Identity)
                if mapping is not None:
                    m.SetTextureCoordinates(mapping, xf, False)
            except Exception:
                pass
        if o.Name == "Ataturk_Bust":
            red = BUST_RED
        if red < 1 and m.Faces.Count > 300:
            try:
                m.Reduce(max(100, int(m.Faces.Count * red)), True, 7, False)
            except Exception:
                pass
        if m.TextureCoordinates.Count != m.Vertices.Count:
            m.TextureCoordinates.Clear()
            for _ in range(m.Vertices.Count):
                m.TextureCoordinates.Add(0.0, 0.0)
        out = m
    cache[k] = out
    return out


def _walk(o, xf, g, red, parent, acc, mats, mp, cache):
    if isinstance(o, DO.InstanceObject):
        x2 = xf * o.InstanceXform
        pm = _objmat(o, parent)
        for c in o.InstanceDefinition.GetObjects():
            _walk(c, x2, g, red, pm, acc, mats, mp, cache)
        return
    mat = _objmat(o, parent)
    n = _mname(mat)
    mats.setdefault(n, mat)
    m = _mesh_of(o, red, mat, mp, cache)
    if m is None:
        return
    d = m.DuplicateMesh()
    d.Transform(xf)
    acc[(g, n)].append(d)


def _write_glb(acc, path):
    hd = Rhino.RhinoDoc.CreateHeadless(None)
    hd.ModelUnitSystem = Rhino.UnitSystem.Meters
    tris = 0
    for (g, n), lst in acc.items():
        m = RG.Mesh()
        for x in lst:
            m.Append(x)
        if m.Normals.Count != m.Vertices.Count:
            m.Normals.ComputeNormals()
        m.Compact()
        a = DO.ObjectAttributes()
        a.Name = g + "__" + n
        hd.Objects.AddMesh(m, a)
        tris += m.Faces.Count
    opt = Rhino.FileIO.FileGltfWriteOptions()
    opt.UseDracoCompression = True
    opt.DracoCompressionLevel = 10
    # 20 bit: ince katmanlar (bayrak ay-yıldızı, çizgiler) yüzeye yapışık kalsın
    opt.DracoQuantizationBitsPosition = 20
    opt.DracoQuantizationBitsNormal = 10
    opt.DracoQuantizationBitsTextureCoordinate = 14
    opt.MapZToY = True
    opt.ExportMaterials = False
    opt.ExportLayers = False
    opt.ExportTextureCoordinates = True
    opt.ExportVertexNormals = True
    opt.CullBackfaces = False
    ok = Rhino.FileIO.FileGltf.Write(path, hd, opt)
    hd.Dispose()
    return ok, tris


def _mat_entry(m):
    if isinstance(m, tuple):
        c = m[1]
        return {"c": [round(c.R / 255., 4), round(c.G / 255., 4), round(c.B / 255., 4)], "m": 0, "r": 1, "o": 1}
    if m.Name in MATS:
        h, op, met, rough, em = MATS[m.Name]
        h = h.lstrip('#')
        e = {"c": [round(int(h[i:i + 2], 16) / 255., 4) for i in (0, 2, 4)], "m": met, "r": rough, "o": op}
        if em:
            e["e"] = 1
        return e
    if m.IsPhysicallyBased:
        pb = m.PhysicallyBased
        c = pb.BaseColor
        e = {"c": [c.R, c.G, c.B], "m": pb.Metallic, "r": pb.Roughness, "o": pb.Opacity}
    else:
        c = m.DiffuseColor
        e = {"c": [c.R / 255., c.G / 255., c.B / 255.], "m": 0, "r": 1 - min(1, m.Shine / 255.), "o": 1 - m.Transparency}
    e = {k: ([round(x, 4) for x in v] if isinstance(v, list) else round(v, 4)) for k, v in e.items()}
    t = m.GetTexture(DO.TextureType.Bitmap)
    if t is not None:
        f = t.FileReference.FullPath if t.FileReference else t.FileName
        if f and os.path.exists(f):
            fn = os.path.basename(f)
            jpg = os.path.splitext(fn)[0] + '.jpg'
            if os.path.exists(os.path.join(SITE, 'tex', jpg)):
                fn = jpg                       # daha önce web için küçültülmüş sürüm
            elif not os.path.exists(os.path.join(SITE, 'tex', fn)):
                shutil.copyfile(f, os.path.join(SITE, 'tex', fn))
            u = t.UvwTransform
            e["map"] = fn
            e["rep"] = [round(u.M00, 5), round(u.M11, 5)]
            e["off"] = [round(u.M03, 5), round(u.M13, 5)]
    return e


def export_main():
    mp = doc.GetMeshingParameters(doc.MeshingParameterStyle)
    acc = collections.defaultdict(list)
    mats = {}
    cache = {}
    for o in doc.Objects:
        l = doc.Layers[o.Attributes.LayerIndex]
        if not l.IsVisible or o.IsHidden or o.ObjectType == DO.ObjectType.TextDot:
            continue
        path = l.FullPath
        g = _grp(path)
        if g is None:
            continue
        red = 1.0
        for p, f in REDUCE.items():
            if path.startswith(p):
                red = f
        _walk(o, RG.Transform.Identity, g, red, None, acc, mats, mp, cache)
    ok, tris = _write_glb(acc, os.path.join(SITE, "school.glb"))
    json.dump({n: _mat_entry(m) for n, m in mats.items()}, open(os.path.join(SITE, "materials.json"), "w"), indent=0)
    return ok, tris, len(acc)


def _to_three(p, o):
    return [round(p.X - o.X, 4), round(p.Z - o.Z, 4), round(-(p.Y - o.Y), 4)]


def export_details(keys=None):
    out_dir = os.path.join(SITE, "details")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    mp = RG.MeshingParameters.QualityRenderMesh
    info = {"materials": {}, "details": {}}
    res = {}
    for key in keys or ORDER:
        o3 = RG.Point3d(*origin_of(key))
        T = RG.Transform.Translation(-o3.X, -o3.Y, -o3.Z)
        acc = collections.defaultdict(list)
        labels = []
        cache = {}
        mats = {}
        root = "DETAILS::%s::" % key
        for o in doc.Objects:
            path = doc.Layers[o.Attributes.LayerIndex].FullPath
            if not path.startswith(root):
                continue
            if o.ObjectType == DO.ObjectType.TextDot:
                n, _, text = (o.Name or "0|").partition("|")
                labels.append({"n": int(n), "t": text, "p": _to_three(o.Geometry.Point, o3)})
                continue
            mat = _objmat(o, None)
            name = _mname(mat)
            mats.setdefault(name, mat)
            m = _mesh_of(o, 1.0, mat, mp, cache)
            if m is None:
                continue
            d = m.DuplicateMesh()
            d.Transform(T)
            acc[(key, name)].append(d)
        ok, tris = _write_glb(acc, os.path.join(out_dir, key + ".glb"))
        for n, m in mats.items():
            info["materials"][n] = _mat_entry(m)
        info["details"][key] = {"labels": sorted(labels, key=lambda x: x["n"])}
        res[key] = (ok, tris, len(labels))
    p = os.path.join(out_dir, "details.json")
    if keys and os.path.exists(p):
        old = json.load(open(p, encoding="utf-8"))
        old["materials"].update(info["materials"])
        old["details"].update(info["details"])
        info = old
    json.dump(info, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return res
