# SU2PY_FWH Bugs Found During Python 3 Porting (March 10, 2026)

## Bug B1: Python 2 print syntax (24 locations, lines 25-603)
- Error: SyntaxError: Missing parentheses in call to 'print'
- Fix: 2to3 -w SU2_FWH_Numba.py (automated conversion)
- Status: FIXED

## Bug B2: Unused pandas import (line 6)
- Error: ModuleNotFoundError: No module named 'pandas'
- Root cause: import pandas as pd — never used in 619 lines
- Fix: Remove line 6, remove from requirements
- Status: IDENTIFIED

## Bug B3: No input validation before Config() (line 470)
- Error: TypeError: 'NoneType' object is not iterable
- Root cause: Config(None) called when --configFile not provided
- Fix: if not options.config_file: parser.error('--configFile is required')
- Status: IDENTIFIED

## Bug B4: optparse with no helpful errors (CLI)
- Error: no such option: -f
- Root cause: optparse deprecated since Python 3.2, no usage help
- Fix: Replace with argparse, add required=True and help= strings
- Status: IDENTIFIED

## Bug B5: No config type validation (line 483)
- Error: KeyError: 'Config parameter not found: UNST_TIMESTEP'
- Root cause: Accepts any .cfg, crashes when UNST_TIMESTEP missing
- Fix: Validate required keys before line 483
- Status: IDENTIFIED

## Bug B6: SURFACE_OUTPUT not a valid SU2 v8.4 option
- Error: Line 115 SURFACE_OUTPUT: invalid option name
- Root cause: SU2 v8.4 uses SURFACE_PARAVIEW not SURFACE_OUTPUT
- Fix: Use OUTPUT_FILES= (RESTART_ASCII, SURFACE_PARAVIEW)
- Status: FIXED (confirmed working on square cylinder case)
