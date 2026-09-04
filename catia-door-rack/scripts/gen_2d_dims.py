from PIL import Image, ImageDraw, ImageFont

W, H = 1400, 620
img = Image.new("RGB", (W, H), (250, 250, 250))
d = ImageDraw.Draw(img)


def font(sz, bold=False):
    for p in ("C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf",
              "C:/Windows/Fonts/simsun.ttc", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


f = font(20)
fd = font(18)
fm = font(16)

SC = 0.5           # mm -> px
x0 = 320
z0 = 520


def X(mm): return x0 + mm * SC
def Z(mm): return z0 - mm * SC

# frame side silhouette (front view, X=length, Z up). Frame bottom at Z=0.
# bottom beams Z 0..40 ; top beams Z 760..800 ; posts to 800 ; handles 800..880
frame = [
    (18, 0, 2380, 40),        # bottom long beam (side)
    (18, 760, 2380, 800),     # top beam
]
d.rectangle([X(18), Z(800), X(2380), Z(760)], outline=(40, 90, 150), width=3, fill=(200, 214, 228))
d.rectangle([X(18), Z(40), X(2380), Z(0)], outline=(40, 90, 150), width=3, fill=(200, 214, 228))
# posts at ends
d.rectangle([X(15), Z(800), X(55), Z(0)], outline=(90, 90, 90), width=2, fill=(150, 150, 150))
d.rectangle([X(2345), Z(800), X(2385), Z(0)], outline=(90, 90, 90), width=2, fill=(150, 150, 150))
# a couple inner posts
for pxx in (280, 600, 960, 1320, 1680, 2040):
    d.rectangle([X(pxx), Z(760), X(pxx + 40), Z(40)], outline=(120, 120, 120), width=1, fill=(170, 170, 170))
# V-beams (row) near bottom
dy = 4
for i in range(10):
    vx = (i + 0.5) * 240
    d.polygon([(X(vx), Z(0)), (X(vx) - 12, Z(38)), (X(vx) + 12, Z(38))], outline=(210, 120, 20))
# gates below (Z -153..0) -> draw a few gate rectangles below the bottom beam
for gx in (680, 1680):
    for pxx in (gx + 20, gx + 520):
        d.rectangle([X(pxx), Z(0), X(pxx + 40), Z(-153)],
                    outline=(90, 90, 90), width=2, fill=(170, 170, 170))


def dim(a, b, label, dy=16, dx=0):
    d.line((a[0], a[1], b[0], b[1]), fill=(120, 120, 120), width=2)
    mx, my = (a[0] + b[0]) / 2 + dx, (a[1] + b[1]) / 2 + dy
    d.text((mx, my), label, fill=(90, 90, 90), font=fd, anchor="lm")


dim((X(18), Z(0)), (X(2380), Z(0)), "总长 2400", 20)
dim((X(18), Z(800)), (X(18), Z(0)), "框架高 ~800", 14, 0)
dim((X(700), Z(0)), (X(700), Z(-153)), "门架高 153", 14, 30)
dim((X(18), Z(40)), (X(18), Z(0)), "40", 6, 4)
dim((X(18), Z(800)), (X(18), Z(760)), "40", 6, 4)

# legend / labels
d.text((X(18), Z(-200)), "方管 40×40（空心管）；门架 U 型梁 宽56×高25、厚3，长580", fill=(40, 40, 40), font=f)
d.text((X(18), Z(-250)), "底部纵梁：Y=-480/-120/+120/+420/+480；门架立柱与 AC 短梁对齐(700/1200/1700/2200)",
       fill=(40, 40, 40), font=f)
d.text((X(18), Z(-300)), "U 型梁底面朝下贴地，立柱插于内底面，立柱顶面贴底部横梁下表面",
       fill=(40, 40, 40), font=f)

out = "C:/Users/Administrator/Documents/Codex/2026-08-30/zhao/outputs/dims_2d.png"
img.save(out)
print("saved", out)
