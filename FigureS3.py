import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from pathlib import Path

# --------------------------
# 1) Grid setup
# --------------------------
x_edges = np.arange(0, 61, 3)
y_edges = np.arange(75, 116, 1)

x_centers = (x_edges[:-1] + x_edges[1:]) / 2
y_centers = (y_edges[:-1] + y_edges[1:]) / 2
Xc, Yc = np.meshgrid(x_centers, y_centers)

# --------------------------
# 2) Carbon neutral line
# --------------------------
x0, y0 = 0.0, 103.0
x1, y1 = 35.0, 75.0
dx, dy = (x1 - x0), (y1 - y0)
L = np.hypot(dx, dy)

Z_signed = ((Xc - x0) * dy - (Yc - y0) * dx) / L
scale = 0.035
Z = scale * Z_signed

# --------------------------
# 3) Colormap
# --------------------------
norm = TwoSlopeNorm(vmin=-0.95, vcenter=0.0, vmax=0.78)
cmap = LinearSegmentedColormap.from_list(
    "green_black_orange_centered",
    [(0.0, "#1e7f2f"), (0.5, "#141414"), (1.0, "#ff6600")]
)

# --------------------------
# 4) Figure & Axes
# --------------------------
fig, ax = plt.subplots(figsize=(5, 4), dpi=200)
fig.patch.set_alpha(0.0)   # transparent figure bg
ax.patch.set_alpha(0.0)    # transparent axes bg

# Create heatmap (this defines "im")
im = ax.pcolormesh(x_edges, y_edges, Z, shading="flat", cmap=cmap, norm=norm)

# Colorbar
cbar = fig.colorbar(im, ax=ax, pad=0.03)
cbar.set_label("Carbon footprint (kg-CO₂eq / kg-PHA)", fontsize=9, color="white")
cbar.ax.yaxis.set_tick_params(color="white", labelcolor="white")
cbar.outline.set_edgecolor("white")

# Carbon neutral line
ax.plot([x0, x1], [y0, y1], color="white", lw=2)
ax.text(23, 87, "Carbon neutral limit",
        color="white",
        rotation=np.degrees(206.47),
        va="center", ha="center", fontsize=9)

# Markers + labels
ax.scatter([0], [85], marker="^", s=90, facecolor="#7fbfff",
           edgecolor="white", linewidth=1.2, zorder=3)
ax.text(2, 84, "Baseline for\nPHA industry", fontsize=9, va="top", ha="left", color="white")

ax.scatter([0], [96], marker="^", s=90, facecolor="#7fbfff",
           edgecolor="white", linewidth=1.2, zorder=3)
ax.text(.25, 92.5, "Current\ntechnology", fontsize=9, va="center", ha="left", color="white")

ax.scatter([59.5], [114.5], marker="^", s=90, facecolor="#7fbfff",
           edgecolor="white", linewidth=1.2, zorder=3)
ax.text(58, 111, "Theoretical\nupper limit", fontsize=9,
        va="bottom", ha="right", color="white")

# Axes cosmetics
ax.set_xlim(0, 60)
ax.set_ylim(75, 115)
ax.set_xlabel("Strain yield (% improved in oil input)", color="white")
ax.set_ylabel("Conversion rate % (kg-PHA output / kg-oil input)", color="white")
ax.tick_params(colors="white", labelsize=9)
for spine in ax.spines.values():
    spine.set_color("white")
    spine.set_linewidth(1)

plt.tight_layout()

# --------------------------
# 5) Save
# --------------------------
out_dir = Path.cwd() / "figures"
out_dir.mkdir(parents=True, exist_ok=True)
outfile = out_dir / "pha_heatmap.png"

fig.savefig(outfile, dpi=600, bbox_inches="tight", transparent=True)
print(f"Saved PNG to: {outfile.resolve()}")

plt.show()
