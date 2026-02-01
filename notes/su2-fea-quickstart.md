# Running FEA in SU2: Quick Start Notes

## Problem
Linear elasticity analysis of a 2D structure using SU2.

## What worked
- Successfully ran the direct elasticity solver
- Generated `vol_solution.vtu`
- Visualized displacement and Von Mises stress in ParaView

## What I learned
- SU2 uses configuration files to define physics, material, and boundary conditions
- Structural markers such as `clamped`, `load`, and `free` control constraints
- ParaView is essential for inspecting FEA results

## Challenges
- Adjoint-based topology optimization requires AD-enabled builds
- Building SU2 with AD support involves CODI and Meson configuration

## Next steps
- Study adjoint methods conceptually
- Start with simpler open-source contributions
