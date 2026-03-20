"""
Genera la imagen AMUTUY: INTERFAZ SENSORIAL KULTRUN
1080x1920 portrait, alta resolución
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

W, H = 1080, 1920
GOLD = (200, 164, 92)
GOLD_DIM = (160, 130, 72)
GOLD_GLOW = (200, 164, 92, 60)
BLUE = (0, 122, 255)
BLUE_GLOW = (0, 122, 255, 40)
WHITE = (255, 255, 255)
WHITE_DIM = (200, 210, 222)
BG_TOP = (10, 22, 40)
BG_BOT = (26, 42, 74)

FONTS = "C:/Windows/Fonts/"
font_title = ImageFont.truetype(FONTS + "georgiab.ttf", 42)
font_subtitle = ImageFont.truetype(FONTS + "georgia.ttf", 28)
font_quad_big = ImageFont.truetype(FONTS + "georgiab.ttf", 36)
font_quad_sub = ImageFont.truetype(FONTS + "georgia.ttf", 24)
font_small = ImageFont.truetype(FONTS + "calibri.ttf", 22)
font_tiny = ImageFont.truetype(FONTS + "calibri.ttf", 18)
font_label = ImageFont.truetype(FONTS + "calibrib.ttf", 20)

# --- Background with gradient ---
img = Image.new("RGBA", (W, H), BG_TOP)
draw = ImageDraw.Draw(img)

for y in range(H):
    t = y / H
    r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
    g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
    b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Add subtle stars
random.seed(42)
for _ in range(200):
    sx, sy = random.randint(0, W), random.randint(0, H)
    brightness = random.randint(60, 180)
    size = random.choice([1, 1, 1, 2])
    draw.ellipse([sx, sy, sx + size, sy + size], fill=(brightness, brightness, brightness + 30, brightness))

# --- Kultrun circle ---
CX, CY = W // 2, 620  # center of kultrun
RADIUS = 340

# Wood texture circle
kultrun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
kd = ImageDraw.Draw(kultrun)

# Dark wood base
kd.ellipse([CX - RADIUS, CY - RADIUS, CX + RADIUS, CY + RADIUS], fill=(35, 30, 28, 240))

# Wood grain texture
random.seed(7)
for i in range(600):
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(0, RADIUS - 5)
    wx = CX + math.cos(angle) * dist
    wy = CY + math.sin(angle) * dist
    grain_len = random.randint(8, 40)
    grain_angle = angle + random.uniform(-0.3, 0.3)
    wx2 = wx + math.cos(grain_angle) * grain_len
    wy2 = wy + math.sin(grain_angle) * grain_len
    c = random.randint(25, 55)
    kd.line([(wx, wy), (wx2, wy2)], fill=(c + 10, c + 5, c, 80), width=1)

# Concentric rings for wood effect
for r in range(50, RADIUS, 30):
    ring_c = random.randint(30, 50)
    kd.ellipse([CX - r, CY - r, CX + r, CY + r], outline=(ring_c, ring_c - 3, ring_c - 5, 40), width=1)

img = Image.alpha_composite(img, kultrun)
draw = ImageDraw.Draw(img)

# Golden border
for offset in range(3):
    r = RADIUS + offset
    alpha = 180 - offset * 50
    border_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border_layer)
    bd.ellipse([CX - r, CY - r, CX + r, CY + r], outline=(*GOLD, alpha), width=2)
    img = Image.alpha_composite(img, border_layer)

draw = ImageDraw.Draw(img)

# --- Golden cross dividing quadrants ---
cross_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cross_layer)

# Vertical line
cd.line([(CX, CY - RADIUS + 15), (CX, CY + RADIUS - 15)], fill=(*GOLD, 160), width=3)
# Horizontal line
cd.line([(CX - RADIUS + 15, CY), (CX + RADIUS - 15, CY)], fill=(*GOLD, 160), width=3)

# Glow for cross
cross_glow = cross_layer.filter(ImageFilter.GaussianBlur(4))
img = Image.alpha_composite(img, cross_glow)
img = Image.alpha_composite(img, cross_layer)
draw = ImageDraw.Draw(img)


# --- Helper: draw centered text ---
def draw_text_centered(d, text, x, y, font, fill=WHITE):
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    d.text((x - tw // 2, y), text, font=font, fill=fill)


def draw_text_centered_on_img(text, x, y, font, fill=WHITE):
    """Draw text with subtle shadow for readability"""
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_text_centered(sd, text, x + 2, y + 2, font, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    global img, draw
    img = Image.alpha_composite(img, shadow)

    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)
    draw_text_centered(td, text, x, y, font, fill)
    img = Image.alpha_composite(img, text_layer)
    draw = ImageDraw.Draw(img)


# --- Draw icons ---
def draw_sun_icon(cx, cy, size=30):
    """Sun rising icon"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Horizon line
    d.line([(cx - size, cy + 5), (cx + size, cy + 5)], fill=(*WHITE, 200), width=2)
    # Semi-circle sun
    d.arc([cx - size // 2, cy - size // 2 + 5, cx + size // 2, cy + size // 2 + 5],
          180, 0, fill=(*WHITE, 220), width=2)
    # Rays
    for angle in range(200, 340, 20):
        rad = math.radians(angle)
        x1 = cx + math.cos(rad) * (size // 2 + 5)
        y1 = cy + 5 + math.sin(rad) * (size // 2 + 5)
        x2 = cx + math.cos(rad) * (size // 2 + 14)
        y2 = cy + 5 + math.sin(rad) * (size // 2 + 14)
        d.line([(x1, y1), (x2, y2)], fill=(*WHITE, 180), width=2)
    global img, draw
    img = Image.alpha_composite(img, layer)
    draw = ImageDraw.Draw(img)


def draw_cloud_rain(cx, cy, size=28):
    """Cloud with rain icon"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Cloud body
    d.ellipse([cx - size, cy - size // 2, cx, cy + size // 4], outline=(*WHITE, 200), width=2)
    d.ellipse([cx - size // 2, cy - size, cx + size // 2, cy], outline=(*WHITE, 200), width=2)
    d.ellipse([cx, cy - size // 2, cx + size, cy + size // 4], outline=(*WHITE, 200), width=2)
    # Cloud fill area
    d.rectangle([cx - size + size // 4, cy - size // 4, cx + size - size // 4, cy + size // 4],
                fill=(35, 30, 28, 200))
    d.arc([cx - size, cy - size // 2, cx + size, cy + size // 4], 0, 180, fill=(*WHITE, 200), width=2)
    # Rain drops
    for i in range(-1, 2):
        rx = cx + i * 14
        d.line([(rx, cy + size // 3), (rx - 5, cy + size // 3 + 15)], fill=(*WHITE, 160), width=2)
    global img, draw
    img = Image.alpha_composite(img, layer)
    draw = ImageDraw.Draw(img)


def draw_moon_icon(cx, cy, size=28):
    """Crescent moon icon"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - size, cy - size, cx + size, cy + size], outline=(*WHITE, 220), width=2)
    d.ellipse([cx - size + 12, cy - size - 4, cx + size + 12, cy + size - 4],
              fill=(35, 30, 28, 240), outline=(35, 30, 28, 240))
    global img, draw
    img = Image.alpha_composite(img, layer)
    draw = ImageDraw.Draw(img)


def draw_people_icon(cx, cy, size=20):
    """Community/people icon"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    positions = [-size * 1.5, -size * 0.5, size * 0.5, size * 1.5]
    for px in positions:
        x = int(cx + px)
        # Head
        d.ellipse([x - 6, cy - 16, x + 6, cy - 4], outline=(*WHITE, 200), width=2)
        # Body
        d.arc([x - 9, cy - 2, x + 9, cy + 18], 0, 180, fill=(*WHITE, 180), width=2)
    global img, draw
    img = Image.alpha_composite(img, layer)
    draw = ImageDraw.Draw(img)


# --- Quadrant texts and icons ---

# TOP: PUEL MAPU (Este) - sun
draw_text_centered_on_img("PUEL MAPU", CX, CY - 220, font_quad_big)
draw_text_centered_on_img("(Este)", CX, CY - 180, font_quad_sub, WHITE_DIM)
draw_sun_icon(CX, CY - 140, 30)

# LEFT: PIKUN MAPU (Norte) - cloud/rain
draw_text_centered_on_img("PIKUN MAPU", CX - 170, CY - 40, font_quad_big)
draw_text_centered_on_img("(Norte)", CX - 170, CY, font_quad_sub, WHITE_DIM)
draw_cloud_rain(CX - 170, CY + 55, 24)

# BOTTOM: LAFKEN MAPU / NGULU MAPU (Oeste) - moon
draw_text_centered_on_img("LAFKEN MAPU", CX, CY + 120, font_quad_big)
draw_text_centered_on_img("NGULU MAPU", CX, CY + 160, font_quad_sub, WHITE_DIM)
draw_text_centered_on_img("(Oeste)", CX, CY + 190, font_quad_sub, WHITE_DIM)
draw_moon_icon(CX, CY + 245, 22)

# RIGHT: WILLI MAPU (Sur) - people
draw_text_centered_on_img("WILLI MAPU", CX + 170, CY - 40, font_quad_big)
draw_text_centered_on_img("(Sur)", CX + 170, CY, font_quad_sub, WHITE_DIM)
draw_people_icon(CX + 170, CY + 50, 16)


# --- Activation points on kultrun perimeter ---
activation_angles = [30, 70, 110, 150, 190, 230, 270, 310, 350, 10]
for angle_deg in activation_angles:
    rad = math.radians(angle_deg)
    px = CX + math.cos(rad) * RADIUS
    py = CY + math.sin(rad) * RADIUS

    # Outer glow rings
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    for ring in range(3, 0, -1):
        rs = 6 + ring * 5
        alpha = 30 - ring * 8
        gd.ellipse([px - rs, py - rs, px + rs, py + rs],
                    outline=(*GOLD, max(alpha, 10)), width=1)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img, glow_layer)

    # Center dot
    dot_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot_layer)
    dd.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(*GOLD, 220))
    img = Image.alpha_composite(img, dot_layer)

draw = ImageDraw.Draw(img)

# --- Outer hexagonal glow around kultrun ---
hex_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hex_layer)
hex_radius = RADIUS + 50
hex_points = []
for i in range(6):
    angle = math.radians(60 * i - 30)
    hx = CX + math.cos(angle) * hex_radius
    hy = CY + math.sin(angle) * hex_radius
    hex_points.append((hx, hy))
hex_points.append(hex_points[0])
hd.line(hex_points, fill=(*BLUE, 50), width=2)
hex_glow = hex_layer.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img, hex_glow)
img = Image.alpha_composite(img, hex_layer)
draw = ImageDraw.Draw(img)


# --- Circuit lines from kultrun to Arduino box ---
ARDUINO_X, ARDUINO_Y = 160, 1400
ARDUINO_W, ARDUINO_H = 220, 140

def draw_circuit_line(points, color=BLUE, glow_color=BLUE_GLOW, width=2):
    """Draw a circuit line with glow effect"""
    global img, draw
    # Glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.line(points, fill=glow_color, width=width + 6)
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, glow)
    # Line
    line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(line_layer)
    ld.line(points, fill=(*color, 180), width=width)
    img = Image.alpha_composite(img, line_layer)
    draw = ImageDraw.Draw(img)


# Main trunk from bottom of kultrun down to Arduino area
trunk_start = (CX, CY + RADIUS + 10)
bend1 = (CX, CY + RADIUS + 120)
bend2 = (CX - 100, CY + RADIUS + 200)
bend3 = (ARDUINO_X + ARDUINO_W // 2 + 80, 1200)
bend4 = (ARDUINO_X + ARDUINO_W // 2 + 80, ARDUINO_Y - 30)
arduino_top = (ARDUINO_X + ARDUINO_W // 2, ARDUINO_Y - 30)

draw_circuit_line([trunk_start, bend1])
draw_circuit_line([bend1, bend2])
draw_circuit_line([bend2, bend3])
draw_circuit_line([bend3, bend4])
draw_circuit_line([bend4, arduino_top])

# Branch lines from activation points to trunk
branch_points = [
    (CX - RADIUS * 0.7, CY + RADIUS * 0.7),
    (CX - RADIUS * 0.9, CY + RADIUS * 0.4),
    (CX - RADIUS * 0.5, CY + RADIUS * 0.9),
]
for bp in branch_points:
    mid = (bp[0] - 40, bp[1] + 60)
    draw_circuit_line([bp, mid, (mid[0], bend2[1]), bend2], width=1)

# Right side branches
right_branches = [
    (CX + RADIUS * 0.7, CY + RADIUS * 0.7),
    (CX + RADIUS * 0.9, CY + RADIUS * 0.3),
]
for bp in right_branches:
    mid_y = bp[1] + 80
    draw_circuit_line([bp, (bp[0], mid_y), (CX, mid_y), bend1], width=1)


# --- Arduino controller box ---
arduino_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(arduino_layer)

# Box with rounded feel
box = [ARDUINO_X, ARDUINO_Y, ARDUINO_X + ARDUINO_W, ARDUINO_Y + ARDUINO_H]
ad.rounded_rectangle(box, radius=8, fill=(15, 25, 45, 200), outline=(*BLUE, 140), width=2)

# PCB details inside the box
# Chip
chip_x, chip_y = ARDUINO_X + 30, ARDUINO_Y + 30
ad.rectangle([chip_x, chip_y, chip_x + 50, chip_y + 35], outline=(*GOLD_DIM, 150), width=1)
ad.rectangle([chip_x + 5, chip_y + 5, chip_x + 45, chip_y + 30], fill=(20, 35, 55, 200))
# Pins
for i in range(6):
    pin_y = chip_y + 5 + i * 5
    ad.line([(chip_x - 8, pin_y), (chip_x, pin_y)], fill=(*GOLD_DIM, 120), width=1)
    ad.line([(chip_x + 50, pin_y), (chip_x + 58, pin_y)], fill=(*GOLD_DIM, 120), width=1)

# USB connector
ad.rectangle([ARDUINO_X + 10, ARDUINO_Y + 8, ARDUINO_X + 35, ARDUINO_Y + 22],
             outline=(*WHITE_DIM, 100), width=1)

# Capacitors
for cx_pos in [ARDUINO_X + 100, ARDUINO_X + 130, ARDUINO_X + 160]:
    ad.ellipse([cx_pos, ARDUINO_Y + 80, cx_pos + 15, ARDUINO_Y + 95],
               outline=(*GOLD_DIM, 100), width=1)

# LED indicators
ad.ellipse([ARDUINO_X + 180, ARDUINO_Y + 20, ARDUINO_X + 188, ARDUINO_Y + 28],
           fill=(0, 200, 0, 150))
ad.ellipse([ARDUINO_X + 190, ARDUINO_Y + 20, ARDUINO_X + 198, ARDUINO_Y + 28],
           fill=(200, 0, 0, 100))

# Connector pins at bottom
for i in range(12):
    px = ARDUINO_X + 90 + i * 10
    ad.rectangle([px, ARDUINO_Y + ARDUINO_H - 15, px + 5, ARDUINO_Y + ARDUINO_H - 5],
                 fill=(*GOLD_DIM, 130))

# Glow around box
arduino_glow = arduino_layer.filter(ImageFilter.GaussianBlur(3))
img = Image.alpha_composite(img, arduino_glow)
img = Image.alpha_composite(img, arduino_layer)
draw = ImageDraw.Draw(img)


# --- Labels next to Arduino ---
label_x = ARDUINO_X + ARDUINO_W + 30
label_y = ARDUINO_Y + 10
labels = [
    ("Arduino Uno", GOLD),
    ("ESP-32", GOLD),
    ("Raspberry Pi 4", GOLD),
    ("Interaccion Tactil", WHITE_DIM),  # avoid accent issues in rendering
    ("Punto de Activacion Evento", WHITE_DIM),
]

# Draw small colored line indicators next to each label
for i, (text, color) in enumerate(labels):
    y = label_y + i * 28
    # Indicator line
    line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(line_layer)

    if i < 3:
        # Solid lines for hardware
        ld.line([(label_x - 20, y + 10), (label_x - 5, y + 10)], fill=(*BLUE, 180), width=3)
    elif i == 3:
        # Dashed for interaction
        for dx in range(0, 15, 5):
            ld.line([(label_x - 20 + dx, y + 10), (label_x - 16 + dx, y + 10)],
                    fill=(*BLUE, 150), width=2)
    else:
        # Dotted for activation
        for dx in range(0, 15, 4):
            ld.ellipse([label_x - 20 + dx, y + 8, label_x - 17 + dx, y + 12],
                       fill=(*GOLD, 150))

    img = Image.alpha_composite(img, line_layer)
    draw = ImageDraw.Draw(img)

    # Fix accented characters
    display_text = text
    if text == "Interaccion Tactil":
        display_text = "Interacci\u00f3n T\u00e1ctil"
    elif text == "Punto de Activacion Evento":
        display_text = "Punto de Activaci\u00f3n Evento"

    draw.text((label_x, y), display_text, font=font_small, fill=color)


# --- Title at top ---
draw_text_centered_on_img("AMUTUY: INTERFAZ SENSORIAL KULTRUN", W // 2, 60, font_title)

# Subtle decorative line under title
title_line = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tld = ImageDraw.Draw(title_line)
line_w = 300
tld.line([(W // 2 - line_w, 115), (W // 2 + line_w, 115)], fill=(*GOLD, 80), width=1)
img = Image.alpha_composite(img, title_line)
draw = ImageDraw.Draw(img)

# --- Bottom left label ---
draw.text((40, H - 80), "Controlador H\u00edbrido Amutuy", font=font_subtitle, fill=WHITE_DIM)

# --- Small Calfuniarki star/logo bottom right ---
star_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(star_layer)
star_cx, star_cy = W - 60, H - 60
star_size = 12
for i in range(8):
    angle = math.radians(i * 45)
    x1 = star_cx + math.cos(angle) * star_size
    y1 = star_cy + math.sin(angle) * star_size
    sd.line([(star_cx, star_cy), (x1, y1)], fill=(*GOLD, 150), width=1)
sd.ellipse([star_cx - 3, star_cy - 3, star_cx + 3, star_cy + 3], fill=(*GOLD, 200))
img = Image.alpha_composite(img, star_layer)
draw = ImageDraw.Draw(img)


# --- Final: convert to RGB and save ---
final = img.convert("RGB")
final.save("C:/src/calfuniarki-site/img/Base_corregida.jpg", "JPEG", quality=95)
print(f"Imagen guardada: {W}x{H} px")
