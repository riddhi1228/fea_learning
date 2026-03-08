# FEA & Topology Optimization — GSoC 2026 Preparation

Learning journal documenting my work with SU2 and computational mechanics,
in preparation for GSoC 2026 with the SU2 multiphysics simulation suite.

## Environment
- SU2 v8.4.0 (built from source using meson + ninja)
- ParaView 5.13.1
- OpenFOAM
- Ubuntu 22.04 (WSL2)

## What I have done
- Built SU2 v8.4.0 from source (meson + ninja)
- Ran linear elasticity simulations (clamped beam, displacement + stress fields)
- Visualized results in ParaView (stress, displacement fields)
- Studied SU2 `.cfg` configuration files for structural problems
- Studied the fea_topology test case (cantilever beam, SIMP method,
  DILATE+ERODE filter kernels, 50% volume fraction target)
- Asked questions on SU2 GitHub regarding topology optimization

## Current focus
- Running topology optimization simulation (fea_topology test case)
- Understanding SIMP penalization and density filtering in SU2
- Studying CFEASolver.cpp internals
- Drafting GSoC 2026 proposal for SU2

## GSoC 2026 Interest Area
Topology optimization and FEA solver improvements in SU2.
Specifically interested in improved Python interface support
for the structural solver and better tutorial documentation
for the topology optimization module.

## Notes
This repo is updated regularly as I progress.
Results and screenshots will be added as simulations complete.

## Results
### Topology Optimization — Cantilever Beam
![Topology Result](results/topology_optimization/topology_result.png)
*Cantilever beam, 50% volume fraction, SIMP p=3, SU2 v8.4.0*
