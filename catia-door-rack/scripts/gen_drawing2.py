from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (1600, 1150), (255, 255, 255))
d = ImageDraw.Draw(img)


def font(sz, bold=False):
    for p in ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf",
              "C:/Windows/Fonts/simsun.ttc", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


fT = font(30, True); fH = font(20, True); fN = font(17); fS = font(15); fX = font(13)
INK = (10, 10, 10); DIM = (120, 120, 120)


def L(a, b, c=INK, w=2):
    d.line((a[0], a[1], b[0], b[1]), fill=c, width=w)


def R(x0, y0, x1, y1, c=INK, w=2):
    d.rectangle([x0, y0, x1, y1], outline=c, width=w)


def cap(x, y, t, fh=fH):
    d.text((x, y), t, fill=INK, font=fh)


d.text((50, 24), "汽车车门转运车架  总装配工程图", fill=INK, font=fT)
d.text((50, 66), "单位 mm | 空心方管 40×40×2.5 | 比例 1:10 (A3)", fill=DIM, font=fN)

# ============ A3 图框 ============
R(30, 100, 1570, 1120, INK, 2)
R(44, 114, 1556, 1106, INK, 1)

# ============ FRONT VIEW (X-Z) : accurate, scaled ============
sx = 0.40; szz = 0.42; fx0 = 90; fz0 = 700
def Fx(mm): return fx0 + mm * sx
def Fz(mm): return fz0 - mm * szz
cap(90, 720, "主视图 (前)", fH)
# bottom beam, top beam, end posts
R(Fx(18), Fz(800), Fx(2382), Fz(760), INK, 2)
R(Fx(18), Fz(40), Fx(2382), Fz(0), INK, 2)
for pxx in (18, 2382):
    R(Fx(pxx), Fz(880), Fx(pxx + 40), Fz(0), INK, 2)
for pxx in (280, 960, 1680, 2040):
    L((Fx(pxx), Fz(760)), (Fx(pxx), Fz(40)), INK, 1)
for i in range(10):
    vx = (i + 0.5) * 240
    d.polygon([(Fx(vx), Fz(0)), (Fx(vx) - 9, Fz(36)), (Fx(vx) + 9, Fz(36))], outline=(150, 150, 150))
for gx in (680, 1680):
    for pxx in (gx + 20, gx + 500):
        R(Fx(pxx), Fz(0), Fx(pxx + 40), Fz(-153), INK, 2)
def dim2(a, b, label, dy=14, dx=0):
    L(a, b, DIM, 1)
    d.text(((a[0] + b[0]) / 2 + dx, (a[1] + b[1]) / 2 + dy), label, fill=DIM, font=fS, anchor="lm")
dim2((Fx(18), Fz(0)), (Fx(2382), Fz(0)), "2400", 18)
dim2((Fx(18), Fz(800)), (Fx(18), Fz(0)), "~880", 0, 12)
dim2((Fx(700), Fz(0)), (Fx(700), Fz(-153)), "153", 0, 20)

# ============ TOP VIEW (X-Y) ============
tx0, ty0, tsx, tsy = 760, 190, 0.36, 0.36
def Tx(mm): return tx0 + mm * tsx
def Ty(mm): return ty0 - mm * tsy
cap(760, 170, "俯视图", fH)
R(Tx(0), Ty(500), Tx(2400), Ty(-500), INK, 2)
for yb in (480, 120, -120, -420, -480):
    L((Tx(18), Ty(yb)), (Tx(2382), Ty(yb)), INK, 2)
for x in (0, 2400):
    L((Tx(x), Ty(480)), (Tx(x), Ty(-480)), INK, 2)
for px2 in (700, 1200, 1700, 2200):
    L((Tx(px2), Ty(460)), (Tx(px2), Ty(-460)), DIM, 1)
dim2((Tx(0), Ty(500)), (Tx(2400), Ty(500)), "2400", 14)
dim2((Tx(0), Ty(500)), (Tx(0), Ty(-500)), "1000", 0, 20)

# ============ SIDE VIEW (Y-Z) ============
sy0, sz0, ssy, ssz = 90, 1040, 0.36, 0.30
def Sy(mm): return sy0 + mm * ssy
def Sz(mm): return sz0 - mm * ssz
cap(90, 960, "侧视图", fH)
R(Sy(-500), Sz(800), Sy(500), Sz(0), INK, 2)
for zz in (760, 40):
    L((Sy(-500), Sz(zz)), (Sy(500), Sz(zz)), INK, 2)

# ============ ISO VIEW (accurate isometric box) ============
ix0, iy0 = 760, 1050
def P(x, y, z):
    return (ix0 + (x - y) * 0.30, iy0 + (x + y) * 0.17 - z * 0.17)
cap(760, 830, "等轴测图", fH)
nc = [(-500, -1000, 0), (-500, 1000, 0), (500, 1000, 0), (500, -1000, 0)]
tc = [(x, y, 800) for (x, y, _) in nc]
for vv in (nc, tc):
    for i in range(4):
        L(P(*vv[i]), P(*vv[(i + 1) % 4]), (70, 70, 110), 2)
for i in range(4):
    L(P(*nc[i]), P(*tc[i]), (70, 70, 110), 2)
# balloons with leader lines
bub = [
    (P(-500, 1000, 800), "1", (P(-500, 1000, 860))),
    (P(500, 1000, 800), "2", (P(560, 1000, 860))),
    (P(-500, -1000, 400), "3", (P(-500, -1100, 430))),
    (P(500, -1000, 800), "4", (P(560, -1000, 860))),
    (P(-300, 300, 20), "5", (P(-360, 300, 30))),
    (P(0, 600, 20), "6", (P(-60, 600, 30))),
    (P(0, 0, 20), "7", (P(-60, 20, 30))),
    (P(0, -600, 20), "8", (P(-60, -600, 30))),
    (P(-500, 1000, -120), "9", (P(-560, 1000, -140))),
    (P(500, 1000, -120), "10", (P(560, 1000, -140))),
    (P(0, 1200, -120), "11", (P(-60, 1200, -140))),
]
for (pt, num, ext) in bub:
    L(ext, pt, (170, 30, 30), 1)
    r = 12
    d.ellipse([ext[0] - r, ext[1] - r, ext[0] + r, ext[1] + r], outline=(170, 30, 30), width=2, fill=(255, 235, 235))
    d.text((ext[0], ext[1]), num, font=fX, anchor="mm", fill=(170, 30, 30))

# ============ BOM table ============
bx, by = 90, 130
cap(bx, by - 34, "BOM 明细表", fH)
colw = [70, 300, 120, 80]
head = ["序号", "零件名称", "材料", "数量"]
R(bx, by, bx + sum(colw), by + 34, INK, 2)
wx = bx
for i, h in enumerate(head):
    d.text((wx + 8, by + 6), h, font=fN, fill=INK)
    wx += colw[i]
parts = [
    ("1", "顶部纵向梁 40×40×2400", "Q235", "11"),
    ("2", "纵/横梁 40×40×2400/2360", "Q235", "6"),
    ("3", "立柱 40×40×720", "Q235", "9"),
    ("4", "角柱(带把手) 40×40×840", "Q235", "4"),
    ("5", "V型定位小梁 40 开口", "Q235", "10"),
    ("6", "连接短梁 320", "Q235", "4"),
    ("7", "连接短梁 200", "Q235", "2"),
    ("8", "连接短梁 260", "Q235", "4"),
    ("9", "门架U型梁 56×25×3", "Q235", "8"),
    ("10", "门架立柱 40×40×150", "Q235", "16"),
    ("11", "端部水平方管 40×153×250", "Q235", "2"),
]
yy = by + 34
for i, row in enumerate(parts):
    rh = 30
    R(bx, yy, bx + sum(colw), yy + rh, INK, 1)
    wx = bx
    for j, val in enumerate(row):
        d.text((wx + 8, yy + 6), val, font=fS, fill=INK)
        wx += colw[j]
    yy += rh

out = "C:/Users/Administrator/Documents/Codex/2026-08-30/zhao/outputs/drawing_A3.png"
img.save(out)
print("saved", out)
