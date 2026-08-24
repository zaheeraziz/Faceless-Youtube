from PIL import Image, ImageDraw, ImageFont
import math
import os
import subprocess

W, H = 1080, 1920
FPS = 24
DURATION = 12
FRAMES = FPS * DURATION
ROOT = os.path.dirname(__file__)
OUT_DIR = os.path.join(ROOT, "frames_v4_youtube_mobile_test")
VIDEO_SILENT = os.path.join(ROOT, "scene1_youtube_mobile_test_v4.mp4")
AUDIO = os.path.join(ROOT, "scene1_youtube_mobile_test_v4_temp_voice.aiff")
VIDEO_VOICE = os.path.join(ROOT, "scene1_youtube_mobile_test_v4_with_voice.mp4")

os.makedirs(OUT_DIR, exist_ok=True)


def clamp(x, lo=0, hi=1):
    return max(lo, min(hi, x))


def ease(x):
    return x * x * (3 - 2 * x)


def ease_out(x):
    return 1 - (1 - x) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


def load_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Avenir Next Condensed.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


FONT_HERO = load_font(98, True)
FONT_HOOK = load_font(82, True)
FONT_NODE = load_font(34, True)
FONT_SMALL = load_font(44, True)

NODES = {
    "Research": (315, 670),
    "Draft": (760, 780),
    "Check": (330, 1155),
    "Publish": (770, 1290),
}

CORRECT_PATH = [NODES["Research"], NODES["Draft"], NODES["Check"], NODES["Publish"]]
WRONG_PATH = [(540, 390), NODES["Research"], NODES["Draft"], NODES["Publish"]]


def point_on(points, progress):
    total = len(points) - 1
    idx_float = clamp(progress) * total
    idx = min(int(idx_float), total - 1)
    local = ease(idx_float - idx)
    ax, ay = points[idx]
    bx, by = points[idx + 1]
    return lerp(ax, bx, local), lerp(ay, by, local), math.atan2(by - ay, bx - ax)


def text_center(draw, xy, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=font, fill=fill)


def draw_dotted_line(draw, points, fill, width=6, dash=20, gap=17):
    for a, b in zip(points, points[1:]):
        ax, ay = a
        bx, by = b
        length = math.hypot(bx - ax, by - ay)
        if length == 0:
            continue
        ux, uy = (bx - ax) / length, (by - ay) / length
        pos = 0
        while pos < length:
            end = min(pos + dash, length)
            draw.line((ax + ux * pos, ay + uy * pos, ax + ux * end, ay + uy * end), fill=fill, width=width)
            pos += dash + gap


def draw_probe(draw, x, y, angle):
    size = 58
    body = []
    for base, dist in [(0, size), (2.36, size * 0.72), (-2.36, size * 0.72)]:
        a = angle + base
        body.append((x + math.cos(a) * dist, y + math.sin(a) * dist))
    draw.polygon([(px, py + 12) for px, py in body], fill=(0, 0, 0, 85))
    draw.polygon(body, fill=(222, 248, 255, 255), outline=(65, 232, 255, 255))
    draw.ellipse((x - 20, y - 20, x + 20, y + 20), fill=(0, 240, 235, 255), outline=(235, 255, 255, 255))
    rear_x = x - math.cos(angle) * 48
    rear_y = y - math.sin(angle) * 48
    for side in [-1, 1]:
        ex = rear_x + side * math.sin(angle) * 38
        ey = rear_y - side * math.cos(angle) * 38
        draw.line((rear_x, rear_y, ex, ey), fill=(130, 225, 255, 210), width=4)


def draw_background(draw, t):
    for y in range(H):
        shade = int(28 * y / H)
        draw.line((0, y, W, y), fill=(4, 8 + shade // 2, 17 + shade))
    drift = math.sin(t * math.pi * 2) * 30
    for i in range(-14, 24):
        x = i * 92 + drift
        draw.line((x, 0, x + 520, H), fill=(42, 118, 165), width=1)
    for j in range(8, 18):
        y = j * 115
        draw.line((80, y, W - 80, y + 40), fill=(24, 75, 112), width=1)


def draw_prompt(draw, t):
    alpha = int(215 * clamp((t - 0.08) / 0.12) * (1 - clamp((t - 0.36) / 0.15)))
    if alpha <= 0:
        return
    x0, y0, x1, y1 = 155, 210, 925, 535
    draw.rounded_rectangle((x0, y0, x1, y1), radius=30, fill=(14, 32, 52), outline=(112, 226, 255), width=3)
    for i in range(10):
        y = y0 + 48 + i * 24
        length = 340 + 210 * abs(math.sin(i * 1.31))
        draw.line((x0 + 58, y, x0 + 58 + length, y), fill=(177, 229, 255), width=4)
    text_center(draw, (540, 166), "Smart agents", FONT_SMALL, (230, 250, 255))


def render_frame(i):
    t = i / (FRAMES - 1)
    img = Image.new("RGB", (W, H), (4, 8, 17))
    draw = ImageDraw.Draw(img, "RGBA")

    draw_background(draw, t)
    draw_prompt(draw, t)

    hook_alpha = int(245 * (1 - clamp((t - 0.18) / 0.12)))
    if hook_alpha > 0:
        text_center(draw, (540, 92), "Smart agents", FONT_HOOK, (238, 250, 255, hook_alpha))
        text_center(draw, (540, 172), "still fail", FONT_HOOK, (255, 198, 84, hook_alpha))

    reveal = clamp((t - 0.27) / 0.18)
    if reveal > 0:
        draw_dotted_line(draw, CORRECT_PATH, (75, 210, 255, int(95 * reveal)), width=6)
        text_center(draw, (540, 570), "Graph Route", FONT_SMALL, (160, 225, 255, int(170 * reveal)))

    for label, (x, y) in NODES.items():
        alpha = int(100 + 135 * reveal)
        color = (88, 202, 255) if label != "Check" else (255, 196, 78)
        radius = int(38 + 5 * math.sin(i * 0.06 + x))
        draw.ellipse((x - radius * 2, y - radius * 2, x + radius * 2, y + radius * 2), outline=(*color, int(alpha * 0.18)), width=10)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=(*color, alpha), width=4)
        text_center(draw, (x, y + 76), label, FONT_NODE, (222, 238, 248, alpha))

    move = clamp((t - 0.19) / 0.58)
    px, py, angle = point_on(WRONG_PATH, move)
    angle += math.sin(i * 0.22) * 0.18

    trail = []
    for j in range(26):
        past = clamp(move - j * 0.014)
        trail.append(point_on(WRONG_PATH, past)[:2])
    for j in range(len(trail) - 1):
        alpha = int(105 * (1 - j / len(trail)))
        draw.line((trail[j], trail[j + 1]), fill=(0, 235, 255, alpha), width=8)

    if t > 0.53:
        shortcut_alpha = int(150 * clamp((t - 0.53) / 0.14))
        draw.line((NODES["Draft"], NODES["Publish"]), fill=(255, 73, 105, shortcut_alpha), width=12)
        check_x, check_y = NODES["Check"]
        miss_alpha = int(230 * clamp((t - 0.55) / 0.12))
        draw.ellipse((check_x - 88, check_y - 88, check_x + 88, check_y + 88), outline=(255, 73, 105, miss_alpha), width=14)
        text_center(draw, (545, 1435), "Skipped Check", FONT_HERO, (246, 250, 255, miss_alpha))

    draw.ellipse((px - 82, py - 82, px + 82, py + 82), outline=(0, 230, 255, 34), width=16)
    draw.ellipse((px - 58, py - 58, px + 58, py + 58), outline=(0, 230, 255, 50), width=9)
    draw_probe(draw, px, py, angle)

    if t > 0.79:
        fade = ease_out(clamp((t - 0.79) / 0.21))
        draw.rectangle((0, 0, W, H), fill=(4, 8, 17, int(188 * fade)))
        text_center(draw, (540, 900), "No usable map", FONT_HERO, (238, 250, 255, int(255 * fade)))
        text_center(draw, (540, 1022), "No control flow", FONT_SMALL, (130, 221, 255, int(235 * fade)))

    return img


for frame in range(FRAMES):
    render_frame(frame).save(os.path.join(OUT_DIR, f"frame_{frame:04d}.png"), quality=94)

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
        "It looks smart, until it skips verification. Without control flow, the agent can miss the step that matters.",
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
