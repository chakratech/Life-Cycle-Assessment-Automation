import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Set the style to a dark background to match the provided chart
plt.style.use('dark_background')

# --- 1. Data Setup ---
# Categories for the x-axis (Updated to match new chart)
categories = [
    'Soybean Oil', 'Green Methanol', 'Grey Methanol',
    'Palm Oil', 'Waste Cooking Oil', 'Fossil-based Polymers'
]

# Data for each series (Updated from new data table)
data = {
    'Upstream Processing': np.array([2.3, 2.9200, 2.3, 3.7, 0.2, 0]),
    'PHA Production': np.array([1.9, 1.9, 1.9, 2.4, 2.4, 3.08]),
    'Pelleting': np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
    'EOL': np.array([2.4, 2.44, 2.40, 2.40, 2.40, 2.44]),
    'Carbon Uptake / Methane Capture': np.array([0, -11.7, 0, -3.7, -2.1, 0])
}

# Totals to display on top of each bar (Updated from new chart labels)
totals = [7.03, -3.96, 7.11, 5.34, 3.44, 6.02]
x_indices = range(len(categories))

# Colors chosen to match the chart
colors = {
    'Upstream Processing': '#5A9BD5',  # Blue
    'PHA Production': '#8c564b',  # Brown
    'Pelleting': '#ED7D31',  # Orange-Pink (closer to original)
    'EOL': '#9999FF',  # Lilac
    'Carbon Uptake / Methane Capture': '#70AD47'  # Green
}

# --- 2. Plotting ---
fig, ax = plt.subplots(figsize=(12, 8))

# Initialize bottoms for positive and negative stacks
bottom_positive = np.zeros(len(categories))
bottom_negative = np.zeros(len(categories))

# Loop through the data to plot each series
plot_bars = {}
for label, values in data.items():
    # Separate positive and negative values for stacking
    positive_values = np.where(values > 0, values, 0)
    negative_values = np.where(values < 0, values, 0)

    # Plot positive values
    p1 = ax.bar(categories, positive_values, label=label, bottom=bottom_positive, color=colors[label], width=0.6)
    bottom_positive += positive_values

    # Plot negative values
    p2 = ax.bar(categories, negative_values, bottom=bottom_negative, color=colors[label], width=0.6)
    bottom_negative += negative_values

    # Store one of the bar containers for the legend
    plot_bars[label] = p1

# --- 3. Customization and Styling ---

# --- NEW: Add more pronounced zero line ---
ax.axhline(0, color='white', linewidth=1.2)
# ---

# Add total value labels on top of the bars
for i, total in enumerate(totals):
    # Position the text slightly above the top of the *positive* bar segment
    # This matches the placement in your example chart
    ax.text(i, bottom_positive[i] + 0.2, f'{total:.2f}', ha='center', fontsize=11, fontweight='bold', color='white')

# Set labels and title
ax.set_ylabel('Carbon footprint (kgCO2-eq / kg - polymer)', fontsize=12, labelpad=15)

# --- Updated Y-Axis Limits and Ticks ---
# Set Y-limits to show the full range
ax.set_ylim(-15, 12)
# Set Y-ticks to match the new chart
ax.set_yticks([-15, -10, -5, 0, 5, 10])

# Set minor ticks to appear every 1 unit
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

# Customize ticks and spines
ax.tick_params(axis='x', labelsize=11, length=0, pad=10)  # Remove x-tick lines
ax.tick_params(axis='y', labelsize=10, colors='white')
# Style the minor ticks to be visible but not distracting
ax.tick_params(axis='y', which='minor', length=4, color='gray')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

# Add a horizontal grid
ax.yaxis.grid(True, linestyle='--', which='major', color='gray', alpha=0.5)

# --- ADDED: Faint grid lines for minor ticks ---
ax.yaxis.grid(True, linestyle=':', which='minor', color='gray', alpha=0.4)
# ---

ax.set_axisbelow(True)  # Ensure grid is behind bars

# Add white dots for the net total emissions
# This plots the dot at the *actual total value* from the 'totals' list
ax.scatter(
    x=x_indices,
    y=totals,
    color='white',
    s=40,              # Size of the dot
    zorder=5           # Set zorder to plot on top of bars
)

# --- 4. Legend ---
# Create the legend in the desired order (Updated to match new chart)
legend_labels = [
    'Carbon Uptake / Methane Capture', 'Upstream Processing',
    'PHA Production', 'Pelleting', 'EOL'
]
ax.legend(
    [plot_bars[label] for label in legend_labels],
    legend_labels,
    loc='lower center',
    bbox_to_anchor=(0.5, -0.25),  # Position below the plot
    ncol=len(legend_labels),  # Display in a single row
    frameon=False,  # No frame
    fontsize=11
)

# Adjust layout to prevent labels from being cut off
plt.tight_layout(pad=2)

# Save the figure to a file before showing it
# You can change the filename and format (e.g., 'my_chart.pdf')

plt.savefig('stacked_bar_chart_updated.png', dpi=300, bbox_inches='tight', transparent=True)

# Show the plot
plt.show()