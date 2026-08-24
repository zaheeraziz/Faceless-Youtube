from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import os
import subprocess

W, H = 1080, 1920
FPS = 30
DURATION = 12
FRAMES = FPS * DURATION
OUT_DIR = os.path.join(os.path.dirname(__file__), "frames")
VIDEO_PATH = os.path.join(os.path.dirname(__file__), "scene1_lost_agent_probe.mp4")

os.makedirs(OUT_DIR, exist_ok=True)


def ease(x):
    return x * x * (3 - 2 * x)


def lerp(a, b, t):
    return a + (b - a) * t


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


FONT_BIG = load_font(94, True)
FONT_MED = load_font(46, True)
FONT_SMALL = load_font(34, False)

nodes = {
    "Research": (300, 660),
    "Draft": (760, 760),
    "Check": (300, 1160),
    "Publish": (760, 1270),
}

path_points = [
    (540, 420),
    (300, 660),
    (760, 760),
    (300, 660),
    (760, 1270),
]


def point_on_path(t):
    total = len(path_points) - 1
    x = min(t * total, total - 0.0001)
    i = int(x)
    local = ease(x - i)
    ax, ay = path_points[i]
    bx, by = path_points[i + 1]
    return lerp(ax, bx, local), lerp(ay, by, local), math.atan2(by - ay, bx - ax)


def draw_glow(draw, xy, radius, color, width=2):
    x, y = xy
    for r in range(radius + 18, radius, -7):
        alpha = int(22 * (r - radius) / 18)
        draw.ellipse((x - r, y - r, x + r, y + r), outline=(*color, alpha), width=width)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, 235))


def draw_centered_text(draw, xy, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=font, fill=fill)


def draw_probe(draw, x, y, angle, alpha=255):
    size = 48
    pts = []
    for base_angle, dist in [(0, size), (2.45, size * 0.72), (-2.45, size * 0.72)]:
        a = angle + base_angle
        pts.append((x + math.cos(a) * dist, y + math.sin(a) * dist))
    draw.polygon(pts, fill=(205, 244, 255, alpha), outline=(70, 220, 255, alpha))
    draw.ellipse((x - 17, y - 17, x + 17, y + 17), fill=(20, 245, 235, alpha))
    ax = x - math.cos(angle) * 42
    ay = y - math.sin(angle) * 42
    draw.line((ax, ay, ax - math.sin(angle) * 26, ay + math.cos(angle) * 26), fill=(130, 220, 255, alpha), width=3)
    draw.line((ax, ay, ax + math.sin(angle) * 26, ay - math.cos(angle) * 26), fill=(130, 220, 255, alpha), width=3)


def draw_prompt_block(draw, t):
    if t < 0.13 or t > 0.48:
        return
    appear = min(1, (t - 0.13) / 0.08)
    fade = 1 if t < 0.36 else max(0, 1 - (t - 0.36) / 0.12)
    alpha = int(180 * appear * fade)
    x0, y0, x1, y1 = 190, 210, 890, 520
    draw.rounded_rectangle((x0, y0, x1, y1), radius=24, outline=(120, 210, 255, alpha), width=3, fill=(18, 34, 54, int(alpha * 0.45)))
    for i in range(9):
        y = y0 + 44 + i * 25
        length = 440 + int(math.sin(i * 1.7) * 90)
        draw.line((x0 + 54, y, x0 + 54 + length, y), fill=(170, 220, 255, alpha), width=4)
    draw_centered_text(draw, (540, 170), "Smart?", FONT_MED, (230, 250, 255, alpha))


def render_frame(n):
    t = n / (FRAMES - 1)
    img = Image.new("RGBA", (W, H), (5, 9, 18, 255))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    # Dim geometric grid.
    for i in range(-10, 20):
        x = i * 105 + int(80 * math.sin(t * 2))
        gd.line((x, 0, x + 420, H), fill=(28, 70, 105, 34), width=1)
    for y in range(160, H, 150):
        gd.line((0, y, W, y + 70), fill=(28, 70, 105, 28), width=1)

    draw = ImageDraw.Draw(img)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(2)))
    draw = ImageDraw.Draw(img)

    draw_prompt_block(draw, t)

    node_alpha = int(80 + 130 * min(1, max(0, (t - 0.28) / 0.18)))
    for label, (x, y) in nodes.items():
        pulse = 1 + 0.08 * math.sin(n * 0.08 + x)
        r = int(42 * pulse)
        color = (80, 190, 255) if label != "Check" else (255, 196, 80)
        draw.ellipse((x - r, y - r, x + r, y + r), outline=(*color, node_alpha), width=4)
        draw_centered_text(draw, (x, y + 78), label, FONT_SMALL, (210, 230, 245, node_alpha))

    move_t = min(1, max(0, (t - 0.2) / 0.62))
    px, py, ang = point_on_path(move_t)

    trail_count = 24
    for j in range(trail_count):
        past = max(0, move_t - j * 0.013)
        tx, ty, _ = point_on_path(past)
        a = int(105 * (1 - j / trail_count) * min(1, t * 2))
        draw.ellipse((tx - 9, ty - 9, tx + 9, ty + 9), fill=(0, 235, 255, a))

    # Unstable wrong path lines.
    if t > 0.44:
        wobble = math.sin(n * 0.8) * 5
        draw.line((300, 660 + wobble, 760, 1270 - wobble), fill=(255, 80, 110, 90), width=5)
        draw_centered_text(draw, (540, 1490), "Lost.", FONT_BIG, (245, 250, 255, int(210 * min(1, (t - 0.44) / 0.12))))

    draw_probe(draw, px, py, ang + math.sin(n * 0.25) * 0.28)

    if t > 0.78:
        overlay = Image.new("RGBA", (W, H), (5, 9, 18, int(170 * (t - 0.78) / 0.22)))
        img.alpha_composite(overlay)
        draw = ImageDraw.Draw(img)
        draw_centered_text(draw, (540, 910), "No map.", FONT_BIG, (235, 250, 255, int(255 * (t - 0.78) / 0.22)))
        draw_centered_text(draw, (540, 1015), "The agent needs a path.", FONT_MED, (140, 215, 255, int(230 * (t - 0.78) / 0.22)))

    return img.convert("RGB")


for frame in range(FRAMES):
    render_frame(frame).save(os.path.join(OUT_DIR, f"frame_{frame:04d}.png"), quality=95)

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
        VIDEO_PATH,
    ],
    check=True,
)

print(VIDEO_PATH)
