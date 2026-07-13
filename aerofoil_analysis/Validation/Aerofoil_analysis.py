import numpy as np
import matplotlib.pyplot as plt

# ── AoA ──────────────────────────────────────────────────────────────────────
aoa = np.array([0, 2, 4, 6, 8, 10, 12])

# ── CFD RESULTS ──────────────────────────────────────────────────────────────
CL_0012 = np.array([-5.70e-4, 2.09e-1, 4.22e-1, 6.34e-1, 8.41e-1, 1.04, 1.22])
CD_0012 = np.array([9.08e-3, 9.39e-3, 1.03e-2, 1.18e-2, 1.39e-2, 1.70e-2, 2.11e-2])

CL_4412 = np.array([4.37e-1, 6.58e-1, 8.76e-1, 1.08, 1.28, 1.47, 1.64])
CD_4412 = np.array([9.21e-3, 1.02e-2, 1.16e-2, 1.35e-2, 1.60e-2, 1.94e-2, 2.38e-2])

CL_2412 = np.array([2.18e-1, 4.38e-1, 6.56e-1, 8.72e-1, 1.08, 1.28, 1.46])
CD_2412 = np.array([8.54e-3, 9.16e-3, 1.03e-2, 1.20e-2, 1.44e-2, 1.74e-2, 2.16e-2])

# ── THIN AEROFOIL THEORY ─────────────────────────────────────────────────────
# CL = 2π(α + α_L0) where α_L0 ≈ 0 for symmetric, -2πε for cambered (ε = max camber)
aoa_fine = np.linspace(0, 12, 200)
aoa_rad  = np.radians(aoa_fine)

CL_theory_0012 = 2 * np.pi * aoa_rad                        # symmetric: zero-lift at 0°
CL_theory_2412 = 2 * np.pi * (aoa_rad + np.radians(2.34))  # NACA 2412: α_L0 ≈ -2.34°
CL_theory_4412 = 2 * np.pi * (aoa_rad + np.radians(4.00))  # NACA 4412: α_L0 ≈ -4.00°

# ── PLOT STYLE ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
})

colours = {
    '0012': '#1B6AC9',
    '2412': '#E87722',
    '4412': '#0DAB76',
    'theory': '#888888',
}

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
fig.suptitle('NACA Aerofoil CFD Analysis — Ansys Fluent (k-ω SST)\nComparison with Thin Aerofoil Theory',
             fontsize=13, fontweight='bold', y=1.01)

# ── LEFT: CL vs AoA ──────────────────────────────────────────────────────────
ax1 = axes[0]

ax1.plot(aoa_fine, CL_theory_0012, '--', color=colours['theory'], linewidth=1.2, alpha=0.6, label='Thin Aerofoil Theory')
ax1.plot(aoa_fine, CL_theory_2412, '--', color=colours['theory'], linewidth=1.2, alpha=0.6)
ax1.plot(aoa_fine, CL_theory_4412, '--', color=colours['theory'], linewidth=1.2, alpha=0.6)

ax1.plot(aoa, CL_0012, 'o-', color=colours['0012'], linewidth=2, markersize=6, label='NACA 0012 (Fluent)')
ax1.plot(aoa, CL_2412, 's-', color=colours['2412'], linewidth=2, markersize=6, label='NACA 2412 (Fluent)')
ax1.plot(aoa, CL_4412, '^-', color=colours['4412'], linewidth=2, markersize=6, label='NACA 4412 (Fluent)')

ax1.set_xlabel('Angle of Attack, α (°)', fontsize=11)
ax1.set_ylabel('Lift Coefficient, $C_L$', fontsize=11)
ax1.set_title('$C_L$ vs Angle of Attack', fontsize=12)
ax1.set_xlim(-0.5, 12.5)
ax1.legend(fontsize=9.5, framealpha=0.9)
ax1.axhline(0, color='black', linewidth=0.6, alpha=0.4)

# ── RIGHT: CD vs AoA ─────────────────────────────────────────────────────────
ax2 = axes[1]

ax2.plot(aoa, CD_0012, 'o-', color=colours['0012'], linewidth=2, markersize=6, label='NACA 0012')
ax2.plot(aoa, CD_2412, 's-', color=colours['2412'], linewidth=2, markersize=6, label='NACA 2412')
ax2.plot(aoa, CD_4412, '^-', color=colours['4412'], linewidth=2, markersize=6, label='NACA 4412')

ax2.set_xlabel('Angle of Attack, α (°)', fontsize=11)
ax2.set_ylabel('Drag Coefficient, $C_D$', fontsize=11)
ax2.set_title('$C_D$ vs Angle of Attack', fontsize=12)
ax2.set_xlim(-0.5, 12.5)
ax2.legend(fontsize=9.5, framealpha=0.9)

# ── ANNOTATION ───────────────────────────────────────────────────────────────
fig.text(0.5, -0.04,
         'CFD: Ansys Fluent 2026 R1 | Turbulence model: k-ω SST | Re ≈ 3.4×10⁶ | Freestream velocity: 50 m/s',
         ha='center', fontsize=8.5, color='#555555')

plt.tight_layout()
plt.savefig('NACA_CL_CD_comparison.png', dpi=180, bbox_inches='tight')
plt.show()
print("Plot saved as NACA_CL_CD_comparison.png")