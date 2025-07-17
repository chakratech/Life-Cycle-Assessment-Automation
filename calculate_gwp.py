import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("pha_lca.db")

# Helper function to join a table with its GWP impact factors
def calculate_gwp(table_name, name_col="name", quantity_col="amount_per_tpha"):
    query = f"""
    SELECT a.{name_col} AS name, a.{quantity_col} AS quantity, b.value_per_unit
    FROM {table_name} a
    LEFT JOIN impact_factors b ON a.{name_col} = b.name
    WHERE b.impact_category = 'Climate Change'
    """
    df = pd.read_sql(query, conn)
    df["gwp"] = df["quantity"] * df["value_per_unit"]
    return df[["name", "gwp"]].dropna()

# --- Raw Materials ---
raw_df = calculate_gwp("raw_materials")

# --- Utilities (electricity, steam, water) ---
utility_df = calculate_gwp("utilities", name_col="process_stage", quantity_col="electricity_kwh")
utility_df.loc[:, "name"] = utility_df["name"] + " (Electricity)"

steam_df = calculate_gwp("utilities", name_col="process_stage", quantity_col="steam_ton")
steam_df["name"] = steam_df["name"].str.replace(" (Electricity)", "") + " (Steam)"

water_df = calculate_gwp("utilities", name_col="process_stage", quantity_col="water_ton")
water_df["name"] = water_df["name"].str.replace(" (Electricity)", "") + " (Water)"

utilities_combined = pd.concat([utility_df, steam_df, water_df])

# --- Transportation ---
transport_df = calculate_gwp("transportation", name_col="mode", quantity_col="distance_km")
transport_df["name"] = "Transport - " + transport_df["name"].str.capitalize()

# --- Waste Gas Effluents ---
waste_gas_df = calculate_gwp("waste_gas_effluents", name_col="gas_name", quantity_col="value")

# --- End of Life (EoL) ---
eol_df = pd.read_sql("""
    SELECT name, value_per_unit as gwp
    FROM impact_factors
    WHERE name IN ('Incineration', 'Landfill', 'Recycling', 'Composting')
""", conn)

# Weightings from the paper (Base Case Table S11): 13% incineration, 30% landfill, 19% recycling, 38% uncontrolled
# We'll model uncontrolled as incineration to keep it simple
eol_shares = {
    "Incineration": 0.13 + 0.38,
    "Landfill": 0.30,
    "Recycling": 0.19,
    "Composting": 0.0  # Not used in base case
}
eol_df["gwp"] = eol_df["name"].map(eol_shares) * eol_df["gwp"]
eol_df = eol_df[["name", "gwp"]]

# --- Total GWP ---
all_sources = pd.concat([
    raw_df,
    utilities_combined,
    transport_df,
    waste_gas_df,
    eol_df
])

total_gwp = all_sources["gwp"].sum()
print(f"🌍 Cradle-to-Grave GWP (Base Case): {total_gwp:.2f} kg CO2-eq per t-PHA\n")

# --- Breakdown Table ---
breakdown = all_sources.groupby("name")["gwp"].sum().sort_values(ascending=False)
print(breakdown.to_string())

# --- Visualization ---
plt.figure(figsize=(10, 8))
breakdown.plot(kind="barh")
plt.xlabel("GWP Contribution (kg CO2-eq per t-PHA)")
plt.title("Cradle-to-Grave GWP Breakdown (Base Case)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Done
conn.close()
