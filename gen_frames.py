#!/usr/bin/env python3
"""Generate 6 cinematic placeholder frames for the Drava Nova narrative.
Palette: burnt orange + electric blue (Drava Nova canon). 16:9, 1600x900.
These are functional stand-ins; swap with real Higgsfield frames when available."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1600, 900

def font(sz, bold=True):
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def vgrad(img, top, bottom):
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bottom, y / H))

def radial_glow(size, color, alpha=180):
    g = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    for r in range(size // 2, 0, -1):
        a = int(alpha * (1 - r / (size / 2)) ** 2)
        c = color + (a,)
        d.ellipse([size//2 - r, size//2 - r, size//2 + r, size//2 + r], fill=c)
    return g

def skyline(draw, base_y, color, count=26, seed=1):
    x = -20
    rng = seed
    while x < W + 20:
        rng = (rng * 1103515245 + 12345) & 0x7fffffff
        bw = 24 + rng % 70
        rng = (rng * 1103515245 + 12345) & 0x7fffffff
        bh = 60 + rng % 260
        draw.rectangle([x, base_y - bh, x + bw, base_y], fill=color)
        # neon windows
        rng = (rng * 1103515245 + 12345) & 0x7fffffff
        if rng % 3 == 0:
            wc = (90, 200, 255)
        else:
            wc = (255, 150, 60)
        for wy in range(base_y - bh + 12, base_y, 26):
            for wx in range(x + 6, x + bw - 6, 18):
                if (wx + wy) % 47 < 20:
                    draw.rectangle([wx, wy, wx + 5, wy + 8], fill=wc)
        x += bw + 8 + rng % 12

def hero(draw, cx, base_y, scale=1.0, color=(8, 10, 22), robot=True, arm_up=False):
    s = scale
    # boy body
    bw = int(34 * s); bh = int(90 * s)
    draw.rounded_rectangle([cx - bw//2, base_y - bh, cx + bw//2, base_y],
                           radius=int(12*s), fill=color)
    # head
    hr = int(22 * s)
    hy = base_y - bh - hr + int(6*s)
    draw.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=color)
    # goggles hint
    draw.line([cx - hr, hy - int(6*s), cx + hr, hy - int(6*s)],
              fill=(90, 200, 255), width=max(2, int(4*s)))
    # arm up
    if arm_up:
        draw.line([cx + int(10*s), base_y - int(60*s), cx + int(40*s), base_y - bh - int(30*s)],
                  fill=color, width=int(10*s))
    # robot companion
    if robot:
        rr = int(20 * s)
        rx = cx + int(60 * s); ry = base_y - int(50 * s)
        draw.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], fill=color)
        draw.ellipse([rx - int(7*s), ry - int(7*s), rx + int(7*s), ry + int(7*s)],
                     fill=(120, 215, 255))

def grain_and_vignette(img):
    # vignette
    v = Image.new("L", (W, H), 0)
    dv = ImageDraw.Draw(v)
    dv.ellipse([-W//3, -H//3, W + W//3, H + H//3], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(img, dark, v)
    return img

def title_block(img, num, title, desc):
    d = ImageDraw.Draw(img, "RGBA")
    fnum = font(150)
    ftitle = font(52)
    fdesc = font(28, bold=False)
    # big translucent frame number
    d.text((70, H - 250), f"{num:02d}", font=fnum, fill=(255, 255, 255, 26))
    d.text((78, H - 150), title, font=ftitle, fill=(255, 255, 255, 235))
    d.text((80, H - 88), desc, font=fdesc, fill=(150, 200, 255, 210))
    # scanline accent
    d.rectangle([78, H - 96, 78 + 340, H - 92], fill=(255, 120, 40, 230))
    # top label
    fl = font(24)
    d.text((78, 60), "DRAVA NOVA  ·  HDRV STUDIO", font=fl, fill=(255, 150, 60, 200))

def paste_glow(img, cx, cy, size, color, alpha=180):
    g = radial_glow(size, color, alpha)
    img.paste(g, (cx - size//2, cy - size//2), g)

# ---- Frame definitions ----
def frame1():
    img = Image.new("RGB", (W, H))
    vgrad(img, (250, 140, 40), (30, 20, 60))
    paste_glow(img, 1150, 300, 700, (255, 180, 70), 200)  # sun
    d = ImageDraw.Draw(img)
    # distant city in valley
    skyline(d, 640, (40, 30, 70), seed=7)
    # cliff
    d.polygon([(0, H), (0, 560), (520, 620), (620, H)], fill=(14, 12, 26))
    hero(d, 300, 600, scale=1.4, color=(10, 10, 22), robot=False)
    return img, 1, "THE EDGE OF TOMORROW", "A young inventor overlooks the neon city at sunset"

def frame2():
    img = Image.new("RGB", (W, H))
    vgrad(img, (20, 24, 55), (8, 6, 18))
    for gx, gc in [(300, (255,120,40)), (800, (60,170,255)), (1250, (255,90,150))]:
        paste_glow(img, gx, 300, 380, gc, 120)
    d = ImageDraw.Draw(img)
    skyline(d, 560, (18, 16, 40), seed=13)
    # string lights
    for x in range(40, W, 60):
        y = 200 + int(30 * math.sin(x / 90))
        d.ellipse([x-4, y-4, x+4, y+4], fill=(255, 200, 120))
    d.rectangle([0, 620, W, H], fill=(10, 9, 20))
    hero(d, 760, 720, scale=1.5, color=(6, 8, 18), robot=True)
    return img, 2, "NIGHT MARKET", "The boy and his robot roam the neon bazaar"

def frame3():
    img = Image.new("RGB", (W, H))
    vgrad(img, (40, 30, 20), (6, 8, 16))
    paste_glow(img, 800, 250, 600, (90, 190, 255), 120)
    d = ImageDraw.Draw(img)
    # mechanical arms
    for ax in [250, 620, 1050, 1380]:
        d.line([ax, 0, ax + 120, 380], fill=(50, 45, 60), width=26)
        d.ellipse([ax+100, 360, ax+160, 420], fill=(70, 60, 80))
    # sparks
    rng = 99
    for _ in range(160):
        rng = (rng * 1103515245 + 12345) & 0x7fffffff
        sx = rng % W
        rng = (rng * 1103515245 + 12345) & 0x7fffffff
        sy = 200 + rng % 500
        d.line([sx, sy, sx+6, sy+10], fill=(255, 180, 80), width=2)
    d.rectangle([0, 700, W, H], fill=(8, 8, 14))
    hero(d, 800, 800, scale=1.6, color=(4, 6, 14), robot=True)
    return img, 3, "THE HANGAR", "Sparks fly beneath giant mechanical arms"

def frame4():
    img = Image.new("RGB", (W, H))
    vgrad(img, (255, 200, 90), (200, 90, 40))
    paste_glow(img, 1200, 250, 900, (255, 240, 180), 200)
    d = ImageDraw.Draw(img)
    # clouds
    for cx, cy, cs in [(300,600,240),(700,700,300),(1100,620,260),(1400,720,220)]:
        paste_glow(img, cx, cy, cs, (255, 230, 190), 90)
    # dragon silhouette
    d.polygon([(500,500),(760,430),(900,470),(1050,410),(980,520),
               (820,560),(700,540),(560,600)], fill=(30, 18, 20))
    # wing
    d.polygon([(760,440),(680,300),(880,420)], fill=(40, 22, 24))
    # rider
    hero(d, 800, 470, scale=0.8, color=(20, 12, 14), robot=False)
    # energy veins
    d.line([(560,590),(820,555),(1040,415)], fill=(90, 200, 255), width=4)
    return img, 4, "SKYBORNE", "Riding the mechanical dragon at golden hour"

def frame5():
    img = Image.new("RGB", (W, H))
    vgrad(img, (10, 14, 34), (2, 3, 10))
    # portal
    paste_glow(img, 800, 380, 620, (70, 180, 255), 220)
    d = ImageDraw.Draw(img)
    for r in range(300, 220, -6):
        a = int(255 * (1 - (300 - r) / 80))
        d.ellipse([800-r, 380-r, 800+r, 380+r], outline=(90, 200, 255), width=3)
    d.ellipse([800-230, 380-230, 800+230, 380+230], fill=(120, 210, 255))
    # ruins pillars
    for px in [180, 380, 1200, 1420]:
        d.rectangle([px, 300, px+70, H], fill=(12, 14, 26))
        d.rectangle([px-10, 290, px+80, 320], fill=(18, 20, 34))
    d.rectangle([0, 760, W, H], fill=(6, 7, 14))
    hero(d, 800, 860, scale=1.7, color=(3, 5, 12), robot=True)
    return img, 5, "THE ANCIENT GATE", "A glowing portal in the futuristic ruins"

def frame6():
    img = Image.new("RGB", (W, H))
    vgrad(img, (14, 16, 40), (30, 18, 30))
    # huge moon
    paste_glow(img, 800, 360, 1000, (255, 235, 200), 160)
    d = ImageDraw.Draw(img)
    d.ellipse([800-320, 360-320, 800+320, 360+320], fill=(245, 235, 215))
    # city glow below
    skyline(d, H, (10, 9, 20), seed=21)
    paste_glow(img, 800, 880, 1200, (255, 140, 50), 90)
    # ledge
    d.rectangle([0, 780, W, H], fill=(6, 6, 12))
    hero(d, 780, 790, scale=1.8, color=(4, 4, 10), robot=True, arm_up=True)
    return img, 6, "A NEW HORIZON", "Silhouetted against the moon, the journey begins"

frames = [frame1, frame2, frame3, frame4, frame5, frame6]
for i, fn in enumerate(frames, 1):
    img, num, title, desc = fn()
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    img = grain_and_vignette(img)
    title_block(img, num, title, desc)
    out = f"/tmp/hdrv-cinematic-demo/frames/frame-{i:02d}.png"
    img.save(out, "PNG")
    print("saved", out)
print("DONE")
