"""
Create a stacked column chart comparing Green vs Grey Methanol→PHA
using the same inventory + impact-factor workflow as your waterfall code.

Outputs:
- green_grey_stacked_transparent.png (transparent background)
- green_grey_contributions.csv (table used for plotting)

Edit the INVENTORY_PATH / *_IMPACT_FACTORS_PATH values if needed.
"""""

from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from difflib import get_close_matches
import re
from pathlib import Path
from matplotlib.patches import Patch

# ----------------------
# 1) File paths (EDIT ME if paths change)
# ----------------------
INVENTORY_PATH = \
    "/Users/cooperzvegintzov/Library/Mobile Documents/com~apple~CloudDocs/Documents/ChakraTech/LCA/MethanolToPHA/Inventory.csv"
GREY_IMPACT_FACTORS_PATH = \
    "/Users/cooperzvegintzov/Library/Mobile Documents/com~apple~CloudDocs/Documents/ChakraTech/LCA/MethanolToPHA/GreyImpactfactors.csv"
GREEN_IMPACT_FACTORS_PATH = \
    "/Users/cooperzvegintzov/Library/Mobile Documents/com~apple~CloudDocs/Documents/ChakraTech/LCA/MethanolToPHA/GreenImpactfactors.csv"

# Output directory (defaults to sibling folder)
OUTDIR = Path("../StackedBarGraph")

# ----------------------
# 2) Helpers copied from your existing workflow
# ----------------------

def norm(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s)
    s = (
        s.replace("\u202f", " ")
        .replace("\u00a0", " ")
        .replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
    )
    return re.sub(r"\s+", " ", s).strip().lower()


def find_col(df: pd.DataFrame, tokens) -> str:
    for c in df.columns:
        cl = c.lower()
        if all(t.lower() in cl for t in tokens):
            return c
    raise KeyError(f"Column with tokens {tokens} not found. Columns: {list(df.columns)}")


SECTION_HEADERS = ["Electricity consumption", "Steam", "Water", "Transportation"]
SECTION_HEADERS_N = [norm(x) for x in SECTION_HEADERS]

# Categories in inventory that are per-ton PHA and need /1000
PER_TON_CATS = ["Methanol", "Electricity", "Chemicals", "Water"]


def category_totals_from(impact_factors_csv: str) -> pd.Series:
    inv_raw = pd.read_csv(INVENTORY_PATH)
    imp_raw = pd.read_csv(impact_factors_csv)

    cat_col = find_col(imp_raw, ["impact", "category"])
    kg_col = find_col(imp_raw, ["co2", "kg"])

    # Exclude EOL/disposal rows if present in factors table
    EXCLUDE = {"incineration", "landfill", "composting", "recycling"}
    imp = imp_raw[~imp_raw[cat_col].astype(str).str.strip().str.lower().isin(EXCLUDE)].copy()

    imp["_key"] = imp[cat_col].map(norm)
    imp[kg_col] = pd.to_numeric(imp[kg_col], errors="coerce")

    factor_lookup = dict(zip(imp["_key"], imp[kg_col]))
    factor_keys = list(factor_lookup.keys())

    rows, current_section = [], None
    for _, r in inv_raw.iterrows():
        name = str(r.get("Raw Material", "")).strip()
        val = pd.to_numeric(r.get("Value", np.nan), errors="coerce")
        unit = r.get("Unit", "")

        # Section headers in inventory (no value)
        if norm(name) in SECTION_HEADERS_N and pd.isna(val):
            current_section = name
            continue
        if not name or pd.isna(val):
            continue

        rows.append({"Item": name, "Section": current_section, "Value": val, "Unit": unit})

    inv = pd.DataFrame(rows).reset_index(drop=True)

    def assign_category(row):
        if pd.notna(row["Section"]):
            return row["Section"]
        if norm(row["Item"]) == norm("CH3OH"):
            return "Methanol"
        if norm(row["Item"]) == norm("Water"):
            return "Water"
        if norm(row["Item"]) == norm("Electricity"):
            return "Electricity"
        return "Chemicals"

    inv["Category"] = inv.apply(assign_category, axis=1)

    def factor_key_for_row(row):
        key = norm(row["Item"])
        if key in factor_lookup:
            return key
        m = get_close_matches(key, factor_keys, n=1, cutoff=0.85)
        return m[0] if m else None

    inv["_factor_key"] = inv.apply(factor_key_for_row, axis=1)
    inv["Factor (kg CO2-eq / unit)"] = inv["_factor_key"].map(factor_lookup)

    def compute_impact(row):
        val = row["Value"] * row["Factor (kg CO2-eq / unit)"]
        return (val / 1000.0) if row["Category"] in PER_TON_CATS else val

    inv["Impact (kg CO2-eq)"] = inv.apply(compute_impact, axis=1)

    by_cat = (
        inv.dropna(subset=["Impact (kg CO2-eq)"])
           .groupby("Category", as_index=False)["Impact (kg CO2-eq)"].sum()
    )

    ordered = ["Methanol", "Electricity", "Chemicals", "Water"]
    s = by_cat.set_index("Category")["Impact (kg CO2-eq)"].reindex(ordered).fillna(0.0)
    return s


# ----------------------
# 3) Compute the two scenarios
# ----------------------

grey = category_totals_from(GREY_IMPACT_FACTORS_PATH)
green = category_totals_from(GREEN_IMPACT_FACTORS_PATH)

def rename_feedstock(s: pd.Series) -> pd.Series:
    s = s.copy()
    s.index = ["Feedstock" if i == "Methanol" else i for i in s.index]
    return s

cats = ["Chemicals", "Water", "Electricity", "Feedstock"]
g = rename_feedstock(green).reindex(cats).fillna(0.0)
r = rename_feedstock(grey).reindex(cats).fillna(0.0)

# Build the tidy table used for plotting and save it
OUTDIR.mkdir(parents=True, exist_ok=True)
long = pd.concat(
    [
        pd.DataFrame({"Scenario": "Green", "Category": cats, "Impact_kgCO2eq": g.values}),
        pd.DataFrame({"Scenario": "Grey",  "Category": cats, "Impact_kgCO2eq": r.values}),
    ],
    ignore_index=True
)
(long).to_csv(OUTDIR / "green_grey_contributions.csv", index=False)

# ----------------------
# 4) Plot (manual stacking; handles mixed signs cleanly)
# ----------------------

plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_alpha(0.0)
ax.set_facecolor("none")

# Colors (match your legend exactly)
CHEM = "#FFD166"
WATER = "#118AB2"
ELEC  = "#EF476F"
FEED_GREEN = "#06D6A0"   # legend’s Methanol (Green)
FEED_GREY  = "#888888"

category_colors = {"Chemicals": CHEM, "Water": WATER, "Electricity": ELEC}
feed_colors = {"Green": FEED_GREEN, "Grey": FEED_GREY}

scenarios = ["Green", "Grey"]
x = np.arange(len(scenarios))
width = 0.9

# Precompute totals for labels
totals = long.groupby("Scenario")["Impact_kgCO2eq"].sum().reindex(scenarios)

# Stack each scenario with separate bottoms for positive and negative slices
for i, sc in enumerate(scenarios):
    sub = long[long["Scenario"] == sc].set_index("Category")["Impact_kgCO2eq"]

    pos_bottom = 0.0  # for ≥0 slices (above 0)
    neg_bottom = 0.0  # for <0 slices (below 0)

    # Base categories first
    for cat in ["Chemicals", "Water", "Electricity"]:
        val = float(sub.get(cat, 0.0))
        if val == 0.0:
            continue
        if val > 0:
            ax.bar(i, val, width, bottom=pos_bottom, edgecolor="white", color=category_colors[cat])
            pos_bottom += val
        else:
            ax.bar(i, val, width, bottom=neg_bottom, edgecolor="white", color=category_colors[cat])
            neg_bottom += val

    # Feedstock with scenario-specific color (can be ±)
    feed_val = float(sub.get("Feedstock", 0.0))
    if feed_val != 0.0:
        if feed_val > 0:
            ax.bar(i, feed_val, width, bottom=pos_bottom, edgecolor="white", color=feed_colors[sc])
            pos_bottom += feed_val
        else:
            ax.bar(i, feed_val, width, bottom=neg_bottom, edgecolor="white", color=feed_colors[sc])
            neg_bottom += feed_val

# Axes & labels
ax.set_ylabel("Carbon footprint (kgCO₂-eq / kg-polymer)", color="white")
ax.set_xlabel("Type of Methanol", color="white")
ax.set_title("Bio-based Polymers", color="white", fontsize=14, weight="bold")
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.tick_params(axis="x", colors="white", labelrotation=0)  # horizontal labels
ax.tick_params(axis="y", colors="white")

# Totals above (or below) bars with small point offset
for i, sc in enumerate(scenarios):
    t = float(totals.loc[sc])
    ax.annotate(
        f"{t:.2f}",
        xy=(i, t),
        xytext=(0, 8 if t >= 0 else -8), textcoords="offset points",
        ha="center", va=("bottom" if t >= 0 else "top"),
        fontsize=12, color="white", weight="bold",
        clip_on=False
    )

ax.axhline(0, linewidth=1, color="white", alpha=0.6)
ax.grid(axis="y", linestyle="--", alpha=0.25, color="white")
ax.margins(y=0.15)
plt.tight_layout()

# Legend (restored; exactly as you specified)
legend_elements = [
    Patch(facecolor=CHEM, edgecolor="white", label="Chemicals"),
    Patch(facecolor=WATER, edgecolor="white", label="Water"),
    Patch(facecolor=ELEC,  edgecolor="white", label="Electricity"),
    Patch(facecolor=FEED_GREEN, edgecolor="white", label="Methanol (Green)"),
    Patch(facecolor=FEED_GREY,  edgecolor="white", label="Methanol (Grey)"),
]
leg = ax.legend(handles=legend_elements, ncols=2,facecolor="black", edgecolor="white", labelcolor="white")
for txt in leg.get_texts():
    txt.set_color("white")

# Save transparent PNG with requested name
out_png = OUTDIR / "green_grey_stacked_transparent.png"
plt.savefig(out_png, dpi=300, bbox_inches="tight", transparent=True)
print(f"Saved: {out_png}")

# Optional debugging: print scenario series
# print("GREEN:\n", g)
# print("GREY:\n", r)

plt.show()
