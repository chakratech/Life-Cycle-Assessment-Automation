#!/usr/bin/env python3
# pha_lca_basecase.py
#
# Cradle-to-grave GWP100 for the palm-oil → PHA base-case process
# (inventory from your spreadsheets, CI factors from your list;
# non-GHG gas streams are assigned zero GWP100).
# ------------------------------------------------------------------------------

import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# 1. Life-Cycle Inventory – amounts per **tonne PHA**
# ------------------------------------------------------------------------------

inventory = {
    # ─── Raw materials (kg) ───
    "palm_oil":            1_020.0,
    "yeast":                  13.7,
    "glucose":                 2.0,
    "sodium_phosphate":        3.0,
    "citric_acid":            31.5,
    "ammonia_liquid":         14.8,
    "sodium_hydroxide":      125.4,
    "ammonium_sulfate":       12.4,
    "potassium_phosphate":     4.8,
    "enzyme":                  2.4,
    "hydrogen_peroxide":      62.0,
    "sds":                    63.0,
    "activated_carbon":        1.4,
    "sulfuric_acid":           0.4,

    # ─── Utilities ───
    "electricity_fermentation":  706.2,   # kWh
    "electricity_extraction":    508.1,
    "electricity_pelleting":   1_162.5,
    "steam_fermentation":         1.30,   # t steam
    "steam_extraction":           2.70,
    "steam_pelleting":            0.040,
    "water_fermentation":         5.5,    # t ≈ m³
    "water_pelleting":           42.5,

    # ─── Logistics (t-km) ───
    "transport_marine":         35.683,
    "transport_road":          120.310,

    # ─── Process off-gas (kg) ───
    "nh3_emission":              0.123,
    "h2so4_mist":                0.014,
    "particulate_matter":        0.029,
    "vocs":                      0.081,
    "so2":                   3.0e-07,
    "nox":                      0.056,
    "h2s":                      0.00111,
    "co2_direct":              455.0,

    # ─── Waste-water (m³) ───
    "wastewater":               35.6,
}

# ------------------------------------------------------------------------------
# 2. Carbon-intensity factors – kg CO₂-eq per unit
# ------------------------------------------------------------------------------

ci = {
    # Raw materials
    "palm_oil":          4.35,
    "yeast":             1.25,
    "glucose":           1.76,
    "sodium_phosphate":  2.13,
    "citric_acid":       4.70,
    "ammonia_liquid":    0.724,
    "sodium_hydroxide":  0.683,
    "ammonium_sulfate":  2.62,
    "potassium_phosphate": 1.65,
    "enzyme":            4.40,
    "hydrogen_peroxide": 0.804,
    "sds":               1.87,
    "activated_carbon":  2.30,
    "sulfuric_acid":     0.348,

    # Utilities
    "electricity":       0.42,   # kg CO₂e / kWh
    "steam":             0.30,   # kg CO₂e / t steam
    "water":             0.30,   # kg CO₂e / m³

    # Transport
    "transport_road":    0.08993,
    "transport_marine":  0.00790,

    # End-of-life (not used here, included for completeness)
    "incineration":      1.283,
    "landfill":          1.76,
    "composting":        0.20,
    "recycling":         1.22,

    # Direct CO₂
    "co2":               1.00,
}

# --- Non-GHG gas streams & wastewater receive zero GWP100 ---------------------
ci.update({
    "nh3_emission": 0.0,
    "h2so4_mist":   0.0,
    "particulate_matter": 0.0,
    "vocs":         0.0,
    "so2":          0.0,
    "nox":          0.0,
    "h2s":          0.0,
    "wastewater":   0.0,
})
# ------------------------------------------------------------------------------

# 3. Helper to map inventory keys → CI keys
def ci_key(inv_key: str) -> str:
    if inv_key.startswith("electricity"):
        return "electricity"
    if inv_key.startswith("steam"):
        return "steam"
    if inv_key.startswith("water"):
        return "water"
    if inv_key == "co2_direct":
        return "co2"
    return inv_key

# 4. GWP100 calculation
gwp = {k: inventory[k] * ci[ci_key(k)] for k in inventory}
total_gwp_t = sum(gwp.values())
total_gwp_kg = total_gwp_t / 1000.0

print("\n===== GWP100 SUMMARY (Base Case) =====")
print(f"Total: {total_gwp_t:,.1f}  kg CO₂-eq / t-PHA")
print(f"       {total_gwp_kg:,.3f} kg CO₂-eq / kg-PHA\n")

# 5. Simple Figure 2a-style stacked bar (grouped)
groups = {
    "Feedstock & nutrients": [
        "palm_oil", "yeast", "glucose",
        "sodium_phosphate", "citric_acid", "ammonia_liquid",
        "sodium_hydroxide", "ammonium_sulfate", "potassium_phosphate",
        "enzyme", "hydrogen_peroxide", "sds", "activated_carbon",
        "sulfuric_acid",
    ],
    "Utilities": [k for k in inventory if k.startswith(("electricity", "steam", "water"))],
    "Transport": ["transport_marine", "transport_road"],
    "Process emissions": [
        "co2_direct",  # others are zero but included for completeness
    ],
    "Waste-water": ["wastewater"],
}

group_totals = {g: sum(gwp[i] for i in items) for g, items in groups.items()}
sorted_groups = sorted(group_totals.items(), key=lambda x: abs(x[1]), reverse=True)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 5))
bottom = 0.0
for label, value in sorted_groups:
    ax.bar("GWP100", value / 1000, bottom=bottom / 1000, label=label)
    bottom += value

ax.set_ylabel("kg CO₂-eq per kg PHA")
ax.set_title("Cradle-to-Grave GWP100 – Palm-Oil → PHA (Base Case)")
ax.set_xticks([])
ax.axhline(0, color="black", linewidth=0.8)
ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
plt.tight_layout()
plt.show()
