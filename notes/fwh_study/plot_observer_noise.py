"""
Visualize FWH acoustic output from Observer_Noise.dat
Author: Riddhi — GSoC 2026 pre-application study
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')  # headless
import matplotlib.pyplot as plt

data = np.loadtxt('/home/riddhi/SU2PY_FWH/Observer_Noise.dat', comments='#')
time = data[:, 0]
observers = data[:, 1:]
labels = ['Observer 0 (top, 0°)', 'Observer 1 (right, 90°)',
          'Observer 2 (bottom, 180°)', 'Observer 3 (left, 270°)']
colors = ['#2E75B6', '#E74C3C', '#27AE60', '#F39C12']

fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# Time domain
ax = axes[0]
for i in range(4):
    ax.plot(time, observers[:, i], color=colors[i], label=labels[i], linewidth=1.5)
ax.set_xlabel('Observer Time (s)', fontsize=11)
ax.set_ylabel("Acoustic Pressure p' (Pa)", fontsize=11)
ax.set_title("FWH Acoustic Pressure — Square Cylinder (Mach 0.1, Re 22000)", fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Observer geometry diagram
ax2 = axes[1]
ax2.set_xlim(-12, 12)
ax2.set_ylim(-12, 12)
ax2.set_aspect('equal')
ax2.add_patch(plt.Rectangle((-0.5, -0.5), 1, 1, color='#1F3864', zorder=5))
obs_x = [0, 10, 0, -10]
obs_y = [10, 0, -10, 0]
for i in range(4):
    ax2.plot(obs_x[i], obs_y[i], 'o', color=colors[i], markersize=12, zorder=5)
    ax2.annotate(f'Obs {i}', (obs_x[i], obs_y[i]),
                 textcoords='offset points', xytext=(8, 5), fontsize=9, color=colors[i])
    ax2.plot([0, obs_x[i]], [0, obs_y[i]], '--', color=colors[i], alpha=0.4, linewidth=1)
ax2.set_title('Observer Locations (10 chord lengths from cylinder)', fontsize=11)
ax2.set_xlabel('x/D')
ax2.set_ylabel('y/D')
ax2.grid(True, alpha=0.2)
ax2.text(0, 0, 'Square\nCylinder', ha='center', va='center',
         fontsize=7, color='white', fontweight='bold', zorder=6)

plt.tight_layout()
outpath = '/home/riddhi/fea_learning/results/fwh_square_cylinder/fwh_observer_noise.png'
import os; os.makedirs(os.path.dirname(outpath), exist_ok=True)
plt.savefig(outpath, dpi=150, bbox_inches='tight')
print(f"Saved: {outpath}")
