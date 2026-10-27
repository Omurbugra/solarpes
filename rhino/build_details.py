# Yan panelde gösterilen teknik detay modelleri. Her detay DETAILS::<anahtar>::<malzeme> katmanlarında,
# sahanın kuzeyinde bir sıra halinde kurulur. Yerel eksenler: x sağ, y derinlik (+ içeri / arka), z yukarı;
# bina dışı -y yönündedir. Ölçüler metre. Etiketler TextDot ("no|metin") olarak _Labels katmanındadır.
# Kullanım (Rhino MCP): doc=__rhino_doc__; exec(lib); exec(bu dosya); build_all()
import math

ROW_Y = 58.0
ORDER = ['wall', 'roof', 'ground', 'window', 'shading', 'heatpump', 'pvroof', 'pvshade', 'pvpark']


def origin_of(key):
    return (-52.0 + ORDER.index(key) * 11.0, ROW_Y, 0.0)


def ellipse_pts(a, b, n=20):
    return [(a * math.cos(2 * math.pi * i / n), b * math.sin(2 * math.pi * i / n)) for i in range(n)]


# ---------------------------------------------------------------- 1. Duvar (mantolama)
def build_wall():
    begin('wall', origin_of('wall'))
    W, H = 1.4, 1.3
    # iç sıva + tuğla duvar (harç yatağı üzerinde tuğla örgü)
    add(box(0, 0.19, 0, W, 0.21, H), 'D_Plaster_Int')
    add(box(0, 0.006, 0, W, 0.185, H), 'D_Mortar')
    pitch_z, pitch_x, bh, bl = 0.145, 0.30, 0.135, 0.29
    row = 0
    z = 0.005
    while z + bh <= H + 1e-6:
        off = 0 if row % 2 == 0 else -0.15
        x = off
        while x < W:
            x0, x1 = max(0, x), min(W, x + bl)
            if x1 - x0 > 0.02:
                add(box(x0, 0, z, x1, 0.19, z + bh), 'D_Brick')
            x += pitch_x
        z += pitch_z
        row += 1
    # yapıştırma harcı + EPS levhalar (subasman profilinden başlar)
    ew, eh, z0 = 1.10, 1.00, 0.08
    add(box(0, -0.006, z0, ew, 0, eh), 'D_Adhesive')
    for (xa, xb, za, zb) in [(0, 0.5, z0, 0.54), (0.502, ew, z0, 0.54), (0, 0.25, 0.542, eh), (0.252, 0.752, 0.542, eh), (0.754, ew, 0.542, eh)]:
        add(box(xa, -0.086, za, xb, -0.006, zb), 'D_EPS')
    # dübeller (görünür EPS şeridinde)
    for (x, zz) in [(0.97, 0.30), (0.97, 0.66), (0.62, 0.90), (0.28, 0.90), (0.97, 0.90)]:
        add(cyl((x, -0.088, zz), (x, -0.084, zz), 0.03), 'D_Dowel')
        add(cyl((x, -0.084, zz), (x, 0.06, zz), 0.0045), 'D_Dowel')
    # subasman profili (alüminyum, damlalıklı)
    add(box(0, -0.088, z0 - 0.004, ew, -0.006, z0), 'D_Alu')
    add(box(0, -0.090, z0 - 0.03, ew, -0.088, z0), 'D_Alu')
    # file + alt kat sıva, son kat sıva (kademeli soyulmuş)
    add(box(0, -0.090, z0 - 0.03, 0.85, -0.086, 0.78), 'D_Basecoat')
    add(box(0, -0.0905, z0 - 0.03, 0.90, -0.0895, 0.82), 'D_Mesh')
    add(box(0, -0.093, z0 - 0.03, 0.65, -0.090, 0.60), 'D_Finish')
    dot(1, 'İç sıva 2 cm', (1.2, 0.21, 1.15))
    dot(2, 'Tuğla duvar 19 cm', (1.25, -0.002, 1.15))
    dot(3, 'Yapıştırma harcı', (1.10, -0.004, 0.45))
    dot(4, 'EPS ısı yalıtım levhası 8 cm', (1.0, -0.087, 0.45))
    dot(5, 'Yalıtım dübeli', (0.62, -0.09, 0.90))
    dot(6, 'Cam elyaf file + alt kat sıva', (0.80, -0.091, 0.70))
    dot(7, 'Son kat dekoratif sıva', (0.35, -0.094, 0.40))
    dot(8, 'Subasman profili', (0.95, -0.091, 0.06))


# ---------------------------------------------------------------- 2. Çatı (soğuk çatı, döşeme üstü yalıtım)
def build_roof():
    begin('roof', origin_of('roof'))
    L, D = 1.6, 1.2
    add(box(0, 0, -0.015, L, D, 0), 'D_Plaster_Int')
    add(box(0, 0, 0, L, D, 0.15), 'D_RC')
    for i in range(8):
        y = 0.075 + i * 0.15
        add(cyl((0, y, 0.03), (L, y, 0.03), 0.006), 'D_Rebar')
    add(box(0.1, 0, 0.15, 1.45, D, 0.152), 'D_VaporBarrier')
    # taşyünü iki kat, derzleri şaşırtmalı
    for (xa, xb) in [(0.1, 0.7), (0.702, 1.30)]:
        add(box(xa, 0, 0.152, xb, D, 0.222), 'D_Rockwool')
    for (xa, xb) in [(0.1, 0.4), (0.402, 1.0), (1.002, 1.15)]:
        add(box(xa, 0, 0.222, xb, D, 0.292), 'D_Rockwool')
    # taban kirişi, dikme, aşık
    add(box(0, 0, 0.15, 0.1, D, 0.46), 'D_Timber')
    add(box(1.0, 0.55, 0.15, 1.1, 0.65, 0.84), 'D_Timber')
    add(box(0.98, 0, 0.84, 1.12, D, 0.98), 'D_Timber')
    # eğimli katmanlar: 30°, yerel s (eğim boyunca), v (=y), t (yüzeye dik)
    a = math.radians(30)
    T = frame((0, 0, 0.40), (math.cos(a), 0, math.sin(a)), (0, 1, 0))
    push(T)
    for v in (0.05, 0.55, 1.05):
        add(box(0, v, 0, 1.75, v + 0.05, 0.12), 'D_Timber')          # mertek 5x12
    add(box(0, 0, 0.12, 1.55, D, 0.138), 'D_OSB')
    add(box(0, 0, 0.138, 1.40, D, 0.140), 'D_Membrane')
    for v in (0.05, 0.55, 1.05):
        add(box(0, v, 0.140, 1.25, v + 0.05, 0.165), 'D_Batten')     # karşı çıta
    s = 0.05
    while s < 1.25:
        add(box(s, 0, 0.165, s + 0.05, D, 0.195), 'D_Batten')       # çıta
        s += 0.33
    # kil kiremit sıraları (bindirmeli)
    for r in range(3):
        s0 = 0.02 + r * 0.33
        for c in range(5):
            v0 = c * 0.245
            add(box(s0, v0, 0.195, s0 + 0.42, v0 + 0.24, 0.212), 'D_ClayTile')
            for rib in (0.06, 0.18):
                add(cyl((s0, v0 + rib, 0.212), (s0 + 0.42, v0 + rib, 0.212), 0.012), 'D_ClayTile')
    dot(5, 'Mertek 5×12 cm', (1.70, 0.075, 0.06))
    dot(6, 'OSB 18 mm', (1.48, 0.6, 0.138))
    dot(7, 'Su yalıtım örtüsü', (1.33, 0.6, 0.140))
    dot(8, 'Çıta ve karşı çıta', (1.18, 0.075, 0.165))
    dot(9, 'Kil kiremit', (0.5, 0.6, 0.225))
    pop()
    dot(1, 'Betonarme döşeme 15 cm', (1.55, 0.0, 0.08))
    dot(2, 'Buhar dengeleyici örtü', (1.40, 0.0, 0.151))
    dot(3, 'Taşyünü 2 × 7 cm', (1.20, 0.0, 0.20))
    dot(4, 'Ahşap dikme ve aşık', (1.05, 0.0, 0.92))


# ---------------------------------------------------------------- 3. Zemin (toprağa oturan döşeme)
def build_ground():
    begin('ground', origin_of('ground'))
    D = 1.2
    layers = [
        ('D_Soil', -0.78, -0.58, 1.60), ('D_Gravel', -0.58, -0.43, 1.50), ('D_LeanConcrete', -0.43, -0.33, 1.40),
        ('D_Bitumen', -0.33, -0.322, 1.30), ('D_PE', -0.222, -0.220, 1.10), ('D_RC', -0.220, -0.070, 1.00),
        ('D_Screed', -0.070, -0.020, 0.85),
    ]
    for m, zb, zt, x1 in layers:
        add(box(0, 0, zb, x1, D, zt), m)
    for (xa, xb) in [(0, 0.6), (0.602, 1.20)]:
        add(box(xa, 0, -0.322, xb, D, -0.222), 'D_XPS')
    # hasır donatı
    for i in range(7):
        y = 0.075 + i * 0.15
        add(cyl((0, y, -0.18), (1.0, y, -0.18), 0.005), 'D_Rebar')
        add(cyl((0, y, -0.11), (1.0, y, -0.11), 0.005), 'D_Rebar')
    for i in range(6):
        x = 0.075 + i * 0.15
        add(cyl((x, 0, -0.17), (x, D, -0.17), 0.005), 'D_Rebar')
        add(cyl((x, 0, -0.10), (x, D, -0.10), 0.005), 'D_Rebar')
    # seramik
    for i in range(2):
        for j in range(4):
            x0, y0 = i * 0.303, j * 0.303
            add(box(x0, y0, -0.020, min(x0 + 0.30, 0.70), min(y0 + 0.30, D), 0), 'D_FloorTile')
    dot(1, 'Seramik kaplama', (0.35, 0.0, -0.01))
    dot(2, 'Şap 5 cm', (0.80, 0.0, -0.045))
    dot(3, 'Betonarme döşeme 15 cm', (0.95, 0.0, -0.145))
    dot(4, 'PE ayırıcı örtü', (1.05, 0.0, -0.221))
    dot(5, 'XPS ısı yalıtımı 10 cm', (1.15, 0.0, -0.27))
    dot(6, 'Bitümlü su yalıtımı', (1.25, 0.0, -0.326))
    dot(7, 'Grobeton 10 cm', (1.35, 0.0, -0.38))
    dot(8, 'Kırma taş dolgu 15 cm', (1.45, 0.0, -0.50))
    dot(9, 'Sıkıştırılmış zemin', (1.55, 0.0, -0.68))


# ---------------------------------------------------------------- 4. Pencere (PVC, üçlü cam) - köşe kesiti
def build_window():
    begin('window', origin_of('window'))
    Hc = 0.9  # kesit yüksekliği (pencerenin alt köşesi)
    # duvar: pencere solunda tuğla + parapet
    add(box(-0.45, 0, -0.35, 0, 0.19, Hc), 'D_Brick')
    add(box(-0.45, 0, -0.35, 0.9, 0.19, -0.06), 'D_Brick')
    add(box(-0.45, 0.19, -0.35, 0, 0.21, Hc), 'D_Plaster_Int')
    add(box(-0.45, -0.086, -0.35, -0.0, -0.006, Hc), 'D_EPS')
    add(box(-0.45, -0.091, -0.35, -0.0, -0.086, Hc), 'D_Finish')
    add(box(-0.0, -0.086, 0.0, 0.03, -0.006, Hc), 'D_EPS')       # sövede yalıtım dönüşü
    add(box(-0.45, -0.086, -0.35, 0.9, -0.006, -0.12), 'D_EPS')
    # PVC kasa: düşey kasa çok odacıklı profil olarak, z boyunca
    fy0, fy1, fw = 0.0, 0.07, 0.07
    outer = [(0, fy0), (fw, fy0), (fw, fy1), (0, fy1)]
    holes = [[(0.006, 0.006), (0.030, 0.006), (0.030, 0.064), (0.006, 0.064)],
             [(0.034, 0.006), (0.064, 0.006), (0.064, 0.030), (0.034, 0.030)],
             [(0.034, 0.034), (0.064, 0.034), (0.064, 0.064), (0.034, 0.064)]]
    add(prism(outer, (0, 0, 0), (1, 0, 0), (0, 1, 0), Hc, holes), 'D_PVC')
    add(box(0.012, 0.012, 0, 0.026, 0.058, Hc), 'D_Steel_Reinf')    # galvaniz takviye
    add(box(fw, fy0, 0, 0.9, fy1, fw), 'D_PVC')                       # alt kasa
    # kanat
    souter = [(0.06, -0.005), (0.13, -0.005), (0.13, 0.075), (0.06, 0.075)]
    sholes = [[(0.068, 0.002), (0.095, 0.002), (0.095, 0.068), (0.068, 0.068)],
              [(0.099, 0.002), (0.122, 0.002), (0.122, 0.012), (0.099, 0.012)]]
    add(prism(souter, (0, 0, 0.06), (1, 0, 0), (0, 1, 0), Hc - 0.06, sholes), 'D_PVC')
    add(box(0.13, -0.005, 0.06, 0.9, 0.075, 0.13), 'D_PVC')
    # üçlü cam 4-16-4-16-4
    gx0, gz0 = 0.112, 0.112
    for (ya, yb, m) in [(0.013, 0.017, 'D_Glass'), (0.033, 0.037, 'D_LowE'), (0.053, 0.057, 'D_LowE')]:
        add(box(gx0, ya, gz0, 0.9, yb, Hc), m)
    for (ya, yb) in [(0.017, 0.033), (0.037, 0.053)]:
        add(box(gx0, ya, gz0, gx0 + 0.012, yb, Hc), 'D_Spacer')
        add(box(gx0, ya, gz0, 0.9, yb, gz0 + 0.012), 'D_Spacer')
    add(box(gx0 - 0.004, 0.013, gz0 - 0.004, gx0, 0.057, Hc), 'D_Gasket')
    for y in (0.009, 0.057):
        add(box(0.125, y, 0.125, 0.135, y + 0.004, Hc), 'D_Gasket')
    # denizlikler
    add(box(-0.02, -0.15, -0.045, 0.9, 0.0, -0.03), 'D_Alu')
    add(box(-0.02, -0.15, -0.07, 0.9, -0.145, -0.03), 'D_Alu')
    add(box(0.0, 0.07, -0.03, 0.9, 0.26, 0.0), 'D_Marble')
    dot(1, 'Çok odacıklı PVC kasa', (0.035, 0.035, Hc))
    dot(2, 'Galvaniz çelik takviye', (0.019, 0.035, Hc + 0.002))
    dot(3, 'Kanat profili', (0.08, 0.07, Hc))
    dot(4, 'Üçlü cam 4-16-4-16-4', (0.4, 0.0, Hc))
    dot(5, 'Argon gazı dolgulu boşluk', (0.5, 0.025, Hc))
    dot(6, 'Low-e kaplama', (0.6, 0.045, Hc))
    dot(7, 'Sıcak kenar çıtası', (0.118, 0.045, 0.6))
    dot(8, 'EPDM conta', (0.13, 0.059, 0.5))
    dot(9, 'Alüminyum dış denizlik', (0.5, -0.12, -0.03))
    dot(10, 'Sövede yalıtım dönüşü', (0.015, -0.05, 0.7))


# ---------------------------------------------------------------- 5. Güneş gölgelemesi (yatay kanatlı saçak)
def build_shading():
    begin('shading', origin_of('shading'))
    W, H = 2.0, 2.6
    ox0, ox1, oz0, oz1 = 0.30, 1.70, 0.80, 2.20
    for b in [(0, 0, 0, ox0, 0.30, H), (ox1, 0, 0, W, 0.30, H), (ox0, 0, 0, ox1, 0.30, oz0), (ox0, 0, oz1, ox1, 0.30, H)]:
        add(box(*b), 'D_Wall')
    add(box(ox0, 0.08, oz0, ox1, 0.15, oz1), 'D_Frame_Dark')
    add(box(ox0 + 0.06, 0.10, oz0 + 0.06, ox1 - 0.06, 0.13, oz1 - 0.06), 'D_Glass')
    add(box(ox0 - 0.02, -0.06, oz0 - 0.04, ox1 + 0.02, 0.08, oz0 - 0.02), 'D_Alu')
    # konsollar + kanatlar
    zc = 2.36
    for x in (0.35, 1.65):
        add(box(x - 0.06, -0.012, zc - 0.10, x + 0.06, 0, zc + 0.18), 'D_Steel')            # duvar plakası
        add(box(x - 0.006, -0.80, zc - 0.03, x + 0.006, -0.012, zc + 0.05), 'D_Steel')      # konsol
        p0, p1 = (x, -0.012, zc + 0.16), (x, -0.70, zc + 0.05)
        add(cyl(p0, p1, 0.008), 'D_Steel')                                                 # gergi
    for i in range(6):
        y = -0.13 - i * 0.12
        blade = prism(ellipse_pts(0.075, 0.012), (0.25, y, zc + 0.07), (0, 1, 0), (0, 0, 1), 1.5)
        blade.Transform(rot(-25, (1, 0, 0), (0.25, y, zc + 0.07)))
        add(blade, 'D_Alu')
    # doğu/batı için örnek düşey kanat
    add(box(1.86, -0.50, 0.70, 1.88, 0, 2.40), 'D_Alu')
    # güneş ışınları (Ankara, öğle): yaz 73°, kış 27°
    def ray(alt, target, m, length):
        a = math.radians(alt)
        d = (0, -math.cos(a), math.sin(a))
        start = (target[0], target[1] + d[1] * length, target[2] + d[2] * length)
        add(cyl(start, target, 0.010), m)
        add(sphere(start, 0.05), 'D_Sun')
    ray(73.5, (1.0, -0.80, zc + 0.10), 'D_Ray_Summer', 1.2)
    ray(26.6, (1.0, 0.10, 1.65), 'D_Ray_Winter', 2.6)
    dot(1, 'Alüminyum aerodinamik kanatlar', (0.6, -0.50, zc + 0.09))
    dot(2, 'Çelik konsol ve gergi', (1.65, -0.40, zc + 0.12))
    dot(3, 'Duvar bağlantı plakası', (0.35, -0.013, zc + 0.15))
    dot(4, 'Yaz güneşi 73° — kesilir', (1.0, -1.0, zc + 0.8))
    dot(5, 'Kış güneşi 27° — içeri girer', (1.0, -1.6, 2.4))
    dot(6, 'Düşey kanat (doğu/batı)', (1.87, -0.3, 1.6))


# ---------------------------------------------------------------- 6. Isı pompası (VRF dış ünite, yandan üflemeli)
def build_heatpump():
    begin('heatpump', origin_of('heatpump'))
    W, Dp, Hh = 0.94, 0.46, 1.615
    z0 = 0.09
    add(box(-0.20, -0.25, -0.15, W + 0.35, Dp + 0.20, 0), 'D_Concrete')
    for y in (0.03, 0.37):
        for x in (0.05, W - 0.17):
            add(box(x, y, 0, x + 0.12, y + 0.06, 0.03), 'D_Rubber')
        add(box(0, y, 0.03, W, y + 0.06, z0), 'D_Galv')
    zt = z0 + Hh
    # kasa: ön panel fan delikli
    front = box(0, -0.01, z0, W, 0, zt)
    fans = [z0 + 0.42, z0 + 1.06]
    cut = [cyl((W / 2, -0.02, zf), (W / 2, 0.01, zf), 0.29) for zf in fans]
    add(bool_diff(front, cut), 'D_Casing')
    add(box(0, 0, zt - 0.015, W, Dp, zt), 'D_Casing')
    add(box(W - 0.01, 0, z0, W, Dp, zt - 0.015), 'D_Casing')
    add(box(0, 0, z0, W, Dp, z0 + 0.02), 'D_Casing')
    # batarya (arka + sol yan) lamelleri ve koruma telleri
    add(box(0.01, Dp - 0.035, z0 + 0.02, W - 0.01, Dp - 0.03, zt - 0.015), 'D_Coil')
    x = 0.02
    while x < W - 0.02:
        add(box(x, Dp - 0.03, z0 + 0.03, x + 0.002, Dp - 0.005, zt - 0.02), 'D_Coil')
        x += 0.02
    y = 0.02
    while y < Dp - 0.03:
        add(box(0, y, z0 + 0.03, 0.025, y + 0.002, zt - 0.02), 'D_Coil')
        y += 0.02
    zz = z0 + 0.06
    while zz < zt - 0.02:
        add(cyl((0, Dp, zz), (W, Dp, zz), 0.0025), 'D_Guard')
        add(cyl((-0.002, 0, zz), (-0.002, Dp, zz), 0.0025), 'D_Guard')
        zz += 0.06
    # fanlar: ağız halkası, kanatlar, göbek, koruma ızgarası
    for zf in fans:
        c = (W / 2, 0.0, zf)
        add(torus((W / 2, 0.005, zf), (0, 1, 0), 0.285, 0.012), 'D_Fan')
        add(cyl((W / 2, 0.02, zf), (W / 2, 0.11, zf), 0.07), 'D_Fan')
        for k in range(3):
            bl = box(0.06, -0.004, -0.07, 0.26, 0.004, 0.07)
            bl.Transform(rot(22, (1, 0, 0)))
            bl.Transform(rot(k * 120, (0, 1, 0)))
            bl.Transform(move(W / 2, 0.05, zf))
            add(bl, 'D_Fan')
        for R in (0.08, 0.15, 0.22, 0.28):
            add(torus((W / 2, -0.03, zf), (0, 1, 0), R, 0.003), 'D_Guard')
        for k in range(8):
            a = math.radians(k * 45)
            add(cyl((W / 2, -0.03, zf), (W / 2 + 0.28 * math.cos(a), -0.03, zf + 0.28 * math.sin(a)), 0.003), 'D_Guard')
    # servis paneli, vanalar, borular
    add(box(W - 0.24, -0.016, z0 + 0.05, W - 0.02, -0.01, z0 + 0.30), 'D_Casing')
    add(box(W - 0.16, -0.03, z0 + 0.25, W - 0.10, -0.016, z0 + 0.27), 'D_Frame_Dark')
    pipes = [(0.10, 0.0064, 0.022), (0.20, 0.0143, 0.035)]
    for (yy, r_cu, r_in) in pipes:
        zp = z0 + 0.12
        add(box(W, yy - 0.03, zp - 0.03, W + 0.06, yy + 0.03, zp + 0.03), 'D_Brass')
        add(cyl((W + 0.06, yy, zp), (W + 0.12, yy, zp), r_cu), 'D_Copper')
        add(cyl((W + 0.12, yy, zp), (W + 0.30, yy, zp), r_in), 'D_Armaflex')
        add(cyl((W + 0.30, yy, zp), (W + 0.30, yy, -0.10), r_in), 'D_Armaflex')
    add(cyl((W, 0.32, z0 + 0.35), (W + 0.25, 0.32, z0 + 0.35), 0.012), 'D_Cable')
    dot(1, 'Eksenel fan Ø550 + koruma ızgarası', (W / 2 + 0.2, -0.03, fans[1] + 0.2))
    dot(2, 'Lamelli ısı değiştirici (batarya)', (0.3, Dp, z0 + 0.9))
    dot(3, 'Kompresör bölmesi / servis paneli', (W - 0.13, -0.017, z0 + 0.15))
    dot(4, 'Servis vanaları', (W + 0.03, 0.15, z0 + 0.15))
    dot(5, 'Bakır soğutucu hatları (sıvı / gaz)', (W + 0.09, 0.20, z0 + 0.12))
    dot(6, 'Kauçuk boru yalıtımı', (W + 0.30, 0.15, 0.0))
    dot(7, 'Titreşim takozları', (0.11, 0.03, 0.015))
    dot(8, 'Beton kaide', (0.4, -0.25, -0.07))


# ---------------------------------------------------------------- 7. Çatı PV (tek modül, kiremit çatıda)
def build_pvroof():
    begin('pvroof', origin_of('pvroof'))
    a = math.radians(30)
    # yerel: x = eğim boyunca (s, güneye bakan yüzde yukarı), y = yatay (v), z = yüzeye dik (t)
    push(frame((0, 0, 0), (0, math.cos(a), math.sin(a)), (-1, 0, 0)))
    S, V = 2.3, 1.6
    for v in (0.40, 1.20):
        add(box(-0.05, v - 0.03, -0.17, S, v + 0.03, -0.05), 'D_Timber')
    add(box(-0.05, 0, -0.05, S, V, -0.032), 'D_OSB')
    add(box(-0.05, 0, -0.032, S, V, -0.030), 'D_Membrane')
    s = 0.0
    while s < S:
        add(box(s, 0, -0.030, s + 0.05, V, 0.0), 'D_Batten')
        s += 0.33
    hook_s = (0.55, 1.75)
    r = 0
    while r * 0.33 < S - 0.1:
        s0 = r * 0.33
        for c in range(7):
            v0 = c * 0.23
            if v0 > V - 0.05:
                continue
            # kanca altındaki iki kiremit açıkta bırakılır
            skip = r == 1 and c in (1, 2)
            if skip:
                continue
            add(box(s0, v0, 0.0, s0 + 0.42, min(v0 + 0.225, V), 0.017), 'D_ClayTile')
            for rib in (0.055, 0.165):
                if v0 + rib < V:
                    add(cyl((s0, v0 + rib, 0.017), (s0 + 0.42, v0 + rib, 0.017), 0.011), 'D_ClayTile')
        r += 1
    # çatı kancaları: mertek üzerinde taban, kiremidin üstünden dönen kol
    for hs in hook_s:
        for v in (0.40, 1.20):
            add(box(hs - 0.07, v - 0.03, -0.05, hs + 0.07, v + 0.03, -0.044), 'D_Galv')
            add(box(hs + 0.06, v - 0.015, -0.044, hs + 0.067, v + 0.015, 0.06), 'D_Galv')
            add(box(hs - 0.02, v - 0.015, 0.053, hs + 0.067, v + 0.015, 0.06), 'D_Galv')
        add(box(hs - 0.02, 0.05, 0.06, hs + 0.02, V - 0.05, 0.10), 'D_Alu')          # ray
    # modül (dikey): eğim boyunca 1.722, yatay 1.134
    m0s, m0v = 0.30, (V - 1.134) / 2
    push(move(m0s, m0v, 0.10))
    pv_module()
    pop()
    for hs in hook_s:
        for v in (m0v - 0.03, m0v + 1.134):
            add(box(hs - 0.02, v, 0.10, hs + 0.02, v + 0.03, 0.142), 'D_Alu')        # uç kelepçe
    dot(1, 'Monokristal PV modül', (m0s + 1.2, m0v + 0.75, 0.136))
    dot(2, 'Temperli ön cam + hücreler', (m0s + 0.4, m0v + 0.3, 0.136))
    dot(3, 'Alüminyum çerçeve', (m0s + 1.6, m0v + 1.134, 0.12))
    dot(4, 'Uç kelepçe', (hook_s[0], m0v - 0.015, 0.142))
    dot(5, 'Alüminyum montaj rayı', (hook_s[1], V - 0.08, 0.10))
    dot(6, 'Paslanmaz çatı kancası', (0.55, 0.40, 0.0))
    dot(7, 'Kil kiremit', (2.05, 1.45, 0.02))
    dot(8, 'Mertek', (-0.05, 1.20, -0.11))
    pop()


# ---------------------------------------------------------------- 8. Gölgeleme PV (pencere üstü konsol)
def build_pvshade():
    begin('pvshade', origin_of('pvshade'))
    W, H = 2.0, 2.6
    ox0, ox1, oz0, oz1 = 0.30, 1.70, 0.60, 2.00
    for b in [(0, 0, 0, ox0, 0.30, H), (ox1, 0, 0, W, 0.30, H), (ox0, 0, 0, ox1, 0.30, oz0), (ox0, 0, oz1, ox1, 0.30, H)]:
        add(box(*b), 'D_Wall')
    add(box(ox0, 0.08, oz0, ox1, 0.15, oz1), 'D_Frame_Dark')
    add(box(ox0 + 0.06, 0.10, oz0 + 0.06, ox1 - 0.06, 0.13, oz1 - 0.06), 'D_Glass')
    zc = 2.20
    tilt = 15
    for x in (0.45, 1.55):
        add(box(x - 0.08, -0.012, zc - 0.12, x + 0.08, 0, zc + 0.12), 'D_Steel')
        arm = box(x - 0.02, -1.20, -0.03, x + 0.02, 0, 0.03)
        arm.Transform(rot(tilt, (1, 0, 0)))
        arm.Transform(move(0, -0.012, zc))
        add(arm, 'D_Steel')
        tip_y = -0.012 - 1.10 * math.cos(math.radians(tilt))
        tip_z = zc - 1.10 * math.sin(math.radians(tilt))
        add(cyl((x, -0.012, zc + 0.45), (x, tip_y, tip_z + 0.03), 0.008), 'D_Steel')
        add(box(x - 0.06, -0.012, zc + 0.40, x + 0.06, 0, zc + 0.50), 'D_Steel')
    # modül güneye (−y) bakar: dış kenar aşağıda
    T = rot(tilt, (1, 0, 0)) * move(0.14, -1.17, 0.03)
    push(move(0, -0.012, zc) * T)
    pv_module(L=1.722, W=1.134)
    pop()
    add(box(1.75, 0, 0.3, 1.80, -0.04, zc - 0.05), 'D_Frame_Dark')                   # kablo kanalı
    a = math.radians(73.5)
    tgt = (1.0, -0.6, zc - 0.13)
    add(cyl((tgt[0], tgt[1] - math.cos(a) * 1.2, tgt[2] + math.sin(a) * 1.2), tgt, 0.010), 'D_Ray_Summer')
    add(sphere((tgt[0], tgt[1] - math.cos(a) * 1.2, tgt[2] + math.sin(a) * 1.2), 0.05), 'D_Sun')
    dot(1, 'PV modül — saçak olarak', (0.9, -0.6, zc - 0.10))
    dot(2, 'Çelik konsol kol', (1.55, -0.8, zc - 0.25))
    dot(3, 'Gergi çubuğu', (1.55, -0.5, zc + 0.27))
    dot(4, 'Duvar bağlantı plakası (kimyasal dübel)', (0.45, -0.013, zc + 0.08))
    dot(5, 'Kablo kanalı → invertör', (1.775, -0.04, 1.2))
    dot(6, 'Yaz güneşi 73° — pencere gölgede', (1.0, -0.85, zc + 0.9))


# ---------------------------------------------------------------- 9. Otopark PV (tek T-sundurma ünitesi)
def build_pvpark():
    begin('pvpark', origin_of('pvpark'))
    add(box(-0.40, -0.40, -0.60, 0.40, 0.40, 0.10), 'D_Concrete')
    add(box(-0.22, -0.22, 0.10, 0.22, 0.22, 0.125), 'D_Steel')
    for sx in (-1, 1):
        for sy in (-1, 1):
            add(cyl((sx * 0.16, sy * 0.16, 0.0), (sx * 0.16, sy * 0.16, 0.18), 0.012), 'D_Galv')
    # HEA200 kolon
    h, b, tw, tf = 0.19, 0.20, 0.0065, 0.010
    I = [(-b / 2, -h / 2), (b / 2, -h / 2), (b / 2, -h / 2 + tf), (tw / 2, -h / 2 + tf), (tw / 2, h / 2 - tf), (b / 2, h / 2 - tf),
         (b / 2, h / 2), (-b / 2, h / 2), (-b / 2, h / 2 - tf), (-tw / 2, h / 2 - tf), (-tw / 2, -h / 2 + tf), (-b / 2, -h / 2 + tf)]
    add(prism(I, (0, 0, 0.125), (1, 0, 0), (0, 1, 0), 2.75), 'D_Steel')
    # IPE270 konsol kiriş (y boyunca, 5° eğim)
    hb, bb, twb, tfb = 0.27, 0.135, 0.0066, 0.0102
    Ib = [(-bb / 2, -hb / 2), (bb / 2, -hb / 2), (bb / 2, -hb / 2 + tfb), (twb / 2, -hb / 2 + tfb), (twb / 2, hb / 2 - tfb), (bb / 2, hb / 2 - tfb),
          (bb / 2, hb / 2), (-bb / 2, hb / 2), (-bb / 2, hb / 2 - tfb), (-twb / 2, hb / 2 - tfb), (-twb / 2, -hb / 2 + tfb), (-bb / 2, -hb / 2 + tfb)]
    zb = 3.0
    push(move(0, 0, zb) * rot(5, (1, 0, 0)))
    add(prism(Ib, (0, -2.65, 0), (-1, 0, 0), (0, 0, 1), 5.30), 'D_Steel')
    # aşıklar (C profil, x boyunca)
    C = [(0, 0), (0.06, 0), (0.06, 0.015), (0.004, 0.015), (0.004, 0.185), (0.06, 0.185), (0.06, 0.2), (0, 0.2)]
    for y in (-2.25, -0.80, 0.80, 2.25):
        add(prism([(u, v) for (u, v) in C], (-1.75, y - 0.03, hb / 2), (0, 1, 0), (0, 0, 1), 3.50), 'D_Galv')
    # modüller 3 × 3 (dikey)
    zt = hb / 2 + 0.2
    for i in range(3):
        for j in range(3):
            x0 = -1.70 + i * 1.144
            y0 = -2.60 + j * 1.74
            push(move(x0, y0, zt) * rot(90, (0, 0, 1)) * move(0, -1.134, 0))
            pv_module(jbox=(i == 1 and j == 1))
            pop()
    add(box(-0.6, -0.02, -hb / 2 - 0.03, 0.6, 0.02, -hb / 2), 'D_LED')
    pop()
    # köşe bağlantı guseleri
    for s in (-1, 1):
        add(box(-0.004, 0, 2.55, 0.004, s * 0.45, 2.85), 'D_Steel')
    dot(1, 'PV modüller (3 × 3)', (0.0, 0.0, 3.55))
    dot(2, 'Galvaniz C aşık', (1.75, 2.25, 3.25))
    dot(3, 'IPE 270 konsol kiriş', (0.07, -2.0, 2.85))
    dot(4, 'HEA 200 kolon', (0.10, 0.0, 1.6))
    dot(5, 'Taban plakası + ankraj', (0.22, 0.22, 0.12))
    dot(6, 'Betonarme tekil temel', (0.40, -0.4, -0.25))
    dot(7, 'LED aydınlatma', (0.6, 0.0, 2.84))


BUILDERS = {k: globals()['build_' + k] for k in ORDER}


def build_all(keys=None):
    for k in keys or ORDER:
        BUILDERS[k]()
    doc.Views.Redraw()
