from PIL import Image, ImageDraw
import math

img = Image.new("RGB", (1200, 900), (245, 246, 248))
d = ImageDraw.Draw(img)
cos30 = math.cos(math.radians(30))
sin30 = math.sin(math.radians(30))


def P(x, y, z):
    # isometric, y axis goes up-right, frame length X to the right
    return (324 + (x - y) * 0.23, 341 + (x + y) * 0.13 - z * 0.13)


SH = [(215, 222, 235), (170, 180, 200), (120, 132, 158)]  # top, side, deep


def box(x0, y0, z0, x1, y1, z1):
    c = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),   # bottom
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),   # top
    ]
    pts = [P(*p) for p in c]
    # faces: top (4,5,6,7), front (0,1,5,4), right (1,2,6,5)
    d.polygon([pts[4], pts[5], pts[6], pts[7]], fill=SH[0], outline=(90, 96, 118))
    d.polygon([pts[0], pts[1], pts[5], pts[4]], fill=SH[1], outline=(90, 96, 118))
    d.polygon([pts[1], pts[2], pts[6], pts[5]], fill=SH[2], outline=(90, 96, 118))


# ---- frame members (from final model coordinates) ----
L = 2400
# top beams (11) along Y
for i in range(11):
    x = i * 240
    box(x, -480, 760, x + 40, 480, 800)
# top rail (1) at Y -520..-480
box(20, -520, 760, 2380, -480, 800)
# bottom rails (2) at Y +-500
for yb in (480, -520):
    box(20, yb, 0, 2380, yb + 40, 40)
# inner beams (2) at Y +-120
for yc in (100, -140):
    box(40, yc, 0, 2360, yc + 40, 40)
# end rails (2)
box(0, -520, 0, 40, 520, 40)
box(2360, -520, 0, 2400, 520, 40)
# posts (9) at Y=+480
for i in range(1, 10):
    box(i * 240, 460, 40, i * 240 + 40, 500, 760)
# corner posts (4) with handles
for x in (0, 2360):
    for yb in (460, -520):
        box(x, yb, 40, x + 40, yb + 40, 880)
# V-beams (10)
for i in range(10):
    x = (i + 0.5) * 240
    d.polygon([P(x , -480, 40), P(x, 120, 40), P(x + 22, 120, 40)],
              fill=(210, 130, 20), outline=(160, 90, 0))
# connectors A/C at X 700/1200/1700/2200, B at 1500/2100
for xc in (700, 1200, 1700, 2200):
    box(xc, -460, 0, xc + 40, -140, 40)
    box(xc, 140, 0, xc + 40, 400, 40)
for xc in (1500, 2100):
    box(xc, -100, 0, xc + 40, 100, 40)
# gates: U-beams at 660,1680 (below), posts at 680/1160, 1680/2160
for gx in (660, 1660):
    box(gx, -540, -153, gx + 580, -500, -113)   # U-beam (top face at -113, web base -153)
    box(gx + 20, -520, -153, gx + 60, -480, 0)  # post1
    box(gx + 520, -520, -153, gx + 560, -480, 0)  # post2
# end tubes at X 120..370, Y +-120
box(120, 100, -153, 370, 140, 0)
box(120, -140, -153, 370, -100, 0)

img.save("C:/Users/Administrator/Documents/Codex/2026-08-30/zhao/outputs/assembly_iso.png")
print("saved")
