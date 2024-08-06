import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 30
matplotlib.rcParams['mathtext.fontset'] = 'stix'

font1 = {'family': 'Times New Roman','color': 'Black','weight': 'bold','size': 40} #normal
font2 = {'family': 'Times New Roman','size': 26,'weight': 'bold'} # label
font3 = {'family': 'Times New Roman','size': 20,'weight': 'bold'} # legend
font4 = {'family': 'Times New Roman','color': 'Black','weight': 'bold','size': 38}

# Data
homogeneity = [1, 0.75, 0.5, 0.25,0]
# homogeneity = [1, 0.67, 0.33, 0]
success_0_1 = [96, 90, 69, 26,26]
success_0_3 = [53, 44, 16, 1,1]
success_0_5 = [10, 6, 2, 0,0]

# Plot
plt.figure(figsize=(12, 8))

plt.plot(homogeneity, success_0_1, marker='o', label='FP 0.1')
plt.plot(homogeneity, success_0_3, marker='s', label='FP 0.3')
plt.plot(homogeneity, success_0_5, marker='^', label='FP 0.5')

# Labels and Title
plt.xlabel('Homogeneity', fontdict=font2)
plt.ylabel('Success Rate (%)', fontdict=font2)
# plt.title('Success Rate vs Homogeneity for Different Failure Probabilities', fontdict=font1)

# Ticks
plt.xticks(homogeneity, fontsize=20, fontfamily='Times New Roman')
# plt.xticks(fontsize=20, fontfamily='Times New Roman')
plt.yticks(fontsize=20, fontfamily='Times New Roman')

# Legend
plt.legend(prop=font3)

# Save figure as PDF
plt.savefig('success_rate_vs_homogeneity.pdf')

# Show plot
plt.show()
