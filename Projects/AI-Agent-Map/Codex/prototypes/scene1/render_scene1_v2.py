from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import os
import subprocess

W, H = 1080, 1920
FPS = 24
DURATION = 12
FRAMES = FPS * DURATION
ROOT = os.path.dirname(__file__)
OUT_DIR = os.path.join(ROOT, "frames_v2")
VIDEO_SILENT = os.path.join(ROOT, "scene1_lost_agent_probe_v2.mp4")
AUDIO = os.path.join(ROOT, "scene1_temp_voice_v2.aiff")
VIDEO_VOICE = os.path.join(ROOT, "scene1_lost_agent_probe_v2_with_voice.mp4")

os.makedirs(OUT_DIR, exist_ok=True)


def clamp(x, lo=0, hi=1):
    return max(lo, min(hi, x))


def ease(x):
    return x * x * (3 - 2 * x)


def ease_out(x):
    return 1 - (1 - x) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


def font(size, bold=False):
    names = [
        "/System/Library/Fonts/Supplemental/Avenir Next Condensed.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for name in names:
        if os.path.exists(name):
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


FONT_HERO = font(100, True)
FONT_NODE = font(30, True)
FONT_SMALL = font(38)

nodes = [
    ("Research", 315, 670, 0.92),
    ("Draft", 760, 780, 1.02),
    ("Check", 330, 1155, 0.85),
    ("Publish", 770, 1290, 1.1),
]

path = [
    (540, 380),
    (315, 670),
    (760, 780),
    (315, 670),
    (770, 1290),
]


def point_on_path(progress):
    total = len(path) - 1
    idx_float = clamp(progress) * total
    idx = min(int(idx_float), total - 1)
    local = ease(idx_float - idx)
    ax, ay = path[idx]
    bx, by = path[idx + 1]
    return lerp(ax, bx, local), lerp(ay, by, local), math.atan2(by - ay, bx - ax)


def text_center(draw, xy, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=fnt, fill=fill)


def line_glow(layer, points, color, width, blur=9):
    draw = ImageDraw.Draw(layer)
    draw.line(points, fill=(*color[:3], int(color[3] * 0.35)), width=width)
    draw.line(points, fill=color, width=max(1, width // 3))


def draw_probe(draw, x, y, angle, alpha):
    size = 58
    body = []
    for base, dist in [(0, size), (2.36, size * 0.72), (-2.36, size * 0.72)]:
        a = angle + base
        body.append((x + math.cos(a) * dist, y + math.sin(a) * dist))
    shadow = [(px + 0, py + 12) for px, py in body]
    draw.polygon(shadow, fill=(0, 0, 0, int(alpha * 0.34)))
    draw.polygon(body, fill=(220, 248, 255, alpha), outline=(72, 232, 255, alpha))
    draw.ellipse((x - 20, y - 20, x + 20, y + 20), fill=(0, 240, 235, alpha), outline=(230, 255, 255, alpha))
    rear_x = x - math.cos(angle) * 48
    rear_y = y - math.sin(angle) * 48
    for side in [-1, 1]:
        ex = rear_x + side * math.sin(angle) * 38
        ey = rear_y - side * math.cos(angle) * 38
        draw.line((rear_x, rear_y, ex, ey), fill=(130, 225, 255, int(alpha * 0.8)), width=4)


def draw_background(base, t):
    bg = Image.new("RGBA", (W, H), (4, 7, 16, 255))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        shade = int(26 * y / H)
        d.line((0, y, W, y), fill=(4, 7 + shade // 2, 16 + shade, 255))
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    drift = math.sin(t * math.pi * 2) * 28
    for i in range(-14, 24):
        x = i * 92 + drift
        gd.line((x, 0, x + 520, H), fill=(55, 138, 188, 24), width=1)
    for j in range(8, 18):
        y = j * 115
        gd.line((80, y, W - 80, y + 40), fill=(55, 138, 188, 18), width=1)
    bg.alpha_composite(grid)
    base.alpha_composite(bg)


def draw_prompt(draw, t):
    a = int(210 * clamp((t - 0.08) / 0.12) * (1 - clamp((t - 0.38) / 0.18)))
    if a <= 0:
        return
    x0, y0, x1, y1 = 155, 210, 925, 535
    draw.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=(14, 32, 52, int(a * 0.64)), outline=(112, 226, 255, a), width=3)
    for i in range(10):
        y = y0 + 48 + i * 24
        length = 340 + 210 * abs(math.sin(i * 1.31))
        draw.line((x0 + 58, y, x0 + 58 + length, y), fill=(177, 229, 255, int(a * 0.82)), width=4)
    text_center(draw, (540, 166), "Smart?", FONT_SMALL, (230, 250, 255, a))


def render(n):
    t = n / (FRAMES - 1)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_background(img, t)
    draw = ImageDraw.Draw(img)

    draw_prompt(draw, t)

    node_reveal = clamp((t - 0.24) / 0.22)
    for label, x, y, depth in nodes:
        sx = x + math.sin(t * 1.7 + depth) * 10 * depth
        sy = y + math.cos(t * 1.3 + depth) * 12 * depth
        alpha = int((80 + 145 * node_reveal) * depth)
        radius = int(38 + 6 * math.sin(n * 0.06 + x))
        color = (92, 202, 255) if label != "Check" else (255, 196, 78)
        draw.ellipse((sx - radius * 2, sy - radius * 2, sx + radius * 2, sy + radius * 2), outline=(*color, int(alpha * 0.16)), width=10)
        draw.ellipse((sx - radius * 1.45, sy - radius * 1.45, sx + radius * 1.45, sy + radius * 1.45), outline=(*color, int(alpha * 0.22)), width=6)
        draw.ellipse((sx - radius, sy - radius, sx + radius, sy + radius), outline=(*color, alpha), width=4)
        text_center(draw, (sx, sy + 76), label, FONT_NODE, (222, 238, 248, alpha))

    move = clamp((t - 0.18) / 0.60)
    px, py, angle = point_on_path(move)
    angle += math.sin(n * 0.22) * 0.24

    trail = []
    for j in range(28):
        past = clamp(move - j * 0.012)
        tx, ty, _ = point_on_path(past)
        trail.append((tx, ty))
    for j in range(len(trail) - 1):
        alpha = int(95 * (1 - j / len(trail)))
        line_glow(img, [trail[j], trail[j + 1]], (0, 235, 255, alpha), 7, 0)

    if t > 0.46:
        wrong_alpha = int(140 * clamp((t - 0.46) / 0.16))
        wobble = math.sin(n * 0.9) * 9
        line_glow(img, [(315, 670 + wobble), (770, 1290 - wobble)], (255, 73, 105, wrong_alpha), 12, 13)
        text_center(draw, (540, 1510), "Lost.", FONT_HERO, (246, 250, 255, int(230 * clamp((t - 0.5) / 0.14))))

    draw.ellipse((px - 82, py - 82, px + 82, py + 82), outline=(0, 230, 255, 32), width=16)
    draw.ellipse((px - 58, py - 58, px + 58, py + 58), outline=(0, 230, 255, 44), width=9)
    draw_probe(draw, px, py, angle, 255)

    if t > 0.78:
        fade = ease_out(clamp((t - 0.78) / 0.22))
        img.alpha_composite(Image.new("RGBA", (W, H), (4, 7, 16, int(185 * fade))))
        draw = ImageDraw.Draw(img)
        text_center(draw, (540, 900), "No map.", FONT_HERO, (238, 250, 255, int(255 * fade)))
        text_center(draw, (540, 1022), "The agent needs a path.", FONT_SMALL, (130, 221, 255, int(235 * fade)))

    return img.convert("RGB")


for i in range(FRAMES):
    render(i).save(os.path.join(OUT_DIR, f"frame_{i:04d}.png"), quality=94)

subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        os.path.join(OUT_DIR, "frame_%04d.png"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        VIDEO_SILENT,
    ],
    check=True,
)

subprocess.run(
    [
        "say",
        "-v",
        "Samantha",
        "-r",
        "158",
        "An AI agent can sound smart. But without a map, it can still get lost. It can loop, skip checks, or rush to the wrong answer.",
        "-o",
        AUDIO,
    ],
    check=True,
)

subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-i",
        VIDEO_SILENT,
        "-i",
        AUDIO,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        VIDEO_VOICE,
    ],
    check=True,
)

print(VIDEO_VOICE)
