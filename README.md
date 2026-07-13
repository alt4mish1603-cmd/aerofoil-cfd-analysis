# NACA Aerofoil Aerodynamic Analysis — Ansys Fluent CFD

An independent CFD study comparing the aerodynamic performance of three NACA aerofoil profiles across a range of angles of attack, conducted in Ansys Fluent 2026 R1 as part of a first-year Aerospace Engineering portfolio.

Three aerofoils were analysed — NACA 0012 (symmetric), NACA 2412 (low camber), and NACA 4412 (high camber) — allowing direct comparison of how camber affects lift generation, drag, and overall aerodynamic efficiency.

---

## Project Structure

```
aerofoil-cfd-analysis/
│
├── Geometry/
│   ├── NACA0012.txt          # Aerofoil coordinates (cosine-spaced)
│   ├── NACA2412.txt
│   └── NACA4412.txt
│
├── Plots/
│   └── NACA_CL_CD_comparison.png
│
└── Validation/
    └── aerofoil_validation_plot.py
```

---

## Aerofoil Profiles

Three NACA 4-digit aerofoils were selected to isolate the effect of camber on aerodynamic performance while keeping thickness consistent where possible:

| Aerofoil | Max Camber | Camber Position | Max Thickness | Type |
|----------|-----------|-----------------|---------------|------|
| NACA 0012 | 0% | — | 12% | Symmetric |
| NACA 2412 | 2% | 40% chord | 12% | Low camber |
| NACA 4412 | 4% | 40% chord | 12% | High camber |

Aerofoil coordinates were generated using the NACA 4-digit parametric equations with cosine spacing (100 points per surface) to ensure dense point distribution near the leading and trailing edges.

---

## CFD Setup

### Geometry and Domain

Each aerofoil was modelled with a chord length of 1 m. The fluid domain extends 20 chord lengths upstream and laterally, and 25 chord lengths downstream, ensuring the aerofoil wake dissipates fully before the outlet boundary. The aerofoil geometry was subtracted from the domain using a Boolean operation to produce the fluid volume for meshing.

### Mesh

An unstructured mesh was generated with local refinement along the aerofoil surface (element size 0.005 m) and 10 inflation layers applied normal to the wall to resolve the boundary layer. The inflation growth rate was set to 1.2, producing a smooth transition from the near-wall region to the freestream mesh.

| Mesh parameter | Value |
|----------------|-------|
| Surface element size | 0.005 m |
| Inflation layers | 10 |
| Growth rate | 1.2 |
| Orthogonal quality | > 0.5 |

### Solver Settings

| Parameter | Setting |
|-----------|---------|
| Solver | Pressure-based, steady-state |
| Turbulence model | k-ω SST |
| Fluid | Air, ρ = 1.225 kg/m³, μ = 1.789×10⁻⁵ kg/m·s |
| Freestream velocity | 50 m/s |
| Reynolds number | ~3.4×10⁶ |
| Inlet | Velocity inlet (X and Y components for each AoA) |
| Outlet | Pressure outlet, gauge pressure = 0 Pa |
| Aerofoil surface | No-slip wall |
| Convergence criterion | Residuals < 1×10⁻⁵ |
| Iterations | 1000 |

The k-ω SST turbulence model was selected for its superior performance in adverse pressure gradient flows and its accurate prediction of boundary layer separation — both critical for aerofoil analysis.

Angle of attack was set by decomposing the inlet velocity into X and Y components:

```
Vx = V∞ · cos(α)
Vy = V∞ · sin(α)
```

Lift and drag coefficients were extracted using force reports with direction vectors aligned to the lift and drag axes for each AoA:

```
Lift direction:  (-sin α,  cos α, 0)
Drag direction:  ( cos α,  sin α, 0)
```

---

## Results

### CL and CD Data

**NACA 0012**

| AoA (°) | CL | CD |
|---------|-------|--------|
| 0 | -0.000570 | 0.00908 |
| 2 | 0.2090 | 0.00939 |
| 4 | 0.4220 | 0.01030 |
| 6 | 0.6340 | 0.01180 |
| 8 | 0.8410 | 0.01390 |
| 10 | 1.0400 | 0.01700 |
| 12 | 1.2200 | 0.02110 |

**NACA 2412**

| AoA (°) | CL | CD |
|---------|-------|--------|
| 0 | 0.2180 | 0.00854 |
| 2 | 0.4380 | 0.00916 |
| 4 | 0.6560 | 0.01030 |
| 6 | 0.8720 | 0.01200 |
| 8 | 1.0800 | 0.01440 |
| 10 | 1.2800 | 0.01740 |
| 12 | 1.4600 | 0.02160 |

**NACA 4412**

| AoA (°) | CL | CD |
|---------|-------|--------|
| 0 | 0.4370 | 0.00921 |
| 2 | 0.6580 | 0.01020 |
| 4 | 0.8760 | 0.01160 |
| 6 | 1.0800 | 0.01350 |
| 8 | 1.2800 | 0.01600 |
| 10 | 1.4700 | 0.01940 |
| 12 | 1.6400 | 0.02380 |

### CL and CD vs Angle of Attack

![CL CD Comparison](Plots/NACA_CL_CD_comparison.png)

---

## Validation Against Thin Aerofoil Theory

Thin aerofoil theory predicts a linear CL–AoA relationship:

```
CL = 2π(α − α_L0)
```

Where α_L0 is the zero-lift angle of attack, approximately:
- NACA 0012: α_L0 = 0° (symmetric)
- NACA 2412: α_L0 ≈ −2.34°
- NACA 4412: α_L0 ≈ −4.00°

CFD results show good agreement with thin aerofoil theory across the linear range (0°–8°), with gradual divergence above 10° consistent with the onset of flow separation — a known limitation of the steady-state k-ω SST model at high incidence angles where unsteady separated flow dominates.

The cambered aerofoils (2412, 4412) confirm the expected positive zero-lift CL: NACA 4412 generates CL ≈ 0.44 at 0° AoA versus CL ≈ 0 for the symmetric NACA 0012, validating the camber-lift relationship predicted by theory.

---

## Key Observations

**1. Camber increases lift at every AoA.** At 6°, NACA 4412 achieves CL = 1.08 versus CL = 0.634 for NACA 0012 — a 70% increase in lift for the same incidence, entirely attributable to camber.

**2. Camber shifts the zero-lift angle.** NACA 0012 produces zero lift at 0° AoA; NACA 4412 produces CL = 0.437 at 0° AoA, with zero lift occurring at approximately −4°, consistent with thin aerofoil theory.

**3. Drag increases with both AoA and camber.** At 12°, NACA 4412 has CD = 0.0238 versus CD = 0.0211 for NACA 0012, reflecting the higher induced drag penalty associated with greater lift generation.

---

## What I Learned

- Setting up and running external aerodynamic CFD simulations in Ansys Fluent using the k-ω SST turbulence model
- Constructing inflation meshes for accurate boundary layer resolution
- Defining correct lift and drag force vectors as a function of angle of attack
- Extracting and post-processing aerodynamic coefficients from CFD results
- Validating computational results against analytical thin aerofoil theory
- Comparing aerodynamic performance across multiple aerofoil geometries

---

## Tools Used

- **Ansys Fluent 2026 R1** — CFD solver
- **Ansys SpaceClaim / DesignModeler** — geometry and domain setup
- **Python (NumPy, Matplotlib)** — results post-processing and validation plots

---

## Author

**Altamish Shohed**
Queen Mary University of London — MEng Aerospace Engineering (Year 1)
