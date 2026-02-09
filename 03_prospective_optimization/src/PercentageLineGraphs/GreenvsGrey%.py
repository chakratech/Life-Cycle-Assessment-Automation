import matplotlib.pyplot as plt

# 1. Data for the plot
# These are the x and y coordinates for your line
x_data = [0, 25, 50, 75, 100]
y_data = [7.11, 4.34, 1.58, -1.19, -3.96]

# These are the specific labels you showed in your example
# (It skips the first point, so we do too)
x_labels = [25, 50, 75, 100]
y_labels = [4.34, 1.58, -1.19, -3.96]

# 2. Set up the figure and axes with a dark background
# We create a figure (fig) and an axes (ax) to plot on
# We also set the background color of the figure and axes to black
fig, ax = plt.subplots(figsize=(10, 6.5))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# 3. Plot the main line
# This hex code (#5b9bd5) is a standard blue, similar to your chart
ax.plot(x_data, y_data, color='#5b9bd5', linewidth=2.5, zorder=2)

# 4. Add the horizontal zero line
ax.axhline(0, color='white', linewidth=1, zorder=1)

# 5. Add data labels (as seen in your example)
for x, y in zip(x_labels, y_labels):
    # Set a default offset (slightly above the line)
    offset = .8
    va = 'top'  # Vertical alignment


    ax.text(x, y + offset, str(y),
            color='white',
            fontsize=11,
            fontweight='bold',
            ha='center',
            va=va)

# 6. Set titles and labels
# Title is a dark grey, matching your image's style
ax.set_title(
    'Impact of Methanol Feedstock Blend on Total PHA Carbon Footprint',
    color='darkgrey',
    fontsize=16,
    fontweight='bold',
    pad=20
)
ax.set_xlabel(
    '% Green Methanol in Feedstock',
    color='white',
    fontsize=12,
    labelpad=10
)
ax.set_ylabel(
    'Carbon footprint (kgCO2-eq / kg - polymer)',
    color='white',
    fontsize=12,
    labelpad=10
)

# 7. Customize spines (the plot border)
ax.spines['left'].set_color('white')
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('none')  # Hide top spine
ax.spines['right'].set_color('none')  # Hide right spine

# 8. Customize ticks
ax.tick_params(axis='x', colors='white', labelsize=11)
ax.tick_params(axis='y', colors='white', labelsize=11)

# Set the x-axis ticks to match your data points
ax.set_xticks(x_data)

# Set the y-axis range to match the example
ax.set_ylim(-4, 8)
# Add this line in section 8 (Customize ticks)
ax.set_xlim(left=0, right=100)

# 9. Add horizontal gridlines (styled like the image)
ax.grid(axis='y', color='white', linestyle='-', linewidth=0.75, alpha=0.3)

# 10. Ensure a tight layout and display the plot
plt.tight_layout()
# Save the figure to a file before showing it
# You can change the filename and format (e.g., 'my_chart.pdf')
plt.savefig('GreenVsGrey%', dpi=300, bbox_inches='tight', transparent=True)

# Show the plot
plt.show()