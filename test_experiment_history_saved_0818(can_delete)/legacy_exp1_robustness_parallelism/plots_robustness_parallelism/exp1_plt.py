import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 30
matplotlib.rcParams['mathtext.fontset'] = 'stix'

font1 = {'family': 'Times New Roman','color': 'Black','weight': 'bold','size': 40} #normal
font2 = {'family': 'Times New Roman','size': 35 ,'weight': 'bold'} # label
font3 = {'family': 'Times New Roman','size': 26 ,'weight': 'bold'} # legend
font4 = {'family': 'Times New Roman','color': 'Black','weight': 'bold','size': 38}

# Data
homogeneity = [0.25, 0.5, 0.75, 1]
success_0_1 = [42, 77, 97, 98]
success_0_3 = [4, 25, 48, 55]
success_0_5 = [0, 2, 4, 14]

# homogeneity = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1]
# success_0_1 = [42, 80, 97, 99, 100, 100, 100, 100]
# success_0_3 = [4, 42, 56, 78, 86, 82, 93, 94]
# success_0_5 = [1, 7, 10, 28, 47, 35, 42, 51]


# Plot
plt.figure(figsize=(10, 8))

plt.plot(homogeneity, success_0_1, marker='o',label='FP = 0.1', linewidth=4, markersize=15)
plt.plot(homogeneity, success_0_3, marker='s', label='FP = 0.3', linewidth=4, markersize=15)
plt.plot(homogeneity, success_0_5, marker='*', label='FP = 0.5', linewidth=4, markersize=25)

# Labels and Title
plt.xlabel('Homogeneity', fontdict=font2)
plt.ylabel('Success Rate (%)', fontdict=font2)
# plt.title('Success Rate vs Homogeneity for Different Failure Probabilities', fontdict=font1)

# Ticks
if len(homogeneity)==8:
    plt.xticks(homogeneity[1::2], fontsize=30, fontfamily='Times New Roman', fontweight='bold')
else:
    plt.xticks(homogeneity, fontsize=30, fontfamily='Times New Roman',fontweight='bold')
plt.yticks(fontsize=30, fontfamily='Times New Roman',fontweight='bold')

# Legend
plt.legend(prop=font3)
plt.grid(True)
# Adjust layout
plt.tight_layout()

# Save figure as PDF
plt.savefig(f'exp-robust-{len(homogeneity)}.pdf')

# Show plot
plt.show()
