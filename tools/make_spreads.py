import sys, math
# usage: python3 tools/make_spreads.py tools/pages brochure
#   reads tools/pages/p01.jpg ... p20.jpg and writes brochure/spread-00.webp ... spread-10.webp

from PIL import Image, ImageChops, ImageDraw
S, O = sys.argv[1], sys.argv[2]
W = 3400; SM = 0.04
PX0 = round(W * SM); PW = W - 2 * PX0
HALF = PW // 2
PH = round(PW / (594 / 210))
H = round(PH / 0.66); PY0 = (H - PH) // 2
print("canvas", W, H, "paper", PX0, PY0, 2 * HALF, PH, "PG", round(PY0 / H, 5), "SPAN", round(0.5 - PX0 / W, 5))

def gradient(w, h, fold_right):
    vals = []
    for x in range(w):
        d = (w - 1 - x) if fold_right else x
        s = 1 - (0.20 * math.exp(-d / 48.0) + 0.06 * math.exp(-d / 230.0))
        vals.append(int(round(255 * s)))
    g = Image.new("L", (w, 1)); g.putdata(vals)
    return g.resize((w, h)).convert("RGB")

def page(n, fold_right):
    im = Image.open(f"{S}/p{n:02d}.jpg").convert("RGB").resize((HALF, PH), Image.LANCZOS)
    return ImageChops.multiply(im, gradient(HALF, PH, fold_right))

def stack(dr, x_edge, outward):
    cols = [(236, 233, 226, 255), (212, 208, 199, 255), (242, 240, 234, 255), (203, 198, 188, 240), (238, 236, 230, 210)]
    for k, c in enumerate(cols):
        x = x_edge + outward * (2 * k + 1)
        x0, x1 = sorted((x, x + outward * 2))
        dr.rectangle([x0, PY0 + k, x1 - 1, PY0 + PH - 1 - k], fill=c)

def build(left, right, name):
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(canvas)
    if left is not None:
        stack(dr, PX0, -1)
        canvas.paste(page(left, True), (PX0, PY0))
    if right is not None:
        stack(dr, PX0 + 2 * HALF, 1)
        canvas.paste(page(right, False), (PX0 + HALF, PY0))
    canvas.save(f"{O}/{name}.webp", "WEBP", quality=90, method=6)

build(None, 1, "spread-00")
for i, (l, r) in enumerate([(2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), (16, 17), (18, 19)], start=1):
    build(l, r, f"spread-{i:02d}")
build(20, None, "spread-10")
