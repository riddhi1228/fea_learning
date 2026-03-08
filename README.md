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

## What I accomplished (March 8, 2026)
- Built SU2 v8.4.0 with full adjoint/AD support (reverse + forward)
- Ran primal FEA solver + both adjoint solvers (compliance + volume fraction)
- Wrote custom topology optimization driver in Python (Optimality Criteria method)
- Achieved 93% binary topology with volume constraint satisfied at exactly 0.5
- Visualized density field using pvpython headless rendering

## Current focus
- Running FADO optimization framework (pcarruscag's examples)
- Drafting GSoC 2026 proposal
- Improving convergence of custom OC optimizer

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
