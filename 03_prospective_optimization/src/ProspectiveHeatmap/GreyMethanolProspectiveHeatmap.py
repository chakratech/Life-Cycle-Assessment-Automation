import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

# --------------------------
# 1) Grid setup (Matched to Screenshot Data)
# --------------------------
# X-axis: Strain yield (0% to 120%)
x_edges = np.linspace(0, 120, 200)
# Y-axis: Conversion rate (15% to 60%)
y_edges = np.linspace(15, 60, 200)

x_centers = (x_edges[:-1] + x_edges[1:]) / 2
y_centers = (y_edges[:-1] + y_edges[1:]) / 2
Xc, Yc = np.meshgrid(x_centers, y_centers)

# --------------------------
# 2) Calculate Z (Formula derived from Grey Methanol data)
# --------------------------
yield_decimal = Xc / 100.0        # 0.0 to 1.2
conversion_decimal = Yc / 100.0   # 0.15 to 0.60

FIXED_COMPONENT = 0.40
VARIABLE_COMPONENT = 0.32

Z = (FIXED_COMPONENT / conversion_decimal) + \
    (VARIABLE_COMPONENT / (conversion_decimal * (1 + yield_decimal)))

# --------------------------
# 3) Colormap (Green to Red)
# --------------------------
colors = ["#1e7f2f", "#f2e750", "#d12626"]
n_bins = 100
cmap = LinearSegmentedColormap.from_list("green_red", colors, N=n_bins)

# --------------------------
# 4) Figure & Axes
# --------------------------
fig, ax = plt.subplots(figsize=(7, 6), dpi=200)

# Transparent background
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

# Plot heatmap
im = ax.pcolormesh(x_edges, y_edges, Z, shading="flat", cmap=cmap, vmin=0.9, vmax=4.8)

# Colorbar styling
cbar = fig.colorbar(im, ax=ax, pad=0.03)
cbar.set_label("Carbon footprint (kg-CO₂eq / kg-PHA)", fontsize=10, color="white", weight='bold')
cbar.ax.yaxis.set_tick_params(color="white", labelcolor="white")
cbar.outline.set_edgecolor("white")

# --------------------------
# 5) Markers & Text (With clip_on=False)
# --------------------------
current_x, current_y = 0, 17.1
theory_x, theory_y = 114.6, 54.6

# Marker 1: Current Technology (clip_on=False prevents it from being cut in half at x=0)
ax.scatter([current_x], [current_y], marker="^", s=140, facecolor="#7fbfff",
           edgecolor="white", linewidth=1.5, zorder=10, clip_on=False)

ax.text(current_x + 3, current_y, "Current\nTechnology", fontsize=10,
        va="center", ha="left", color="white", fontweight='bold', zorder=10)

# Marker 2: Theoretical Upper Limit (clip_on=False ensures it pops if near edge)
ax.scatter([theory_x], [theory_y], marker="^", s=140, facecolor="#7fbfff",
           edgecolor="white", linewidth=1.5, zorder=10, clip_on=False)

ax.text(theory_x - 3, theory_y - 1.3, "Theoretical\nUpper Limit", fontsize=10,
        va="center", ha="right", color="white", fontweight='bold', zorder=10)

# --------------------------
# 6) Labels & Formatting
# --------------------------
ax.set_xlim(0, 115)
ax.set_ylim(15, 55)

ax.set_xlabel("Strain yield (% improved in Methanol input)", color="white", fontsize=10, weight='bold')
ax.set_ylabel("Conversion rate % (kg-PHA output / kg-Methanol input)", color="white", fontsize=10, weight='bold')

ax.tick_params(colors="white", labelsize=9, width=1.2)

# Set borders to white
for spine in ax.spines.values():
    spine.set_color("white")
    spine.set_linewidth(1.2)

# Save
out_dir = Path.cwd()
out_dir.mkdir(parents=True, exist_ok=True)
outfile = out_dir / "methanol_pha_heatmap.png"

fig.savefig(outfile, dpi=600, bbox_inches="tight", transparent=True)
print(f"Saved PNG to: {outfile.resolve()}")

plt.show()