"""
PHA LCA – Base-case (Palm-oil feedstock)
All numbers taken directly from the provided ‘Inventory’ and ‘Impact Assessment’
spreadsheets (kg CO2e per t-PHA).
No parsing – every datum is hard-coded for full transparency.
"""

from pathlib import Path
import matplotlib.pyplot as plt

# ---------- 1. RAW DATA (kg CO2-eq per t-PHA) ---------- #
# Upstream processing
UPSTREAM = {
    "Palm oil feedstock": 4437.0,
    "Yeast": 17.125,
    "Glucose": 3.520,
    "Sodium phosphate": 6.390,
    "Citric acid": 148.1,
    "Ammonia (liq.)": 27.9,
    "Sodium hydroxide": 171.8,
    "Ammonium sulphate": 32.5,
    "Potassium phosphate": 7.9,
    "Enzyme": 10.6,
    "Hydrogen peroxide": 49.9,
    "SDS": 117.8,
    "Activated carbon": 3.22,
    "Sulphuric acid": 0.139,
}

# Utilities
ELECTRICITY = {
    "Electricity – fermentation": 296.6,
    "Electricity – extraction":   213.4,
    "Electricity – pelleting":    488.3,
}
STEAM = {
    "Steam – fermentation": 390.0,
    "Steam – extraction":   810.0,
    "Steam – pelleting":     12.0,
}
WATER = {
    "Water – fermentation": 1.65,
    "Water – pelleting":   12.8,
}

# Direct process emissions
DIRECT_CO2 = 455.0

# Transport & EoL
TRANSPORT = {
    "Marine transport": 43.363,
    "Road transport":  122.017,
}
EOL = 510.0  # mixed incineration/landfill/composting, kg CO2e t-1

# ---------- 2. CALCULATIONS ---------- #
def sum_dict(d): return sum(d.values())

other_chemicals = sum_dict(UPSTREAM) - UPSTREAM["Palm oil feedstock"]
electricity_total = sum_dict(ELECTRICITY)
steam_total       = sum_dict(STEAM)
water_total       = sum_dict(WATER)
transport_total   = sum_dict(TRANSPORT)

BREAKDOWN = {
    "Palm oil feedstock": UPSTREAM["Palm oil feedstock"],
    "Other chemicals":    other_chemicals,
    "Electricity":        electricity_total,
    "Steam":              steam_total,
    "Water":              water_total,
    "Direct process CO₂": DIRECT_CO2,
    "Transport":          transport_total,
    "End-of-life":        EOL,
}

TOTAL_TONNE = sum(BREAKDOWN.values())            # kg CO2e per t-PHA
TOTAL_KILO  = TOTAL_TONNE / 1000.0               # kg CO2e per kg-PHA

# ---------- 3. TEXT OUTPUT ---------- #
print("=== PHA (Palm-oil) LCA – Base case ===")
print(f"Total GWP100 per tonne  : {TOTAL_TONNE:,.1f} kg CO₂-eq t⁻¹")
print(f"Total GWP100 per kilogram: {TOTAL_KILO:,.3f} kg CO₂-eq kg⁻¹\n")
print("Breakdown (kg CO₂-eq t⁻¹):")
for k, v in BREAKDOWN.items():
    print(f"  {k:<20} {v:8.2f}")

# ---------- 4. FIGURE (like Fig. 2a in paper) ---------- #
categories = list(BREAKDOWN.keys())
values     = list(BREAKDOWN.values())

fig, ax = plt.subplots(figsize=(7, 5))

bottom = 0.0
colors = plt.cm.tab20.colors  # simple qualitative palette

for i, (cat, val) in enumerate(zip(categories, values)):
    ax.bar(
        x=0,
        height=val,
        bottom=bottom,
        width=0.6,
        label=cat,
        color=colors[i % len(colors)],
    )
    bottom += val

# Aesthetics
ax.set_ylabel("kg CO₂-eq per t-PHA")
ax.set_xticks([])  # single stacked column
ax.set_title("Cradle-to-grave carbon footprint – base-case PHA\n(breakdown mirroring Zong et al. 2025 Fig. 2a)")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)

# Save & show
out_path = Path("figure_2a_like.png")
fig.tight_layout()
fig.savefig(out_path, dpi=300)
plt.show(block=False)

print(f"\nFigure saved to: {out_path.resolve()}")
