# ParaView Basics for FEA (SU2)

## Goal
Visualize displacement and stress fields from SU2 FEA simulations.

## Steps Followed
1. Opened `vol_solution.vtu` in ParaView
2. Applied:
   - Color by: Von Mises Stress
   - Warp By Vector: Displacement
3. Adjusted color scale and opacity

## Observations
- Maximum stress appears near the clamped boundary
- Deformation direction matches applied load

## Tools
- SU2
- ParaView
