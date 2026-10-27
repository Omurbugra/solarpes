# Rhino 8 (CPython) yardımcıları: detay modelleri için katman, malzeme ve geometri.
# Rhino MCP üzerinden exec ile yüklenir; `doc` global olarak verilmelidir.
import math
import Rhino
import System

RG = Rhino.Geometry
DO = Rhino.DocObjects

# ad: (sRGB hex, opaklık, metalik, pürüzlülük, emisyon)
MATS = {
    'D_Plaster_Int': ('#efece6', 1, 0, .95, 0),
    'D_Brick': ('#b4603f', 1, 0, .9, 0),
    'D_Mortar': ('#c9c2b4', 1, 0, .95, 0),
    'D_Adhesive': ('#bdb8ad', 1, 0, .95, 0),
    'D_EPS': ('#a3a8ab', 1, 0, .9, 0),
    'D_Dowel': ('#f4f3ee', 1, 0, .6, 0),
    'D_Basecoat': ('#d7d3ca', 1, 0, .95, 0),
    'D_Mesh': ('#e9e2b4', .75, 0, .8, 0),
    'D_Finish': ('#e6dcc9', 1, 0, .95, 0),
    'D_Alu': ('#b9c0c6', 1, .6, .4, 0),
    'D_RC': ('#a9a9a3', 1, 0, .9, 0),
    'D_Rebar': ('#6e5b4b', 1, .4, .6, 0),
    'D_VaporBarrier': ('#5f86ad', 1, .1, .5, 0),
    'D_Rockwool': ('#d8b55c', 1, 0, 1, 0),
    'D_Timber': ('#c69c65', 1, 0, .85, 0),
    'D_OSB': ('#d2aa6e', 1, 0, .9, 0),
    'D_Membrane': ('#3c4b56', 1, 0, .7, 0),
    'D_Batten': ('#b4875a', 1, 0, .85, 0),
    'D_ClayTile': ('#c8714a', 1, 0, .8, 0),
    'D_Soil': ('#6e5a45', 1, 0, 1, 0),
    'D_Gravel': ('#9c968c', 1, 0, 1, 0),
    'D_LeanConcrete': ('#b5b2aa', 1, 0, .95, 0),
    'D_Bitumen': ('#272727', 1, 0, .6, 0),
    'D_XPS': ('#8fbcd8', 1, 0, .8, 0),
    'D_PE': ('#dce8ee', .6, 0, .3, 0),
    'D_Screed': ('#c4c0b6', 1, 0, .95, 0),
    'D_FloorTile': ('#e8e2d4', 1, 0, .4, 0),
    'D_PVC': ('#f2f2ef', 1, 0, .5, 0),
    'D_Steel_Reinf': ('#8b9399', 1, .7, .4, 0),
    'D_Glass': ('#a9c8d6', .28, .1, .05, 0),
    'D_LowE': ('#9fc3a8', .32, .2, .05, 0),
    'D_Spacer': ('#2b2f33', 1, .3, .5, 0),
    'D_Gasket': ('#1b1b1b', 1, 0, .8, 0),
    'D_Marble': ('#ece8df', 1, 0, .3, 0),
    'D_Steel': ('#4a5258', 1, .5, .45, 0),
    'D_Galv': ('#a6acb0', 1, .7, .35, 0),
    'D_PV_Cell': ('#1d2c55', 1, .2, .3, 0),
    'D_PV_Busbar': ('#d9dde0', 1, .6, .3, 0),
    'D_PV_Back': ('#f0f0f0', 1, 0, .7, 0),
    'D_PV_Frame': ('#a9b1b8', 1, .7, .35, 0),
    'D_PV_Glass': ('#cfe0ea', .16, .1, .03, 0),
    'D_Casing': ('#e4e5e1', 1, .1, .5, 0),
    'D_Coil': ('#9aa4aa', 1, .6, .4, 0),
    'D_Fan': ('#3a4046', 1, .1, .6, 0),
    'D_Guard': ('#2e3338', 1, .4, .5, 0),
    'D_Copper': ('#b87333', 1, .8, .35, 0),
    'D_Armaflex': ('#1f1f1f', 1, 0, .9, 0),
    'D_Brass': ('#b8a05a', 1, .7, .35, 0),
    'D_Rubber': ('#1d1d1d', 1, 0, .9, 0),
    'D_Concrete': ('#b9b6ae', 1, 0, .95, 0),
    'D_Sun': ('#f2b134', 1, 0, .5, 1),
    'D_Ray_Summer': ('#e8781e', 1, 0, .5, 1),
    'D_Ray_Winter': ('#f2c34a', 1, 0, .5, 1),
    'D_Cable': ('#151515', 1, 0, .7, 0),
    'D_JBox': ('#2a2a2a', 1, 0, .6, 0),
    'D_LED': ('#fff6dc', 1, 0, .5, 1),
    'D_Frame_Dark': ('#2f3338', 1, .3, .5, 0),
    'D_Wall': ('#e2dccf', 1, 0, .95, 0),
}


def _col(h):
    h = h.lstrip('#')
    return System.Drawing.Color.FromArgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def mat_index(name):
    for m in doc.Materials:
        if not m.IsDeleted and m.Name == name:
            return m.Index
    hexc, op, met, rough, em = MATS[name]
    m = DO.Material()
    m.Name = name
    m.DiffuseColor = _col(hexc)
    m.Transparency = 1 - op
    m.Shine = (1 - rough) * DO.Material.MaxShine
    if em:
        m.EmissionColor = _col(hexc)
    return doc.Materials.Add(m)


def layer(path):
    parent = System.Guid.Empty
    idx = -1
    acc = []
    for part in path.split('::'):
        acc.append(part)
        full = '::'.join(acc)
        idx = doc.Layers.FindByFullPath(full, -1)
        if idx < 0:
            L = DO.Layer()
            L.Name = part
            L.ParentLayerId = parent
            idx = doc.Layers.Add(L)
        parent = doc.Layers[idx].Id
    return idx


# --- yerel çerçeve yığını: add() geometriyi mevcut dönüşümle yerleştirir ---
_stack = [RG.Transform.Identity]
KEY = ['']
ORIGIN = [RG.Point3d(0, 0, 0)]


def push(T):
    _stack.append(_stack[-1] * T)


def pop():
    _stack.pop()


def cur():
    return RG.Transform.Translation(RG.Vector3d(ORIGIN[0])) * _stack[-1]


def add(geo, mat, name=None):
    if geo is None:
        return None
    g = geo.Duplicate() if hasattr(geo, 'Duplicate') else geo
    g.Transform(cur())
    a = DO.ObjectAttributes()
    a.LayerIndex = layer('DETAILS::%s::%s' % (KEY[0], mat))
    a.MaterialSource = DO.ObjectMaterialSource.MaterialFromObject
    a.MaterialIndex = mat_index(mat)
    if name:
        a.Name = name
    return doc.Objects.Add(g, a)


def dot(n, text, p):
    pt = RG.Point3d(*p)
    pt.Transform(cur())
    a = DO.ObjectAttributes()
    a.LayerIndex = layer('DETAILS::%s::_Labels' % KEY[0])
    d = RG.TextDot('%d' % n, pt)
    d.SecondaryText = text
    a.Name = '%d|%s' % (n, text)
    doc.Objects.AddTextDot(d, a)


def begin(key, origin):
    """Detayı (yeniden) kur: önce bu anahtarın eski objelerini sil."""
    KEY[0] = key
    ORIGIN[0] = RG.Point3d(*origin)
    del _stack[1:]
    root = 'DETAILS::%s' % key
    ids = [o.Id for o in doc.Objects if doc.Layers[o.Attributes.LayerIndex].FullPath.startswith(root)]
    for i in ids:
        doc.Objects.Delete(i, True)
    layer(root)


# --- geometri ---
def box(x0, y0, z0, x1, y1, z1):
    return RG.Box(RG.BoundingBox(RG.Point3d(min(x0, x1), min(y0, y1), min(z0, z1)),
                                 RG.Point3d(max(x0, x1), max(y0, y1), max(z0, z1)))).ToBrep()


def cyl(p0, p1, r):
    a = RG.Point3d(*p0)
    b = RG.Point3d(*p1)
    v = b - a
    return RG.Cylinder(RG.Circle(RG.Plane(a, v), r), v.Length).ToBrep(True, True)


def torus(center, normal, R, r):
    return RG.Torus(RG.Plane(RG.Point3d(*center), RG.Vector3d(*normal)), R, r).ToRevSurface().ToBrep()


def sphere(c, r):
    return RG.Sphere(RG.Point3d(*c), r).ToBrep()


def prism(pts, origin, xaxis, yaxis, length, holes=()):
    """(u,v) kesit noktaları -> origin/xaxis/yaxis düzleminde profil, düzlem normali (x × y)
    boyunca `length` kadar ekstrüzyon. holes: iç boşluk profilleri (PVC odacıkları gibi)."""
    pl = RG.Plane(RG.Point3d(*origin), RG.Vector3d(*xaxis), RG.Vector3d(*yaxis))
    def crv(ps):
        return RG.PolylineCurve([pl.PointAt(u, v) for (u, v) in ps] + [pl.PointAt(*ps[0])])
    tol = doc.ModelAbsoluteTolerance
    pb = RG.Brep.CreatePlanarBreps([crv(pts)] + [crv(h) for h in holes], tol)[0]
    path = RG.LineCurve(pl.Origin, pl.Origin + pl.ZAxis * length)
    return pb.Faces[0].CreateExtrusion(path, True)


def rot(deg, axis, center=(0, 0, 0)):
    return RG.Transform.Rotation(math.radians(deg), RG.Vector3d(*axis), RG.Point3d(*center))


def move(x, y, z):
    return RG.Transform.Translation(x, y, z)


def frame(origin, xaxis, yaxis):
    """Yerel (x,y,z) -> verilen düzlem (eğimli yüzeyler için)."""
    return RG.Transform.PlaneToPlane(RG.Plane.WorldXY, RG.Plane(RG.Point3d(*origin), RG.Vector3d(*xaxis), RG.Vector3d(*yaxis)))


def bool_diff(a, cutters):
    res = RG.Brep.CreateBooleanDifference([a], cutters, doc.ModelAbsoluteTolerance)
    return res[0] if res and len(res) else a


def pv_module(L=1.722, W=1.134, T=0.035, cells_l=10, cells_w=6, jbox=True):
    """Yerel çerçevede tek PV modül: x boyunca L, y boyunca W, z kalınlık (alt yüz z=0)."""
    f = 0.035
    add(box(0, 0, 0, L, f, T), 'D_PV_Frame')
    add(box(0, W - f, 0, L, W, T), 'D_PV_Frame')
    add(box(0, f, 0, f, W - f, T), 'D_PV_Frame')
    add(box(L - f, f, 0, L, W - f, T), 'D_PV_Frame')
    add(box(f, f, T - 0.008, L - f, W - f, T - 0.006), 'D_PV_Back')
    gap = 0.003
    cl = (L - 2 * f - 0.02 - gap * (cells_l - 1)) / cells_l
    cw = (W - 2 * f - 0.02 - gap * (cells_w - 1)) / cells_w
    for i in range(cells_l):
        for j in range(cells_w):
            x0 = f + 0.01 + i * (cl + gap)
            y0 = f + 0.01 + j * (cw + gap)
            add(box(x0, y0, T - 0.006, x0 + cl, y0 + cw, T - 0.0045), 'D_PV_Cell')
    for j in range(cells_w):
        yc = f + 0.01 + j * (cw + gap)
        for t in (0.3, 0.7):
            y = yc + cw * t
            add(box(f + 0.01, y - 0.0008, T - 0.0045, L - f - 0.01, y + 0.0008, T - 0.004), 'D_PV_Busbar')
    add(box(f, f, T - 0.0035, L - f, W - f, T - 0.0005), 'D_PV_Glass')
    if jbox:
        add(box(L - 0.25, W / 2 - 0.06, -0.018, L - 0.13, W / 2 + 0.06, 0.0), 'D_JBox')
        for s in (-1, 1):
            y = W / 2 + s * 0.04
            add(cyl((L - 0.13, y, -0.01), (L + 0.05, y, -0.01), 0.003), 'D_Cable')
