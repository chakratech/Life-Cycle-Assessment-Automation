import sqlite3
import pandas as pd

# =======================
# Define DataFrames
# =======================

# Raw Materials
raw_materials = [
    ("Palm Oil", 1020, "kg/t-PHA", "Crude palm oil, at processing {MY} Economic, U"),
    ("Waste Cooking Oil", 1275.00, "kg/t-PHA", "Used vegetable cooking oil, purified"),
    ("Yeast", 13.7, "kg/t-PHA", "Fodder yeast {RoW}| ethanol from whey | Cutoff, U"),
    ("Glucose", 2.0, "kg/t-PHA", "Glucose {RoW}| glucose production | Cut-off, U"),
    ("Sodium Phosphate", 3.0, "kg/t-PHA", "Sodium phosphate production | Cut-off"),
    ("Citric Acid", 31.5, "kg/t-PHA", "Citric acid {CN}| production | Cut-off, U"),
    ("Ammonia liquid", 14.8, "kg/t-PHA", "Ammonia, liquid {CN}| steam reforming"),
    ("Sodium Hydroxide", 125.4, "kg/t-PHA", "Sodium hydroxide, 50% solution"),
    ("Ammonia Sulphate", 12.4, "kg/t-PHA", "Ammonium sulfate {CN}| nickel refining"),
    ("Potassium Phosphate", 4.8, "kg/t-PHA", "Reference provided"),
    ("Enzyme", 2.4, "kg/t-PHA", "Enzymes {RoW}| enzymes production | Cut-off, U"),
    ("Hydrogen Peroxide", 62.0, "kg/t-PHA", "50% solution"),
    ("SDS", 63, "kg/t-PHA", ""),
    ("Activate Carbon", 1.4, "kg/t-PHA", ""),
    ("Sulfuric Acid", 0.4, "kg/t-PHA", "Sulfuric acid {RoW}| production | Cut-off, U"),
]
raw_materials_df = pd.DataFrame(raw_materials, columns=["name", "amount_per_tpha", "unit", "notes"])

# Utilities
utilities_data = [
    ("Fermentation", 706.2, 1.3, 5.5),
    ("Extraction", 508.1, 2.7, 42.5),
    ("Pelleting", 1162.5, 0.04, 0.0),
]
utilities_df = pd.DataFrame(utilities_data, columns=["process_stage", "electricity_kwh", "steam_ton", "water_ton"])

# Wastewater Effluents
wastewater_data = [
    ("Flow rate", 35.6, "m^3/t-PHA"),
    ("COD", 15000.0, "mg/L"),
    ("TN", 750.0, "mg/L"),
    ("TP", 35.0, "mg/L"),
    ("SS", 6000.0, "mg/L"),
]
wastewater_df = pd.DataFrame(wastewater_data, columns=["metric", "value", "unit"])

# Waste Gas Effluents
gas_emissions_data = [
    ("Ammonia", 0.12300, "kg-gas/t-PHA"),
    ("Sulfuric Acid mist", 0.01400, "kg-gas/t-PHA"),
    ("Particle Matter", 0.029, "kg-gas/t-PHA"),
    ("VOCS", 0.0810, "kg-gas/t-PHA"),
    ("SO2", 0.0000003, "kg-gas/t-PHA"),
    ("NOx", 0.056, "kg-gas/t-PHA"),
    ("H2S", 0.00111, "kg-gas/t-PHA"),
    ("CO2", 455.0, "kg-gas/t-PHA"),
]
waste_gas_df = pd.DataFrame(gas_emissions_data, columns=["gas_name", "value", "unit"])

# Transportation
transport_data = [
    ("land", 1000),
    ("sea", 4000),
]
transport_df = pd.DataFrame(transport_data, columns=["mode", "distance_km"])

# Impact Factors
impact_factors_data = [
    ("Palm Oil", "Climate Change", "kg CO2-eq", 4.350),
    ("Waste Cooking Oil", "Climate Change", "kg CO2-eq", 0.150),
    ("Yeast", "Climate Change", "kg CO2-eq", 1.250),
    ("Glucose", "Climate Change", "kg CO2-eq", 1.760),
    ("Sodium Phosphate", "Climate Change", "kg CO2-eq", 2.130),
    ("Citric Acid", "Climate Change", "kg CO2-eq", 4.700),
    ("Ammonia liquid", "Climate Change", "kg CO2-eq", 0.724),
    ("Sodium Hydroxide", "Climate Change", "kg CO2-eq", 0.683),
    ("Ammonia Sulphate", "Climate Change", "kg CO2-eq", 2.620),
    ("Potassium Phosphate", "Climate Change", "kg CO2-eq", 1.650),
    ("Enzyme", "Climate Change", "kg CO2-eq", 4.400),
    ("Hydrogen Peroxide", "Climate Change", "kg CO2-eq", 0.804),
    ("SDS", "Climate Change", "kg CO2-eq", 1.870),
    ("Activate Carbon", "Climate Change", "kg CO2-eq", 2.300),
    ("Sulfuric Acid", "Climate Change", "kg CO2-eq", 0.348),
    ("Electricity", "Climate Change", "kg CO2-eq", 0.420),
    ("Steam", "Climate Change", "kg CO2-eq", 0.300),
    ("Water", "Climate Change", "kg CO2-eq", 0.300),
    ("Transportation - Land", "Climate Change", "kg CO2-eq", 0.0899),
    ("Transportation - Sea", "Climate Change", "kg CO2-eq", 0.00799),
    ("Incineration", "Climate Change", "kg CO2-eq", 1.28),
    ("Landfill", "Climate Change", "kg CO2-eq", 1.76),
    ("Composting", "Climate Change", "kg CO2-eq", 0.20),
    ("Recycling", "Climate Change", "kg CO2-eq", 1.22),
]
impact_factors_df = pd.DataFrame(impact_factors_data, columns=["name", "impact_category", "unit", "value_per_unit"])

# Summary Impacts
summary_impacts_df = pd.DataFrame([
    ("Climate Change - GWP100", 8379.7, 8.380)
], columns=["impact_category", "value_per_ton", "value_per_kg"])

# =======================
# Create SQLite Database
# =======================

conn = sqlite3.connect("pha_lca.db")  # Creates file in project directory

# Save each table to SQLite
raw_materials_df.to_sql("raw_materials", conn, if_exists="replace", index=False)
utilities_df.to_sql("utilities", conn, if_exists="replace", index=False)
wastewater_df.to_sql("wastewater_effluents", conn, if_exists="replace", index=False)
waste_gas_df.to_sql("waste_gas_effluents", conn, if_exists="replace", index=False)
transport_df.to_sql("transportation", conn, if_exists="replace", index=False)
impact_factors_df.to_sql("impact_factors", conn, if_exists="replace", index=False)
summary_impacts_df.to_sql("summary_impacts", conn, if_exists="replace", index=False)

# Test Query (optional)
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Created tables:")
print(tables)

conn.close()
