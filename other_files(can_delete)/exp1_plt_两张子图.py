import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 30
matplotlib.rcParams['mathtext.fontset'] = 'stix'

font1 = {'family': 'Times New Roman', 'color': 'Black', 'weight': 'bold', 'size': 40}  # normal
font2 = {'family': 'Times New Roman', 'size': 40, 'weight': 'bold'}  # label
font3 = {'family': 'Times New Roman', 'size': 40, 'weight': 'bold'}  # legend
font4 = {'family': 'Times New Roman', 'color': 'Black', 'weight': 'bold', 'size': 38}

# Data 1
homogeneity_1 = [0.25, 0.5, 0.75, 1]
success_0_1_1 = [42, 77, 97, 98]
success_0_3_1 = [4, 25, 48, 55]
success_0_5_1 = [0, 2, 4, 14]

# Data 2
homogeneity_2 = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
success_0_1_2 = [42, 80, 97, 99, 100, 100, 100, 100]
success_0_3_2 = [4, 42, 56, 78, 86, 82, 93, 94]
success_0_5_2 = [1, 7, 10, 28, 47, 35, 42, 51]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), sharey=True)

# Plot 1
line1, = ax1.plot(homogeneity_1, success_0_1_1, marker='o', label='FP = 0.1', linewidth=4, markersize=15)
line2, = ax1.plot(homogeneity_1, success_0_3_1, marker='s', label='FP = 0.3', linewidth=4, markersize=15)
line3, = ax1.plot(homogeneity_1, success_0_5_1, marker='*', label='FP = 0.5', linewidth=4, markersize=25)

ax1.set_xlabel('Homogeneity', fontdict=font2)
ax1.set_ylabel('Success Rate (%)', fontdict=font2)
ax1.set_xticks(homogeneity_1)
ax1.set_xticklabels(homogeneity_1, fontsize=40, fontfamily='Times New Roman', fontweight='bold')
ax1.tick_params(axis='x', labelsize=40)
ax1.tick_params(axis='y', labelsize=40)
# Adjust y-axis limits to leave some space below 0 and above 100
ax1.set_ylim(-10, 110)
ax1.set_yticks([0, 20, 40, 60, 80, 100])
ax1.set_yticklabels([0, 20, 40, 60, 80, 100], fontsize=40, fontfamily='Times New Roman', fontweight='bold')

# ax1.set_yticks(range(0, 120, 20))
# ax1.set_yticklabels(ax1.get_yticks(), fontsize=40, fontfamily='Times New Roman', fontweight='bold')
ax1.grid(True)
ax1.set_title('4 Robots', fontdict=font2)

# Plot 2
line4, = ax2.plot(homogeneity_2, success_0_1_2, marker='o', label='FP = 0.1', linewidth=4, markersize=15)
line5, = ax2.plot(homogeneity_2, success_0_3_2, marker='s', label='FP = 0.3', linewidth=4, markersize=15)
line6, = ax2.plot(homogeneity_2, success_0_5_2, marker='*', label='FP = 0.5', linewidth=4, markersize=25)

ax2.set_xlabel('Homogeneity', fontdict=font2)
ax2.set_xticks(homogeneity_2[1::2])
ax2.set_xticklabels(homogeneity_2[1::2], fontsize=40, fontfamily='Times New Roman', fontweight='bold')
ax2.tick_params(axis='x', labelsize=40)

ax2.set_yticklabels(ax2.get_yticks(), fontsize=40, fontfamily='Times New Roman', fontweight='bold')
ax2.grid(True)
ax2.set_title('8 Robots', fontdict=font2)

# Shared legend
# Shared legend
fig.legend(handles=[line1, line2, line3], loc='upper center', bbox_to_anchor=(0.5, 1), prop=font3, ncol=3)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.88])

# Save figure as PDF
plt.savefig('exp-robust-combined.pdf')

# Show plot
plt.show()
