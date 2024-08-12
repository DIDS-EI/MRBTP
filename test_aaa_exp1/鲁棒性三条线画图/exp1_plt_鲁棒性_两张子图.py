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
# heterogeneity_1 = [0.75,0.5,0.25,0]


heterogeneity_1 = [1, 0.67, 0.33,0]
heterogeneity_1=heterogeneity_1[::-1]
success_0_1_1 = [41.4, 59.8, 80.4, 94]
success_0_3_1 = [5.8, 12, 27.2, 59.4]
success_0_5_1 = [0.4, 2, 2.8, 10.4]

# success_0_1_1 = [42, 66, 91, 97]
# success_0_3_1 = [6, 17, 33, 44]
# success_0_5_1 = [2, 2, 3, 12]

# success_0_1_1 = [42, 77, 97, 98]
# success_0_3_1 = [4, 25, 48, 55]
# success_0_5_1 = [0, 2, 4, 14]

# Data 2
# heterogeneity_2 = [0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0] # [1 - x for x in original_list]
step = 1 / 7
heterogeneity_2 = [round(i * step, 2) for i in range(8)]
heterogeneity_2[-1] = int(heterogeneity_2[-1])
# heterogeneity_2 = heterogeneity_2[::-1]

success_0_1_2 = [41.4, 71.2, 94.6, 99.4, 99.2, 100, 99.6, 99.8]
success_0_3_2 = [6.2, 18.2, 46.8, 64.4, 83.6, 85.8, 88, 92.2]
success_0_5_2 = [0.6, 6.4, 7.4, 22.2, 25.4, 38.8, 38.2, 44.6]

# success_0_1_2 = [41, 72, 98, 98, 99, 100, 100, 100]
# success_0_3_2 = [5, 21, 43, 76, 80, 86, 90, 93]
# success_0_5_2 = [1, 6, 14, 15, 36, 31, 44, 45]


# success_0_1_2 = [42, 80, 97, 99, 100, 100, 100, 100]
# success_0_3_2 = [4, 42, 56, 78, 86, 82, 93, 94]
# success_0_5_2 = [1, 7, 10, 28, 47, 35, 42, 51]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), sharey=True)

# Plot 1
line1, = ax1.plot(heterogeneity_1, success_0_1_1, marker='o', label='FP = 0.1', linewidth=4, markersize=15)
line2, = ax1.plot(heterogeneity_1, success_0_3_1, marker='s', label='FP = 0.3', linewidth=4, markersize=15)
line3, = ax1.plot(heterogeneity_1, success_0_5_1, marker='*', label='FP = 0.5', linewidth=4, markersize=25)

ax1.set_xlabel('Homogeneity', fontdict=font2)
ax1.set_ylabel('Success Rate (%)', fontdict=font2)
ax1.set_xticks(heterogeneity_1)
ax1.set_xticklabels(heterogeneity_1, fontsize=40, fontfamily='Times New Roman', fontweight='bold')
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
line4, = ax2.plot(heterogeneity_2, success_0_1_2, marker='o', label='FP = 0.1', linewidth=4, markersize=15)
line5, = ax2.plot(heterogeneity_2, success_0_3_2, marker='s', label='FP = 0.3', linewidth=4, markersize=15)
line6, = ax2.plot(heterogeneity_2, success_0_5_2, marker='*', label='FP = 0.5', linewidth=4, markersize=25)

ax2.set_xlabel('Homogeneity', fontdict=font2)
ax2.set_xticks(heterogeneity_2[0:7:2]+[heterogeneity_2[-1]])
ax2.set_xticklabels(heterogeneity_2[0:7:2]+[heterogeneity_2[-1]], fontsize=40, fontfamily='Times New Roman', fontweight='bold')
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
