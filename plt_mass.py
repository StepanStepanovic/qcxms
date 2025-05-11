#! /opt/ebsofts/Python/3.8.2-GCCcore-9.3.0/bin/python
"""
Plot MS spectrum from result.csv using stem plot.

Usage:
     `result.csv` contains two columns:
    - m/z values (float)
    - intensities (float)

Output:
    - Saves high-resolution plot to fig.png
    - Displays a plot window (unless in headless mode)
"""

import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV into NumPy array
with open('result.csv') as f:
    data = np.array([[float(r) for r in l.split(',')] for l in f])

# Create stem plot: m/z vs intensity
plt.stem(data[:, 0], data[:, 1], linefmt='gray', markerfmt=' ', use_line_collection=True)
plt.xlabel(r'$\it{m/z}$', fontsize=15)
plt.ylabel(r'$\it{Intensity}$', fontsize=15)

# Annotate peaks with intensity > 50
for x, y in zip(data[:, 0], data[:, 1]):
    if y > 50:
        plt.text(x, y, f'{x:.0f}', ha='center', va='bottom', fontsize=8, color='lightgray')

# Save figure and display
plt.tight_layout()
plt.savefig('fig.png', dpi=600)
plt.show()
