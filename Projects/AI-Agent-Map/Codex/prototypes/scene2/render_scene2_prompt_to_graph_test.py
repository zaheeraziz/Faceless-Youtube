from PIL import Image, ImageDraw, ImageFont
import math
import os
import subprocess

W, H = 1080, 1920
FPS = 24
DURATION = 12
FRAMES = FPS * DURATION
ROOT = os.path.dirname(__file__)
OUT_DIR = os.path.join(ROOT, "frames_scene2_prompt_to_graph_test")
VIDEO_SILENT = os.path.join(ROOT, "scene2_prompt_to_graph_test.mp4")
AUDIO = os.path.join(ROOT, "scene2_prompt_to_graph_test_temp_voice.aiff")
VIDEO_VOICE = os.path.join(ROOT, "scene2_prompt_to_graph_test_with_voice.mp4")

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


FONT_HERO = load_font(96, True)
FONT_LABEL = load_font(48, True)
FONT_NODE = load_font(34, True)
FONT_SMALL = load_font(34)

NODES = {
    "Research": (250, 700),
    "Draft": (800, 700),
    "Check": (250, 1160),
    "Publish": (800, 1160),
}

GRAPH_PATH = [NODES["Research"], NODES["Draft"], NODES["Check"], NODES["Publish"]]


def text_center(draw, xy, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=font, fill=fill)


def point_on(points, progress):
    total = len(points) - 1
    idx_float = clamp(progress) * total
    idx = min(int(idx_float), total - 1)
    local = ease(idx_float - idx)
    ax, ay = points[idx]
    bx, by = points[idx + 1]
    return lerp(ax, bx, local), lerp(ay, by, local), math.atan2(by - ay, bx - ax)


def draw_background(draw, t):
    for y in range(H):
        shade = int(26 * y / H)
        draw.line((0, y, W, y), fill=(5, 9 + shade // 2, 18 + shade))
    drift = math.sin(t * math.pi * 2) * 22
    for i in range(-14, 24):
        x = i * 95 + drift
        draw.line((x, 0, x + 520, H), fill=(33, 94, 132), width=1)
    for j in range(7, 18):
        y = j * 120
        draw.line((90, y, W - 90, y + 38), fill=(24, 70, 105), width=1)


def draw_prompt_block(draw, t):
    appear = clamp((t - 0.02) / 0.12)
    collapse = clamp((t - 0.25) / 0.25)
    alpha = int(230 * appear * (1 - clamp((t - 0.48) / 0.12)))
    if alpha <= 0:
        return
    scale = lerp(1, 0.64, ease(collapse))
    cx, cy = 540, 640
    w, h = 760 * scale, 380 * scale
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    draw.rounded_rectangle((x0, y0, x1, y1), radius=28, fill=(15, 32, 52, int(alpha * 0.82)), outline=(108, 226, 255, alpha), width=3)
    labels = ["research", "write", "check", "publish"]
    for idx, label in enumerate(labels):
        y = y0 + 74 * scale + idx * 62 * scale
        draw.line((x0 + 70 * scale, y, x0 + 430 * scale, y), fill=(176, 229, 255, int(alpha * 0.9)), width=max(2, int(5 * scale)))
        draw.text((x0 + 465 * scale, y - 19 * scale), label, font=FONT_SMALL, fill=(200, 232, 248, alpha))


def draw_node(draw, label, xy, alpha):
    x, y = xy
    color = (90, 205, 255) if label != "Check" else (255, 196, 78)
    r = 48
    draw.ellipse((x - r * 1.8, y - r * 1.8, x + r * 1.8, y + r * 1.8), outline=(*color, int(alpha * 0.18)), width=12)
    draw.ellipse((x - r, y - r, x + r, y + r), outline=(*color, alpha), width=5)
    text_center(draw, (x, y + 82), label, FONT_NODE, (230, 242, 250, alpha))


def draw_dotted_line(draw, a, b, fill, width=7, dash=22, gap=17):
    ax, ay = a
    bx, by = b
    length = math.hypot(bx - ax, by - ay)
    if length == 0:
        return
    ux, uy = (bx - ax) / length, (by - ay) / length
    pos = 0
    while pos < length:
        end = min(pos + dash, length)
        draw.line((ax + ux * pos, ay + uy * pos, ax + ux * end, ay + uy * end), fill=fill, width=width)
        pos += dash + gap


def draw_probe(draw, x, y, angle):
    size = 52
    pts = []
    for base, dist in [(0, size), (2.36, size * 0.72), (-2.36, size * 0.72)]:
        a = angle + base
        pts.append((x + math.cos(a) * dist, y + math.sin(a) * dist))
    draw.polygon(pts, fill=(222, 248, 255, 255), outline=(65, 232, 255, 255))
    draw.ellipse((x - 17, y - 17, x + 17, y + 17), fill=(0, 240, 235, 255))


def draw_state_packet(draw, x, y, alpha):
    draw.rounded_rectangle((x - 42, y - 24, x + 42, y + 24), radius=10, fill=(22, 55, 76, alpha), outline=(175, 236, 255, alpha), width=3)
    for offset in [-11, 0, 11]:
        draw.line((x - 24, y + offset, x + 24, y + offset), fill=(190, 235, 255, int(alpha * 0.85)), width=3)


def render_frame(i):
    t = i / (FRAMES - 1)
    img = Image.new("RGB", (W, H), (5, 9, 18))
    draw = ImageDraw.Draw(img, "RGBA")

    draw_background(draw, t)

    top_alpha = int(240 * (1 - clamp((t - 0.22) / 0.18)))
    if top_alpha > 0:
        text_center(draw, (540, 120), "Prompt describes", FONT_HERO, (238, 250, 255, top_alpha))

    draw_prompt_block(draw, t)

    graph_reveal = clamp((t - 0.38) / 0.22)
    if graph_reveal > 0:
        text_center(draw, (540, 410), "Graph executes", FONT_HERO, (238, 250, 255, int(245 * graph_reveal)))

    edge_alpha = int(145 * clamp((t - 0.52) / 0.2))
    if edge_alpha > 0:
        for a, b in zip(GRAPH_PATH, GRAPH_PATH[1:]):
            draw_dotted_line(draw, a, b, (75, 210, 255, edge_alpha), width=7)

    node_alpha = int(235 * graph_reveal)
    for label, xy in NODES.items():
        if node_alpha > 0:
            draw_node(draw, label, xy, node_alpha)

    travel = clamp((t - 0.58) / 0.3)
    if travel > 0:
        px, py, angle = point_on(GRAPH_PATH, travel)
        draw.ellipse((px - 66, py - 66, px + 66, py + 66), outline=(0, 230, 255, 42), width=12)
        draw_probe(draw, px, py, angle)
        draw_state_packet(draw, px + 74, py + 28, int(240 * clamp((t - 0.58) / 0.08)))

    labels_alpha = int(235 * clamp((t - 0.68) / 0.14) * (1 - clamp((t - 0.9) / 0.1)))
    if labels_alpha > 0:
        text_center(draw, (190, 1510), "Node = step", FONT_LABEL, (230, 244, 255, labels_alpha))
        text_center(draw, (540, 1600), "Edge = route", FONT_LABEL, (230, 244, 255, labels_alpha))
        text_center(draw, (875, 1510), "State = context", FONT_LABEL, (230, 244, 255, labels_alpha))

    if t > 0.88:
        fade = ease_out(clamp((t - 0.88) / 0.12))
        draw.rectangle((0, 0, W, H), fill=(5, 9, 18, int(170 * fade)))
        text_center(draw, (540, 900), "Graph executes", FONT_HERO, (238, 250, 255, int(255 * fade)))
        text_center(draw, (540, 1025), "the next step", FONT_LABEL, (130, 221, 255, int(235 * fade)))

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
        "A prompt can describe what you want. But a graph defines what runs next. Nodes do the work, edges control the route, and state carries the context.",
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
