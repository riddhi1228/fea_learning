# FWH Pre-Application Study (March 10, 2026)

## What was done
- Cloned EduardoMolina/SU2PY_FWH
- Attempted to run on Ubuntu 24 / Python 3.12
- Found 5 blocking bugs (documented in BUGS_FOUND.md)
- Successfully ran unsteady square cylinder case in SU2 (50 time steps)
- Generated surface_flow_00000.vtu through surface_flow_00049.vtu

## Square cylinder case
- Mesh: mesh_square_turb_hybrid.su2 (from su2code/TestCases)
- Config: turb_square_working.cfg
- Mach: 0.1, Re: 22000, TIME_STEP: 0.0015s
- Output: SURFACE_PARAVIEW (surface pressure at each time step)

## Key config fixes required
1. RESTART_SOL= NO (no prior solution available)
2. RESTART_ITER= 1
3. OUTPUT_FILES= (RESTART_ASCII, SURFACE_PARAVIEW)
