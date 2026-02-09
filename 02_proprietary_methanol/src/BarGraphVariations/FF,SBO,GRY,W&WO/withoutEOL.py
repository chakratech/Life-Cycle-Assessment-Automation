import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Set the style to a dark background
plt.style.use('dark_background')

# --- 1. Data Setup ---
# Categories (Grey Methanol removed)
categories = [
    'Fossil-based Polymers',
    'Soybean Oil',
    'Green Methanol'
]

# Data for each series (Grey Methanol removed)
data = {
    'Upstream Processing': np.array([0, 2.3, 2.9200]),
    'Conversion': np.array([3.08, 1.9, 1.9]),
    'Pelleting': np.array([0.5, 0.5, 0.5]),
    'Carbon Uptake': np.array([0, 0, -11.7])
}

# Totals (From the version WITHOUT EOL, Grey Methanol's total removed)
# Original totals: [3.58, 4.63, 4.71 (Grey), -6.40]
totals = [3.58, 4.63, -6.40]
x_indices = range(len(categories))

# Colors (No EOL, same as last script)
colors = {
    'Upstream Processing': '#5A9BD5',  # Blue
    'Conversion': '#8c564b',  # Brown
    'Pelleting': '#ED7D31',  # Orange-Pink
    'Carbon Uptake': '#70AD47'  # Green
}

# --- 2. Plotting ---
# Adjusted figsize for 3 bars
fig, ax = plt.subplots(figsize=(9, 8))

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

# Add more pronounced zero line
ax.axhline(0, color='white', linewidth=1.2)

# Add total value labels on top of the bars
for i, total in enumerate(totals):
    # Position the text slightly above the top of the *positive* bar segment
    ax.text(i, bottom_positive[i] + 0.2, f'{total:.2f}', ha='center', fontsize=11, fontweight='bold', color='white')

# Set labels and title
ax.set_ylabel('Carbon footprint (kgCO2-eq / kg - polymer)', fontsize=12, labelpad=15)

# Y-Axis Limits and Ticks
ax.set_ylim(-15, 12)
ax.set_yticks([-15, -10, -5, 0, 5, 10])

# Set minor ticks to appear every 1 unit
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

# Customize ticks and spines
ax.tick_params(axis='x', labelsize=11, length=0, pad=10)
ax.tick_params(axis='y', labelsize=10, colors='white')
ax.tick_params(axis='y', which='minor', length=4, color='gray')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

# Add a horizontal grid
ax.yaxis.grid(True, linestyle='--', which='major', color='gray', alpha=0.5)
ax.yaxis.grid(True, linestyle=':', which='minor', color='gray', alpha=0.4)

ax.set_axisbelow(True)  # Ensure grid is behind bars

# Add white dots for the net total emissions
ax.scatter(
    x=x_indices,
    y=totals,
    color='white',
    s=60,              # Kept larger size
    zorder=5
)

# --- 4. Legend ---
# Create the legend in the desired order (No EOL)
legend_labels = [
    'Carbon Uptake', 'Upstream Processing',
    'Conversion', 'Pelleting'
]
ax.legend(
    [plot_bars[label] for label in legend_labels],
    legend_labels,
    loc='lower center',
    bbox_to_anchor=(0.5, -0.25),
    ncol=len(legend_labels),
    frameon=False,
    fontsize=11
)

# Adjust layout
plt.tight_layout(pad=2)

# Save the figure to a new file
plt.savefig('noGreyWithEOL.png', dpi=300, bbox_inches='tight', transparent=True)

# Show the plot
plt.show()