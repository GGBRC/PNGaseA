
# --- HEX COLORS ---
LOW_HEX   = "#0008ff"
MID_HEX   = "#d9d9d9"
HIGH_HEX  = "#FF0000"

# --- FIGURE SIZE ---
FIG_WIDTH   = 1200
FIG_HEIGHT  = 1500

# --- CELL SIZE ---
CELL_WIDTH  = 12
CELL_HEIGHT = 22

# --- FONT ---
FONT_SIZE   = 12
FONT_FAMILY = "Arial"

# --- COLUMN LABEL MODE ---
# OPTIONS:
# "abbrev"  → RTT / MPD / dBact
# "numeric" → 1 / 2 / 3
COLUMN_LABEL_MODE = "abbrev"

# --- Z RANGE ---
Z_MIN = -2
Z_MAX =  2

# --- LEGEND ---
LEGEND_HEIGHT_FRACTION = 0.35
LEGEND_WIDTH = 20

# --- GROUP LAYOUT ---
GROUP_LAYOUT = {
    "BACT":  (2, 35),
    "PLANT": (2, 30),
    "FUNGI": (2, 30),
    "ALGAE": (1, 6)
}

# =========================
# HELPER FUNCTIONS
# =========================

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

LOW_COLOR  = hex_to_rgb(LOW_HEX)
MID_COLOR  = hex_to_rgb(MID_HEX)
HIGH_COLOR = hex_to_rgb(HIGH_HEX)

def interpolate(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def z_to_color(z):
    z = max(Z_MIN, min(Z_MAX, z))
    ratio = (z - Z_MIN) / (Z_MAX - Z_MIN)
    if ratio < 0.5:
        return interpolate(LOW_COLOR, MID_COLOR, ratio * 2)
    else:
        return interpolate(MID_COLOR, HIGH_COLOR, (ratio - 0.5) * 2)

def rgb_str(rgb):
    return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"

# =========================
# LOAD DATA
# =========================

data = []
with open("heatmap_matrix_scaled.tsv") as f:
    header = f.readline()
    for line in f:
        parts = line.strip().split("\t")
        data.append({
            "ID": parts[0],
            "Group": parts[1],
            "RootToTip": float(parts[2]),
            "MeanDist": float(parts[3]),
            "ClosestBact": float(parts[4])
        })

grouped = {}
for row in data:
    grouped.setdefault(row["Group"], []).append(row)

# Define labels
if COLUMN_LABEL_MODE == "numeric":
    column_labels = ["1", "2", "3"]
else:
    column_labels = ["RTT", "MPD", "dBact"]

# =========================
# SVG GENERATION
# =========================

margin_x = 50
margin_y = 120
block_spacing = 80

with open("heatmap_structured_v4.svg", "w") as svg:

    svg.write(f'<svg xmlns="http://www.w3.org/2000/svg" '
              f'width="{FIG_WIDTH}" height="{FIG_HEIGHT}">\n')

    current_x = margin_x

    for group in ["BACT", "PLANT", "FUNGI", "ALGAE"]:

        if group not in grouped:
            continue

        cols, rows = GROUP_LAYOUT[group]
        species = grouped[group]

        # Group title
        svg.write(
            f'<text x="{current_x}" y="{margin_y - 60}" '
            f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE+2}">'
            f'{group}</text>\n'
        )

        for col in range(cols):

            # Column labels (tilted)
            x_base = current_x + col * (CELL_WIDTH*3 + 6)
            for m, label in enumerate(column_labels):
                x_label = x_base + m * CELL_WIDTH + CELL_WIDTH/2
                y_label = margin_y - 20

                svg.write(
                    f'<text x="{x_label}" y="{y_label}" '
                    f'text-anchor="middle" '
                    f'transform="rotate(-45 {x_label},{y_label})" '
                    f'font-family="{FONT_FAMILY}" '
                    f'font-size="{FONT_SIZE}">'
                    f'{label}</text>\n'
                )

            for row_i in range(rows):

                index = col * rows + row_i
                if index >= len(species):
                    continue

                y = margin_y + row_i * CELL_HEIGHT
                vals = [
                    species[index]["RootToTip"],
                    species[index]["MeanDist"],
                    species[index]["ClosestBact"]
                ]

                for m, val in enumerate(vals):
                    color = rgb_str(z_to_color(val))
                    x = x_base + m * CELL_WIDTH
                    svg.write(
                        f'<rect x="{x}" y="{y}" '
                        f'width="{CELL_WIDTH}" height="{CELL_HEIGHT}" '
                        f'fill="{color}" />\n'
                    )

        current_x += cols * (CELL_WIDTH*3 + 6) + block_spacing

    # =========================
    # LEGEND
    # =========================

    legend_height = FIG_HEIGHT * LEGEND_HEIGHT_FRACTION
    legend_y = (FIG_HEIGHT - legend_height) / 2
    legend_x = FIG_WIDTH - 100
    steps = 100

    for i in range(steps):
        t = i / steps
        z_val = Z_MIN + t * (Z_MAX - Z_MIN)
        color = rgb_str(z_to_color(z_val))
        y = legend_y + legend_height - (i/steps)*legend_height
        svg.write(
            f'<rect x="{legend_x}" y="{y}" '
            f'width="{LEGEND_WIDTH}" height="{legend_height/steps}" '
            f'fill="{color}" />\n'
        )

    svg.write(
        f'<rect x="{legend_x}" y="{legend_y}" '
        f'width="{LEGEND_WIDTH}" height="{legend_height}" '
        f'fill="none" stroke="black"/>\n'
    )

    for val in [Z_MIN, 0, Z_MAX]:
        pos = legend_y + legend_height - ((val - Z_MIN)/(Z_MAX-Z_MIN))*legend_height
        svg.write(
            f'<text x="{legend_x+LEGEND_WIDTH+5}" y="{pos}" '
            f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}">'
            f'{val}</text>\n'
        )

    svg.write('</svg>\n')