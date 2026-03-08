"""
SU2 Topology Optimization Driver
Method: Optimality Criteria (OC)
Problem: Minimum compliance subject to volume fraction constraint

Usage:
    python3 topology_opt.py

Place this script in:
    /home/riddhi/SU2/TestCases/fea_topology/quick_start/
"""

import os
import subprocess
import numpy as np
import shutil

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
SU2_CFD    = "/home/riddhi/SU2/install/bin/SU2_CFD"
SU2_CFD_AD = "/home/riddhi/SU2/install/bin/SU2_CFD_AD"
WORKDIR    = "/home/riddhi/SU2/TestCases/fea_topology/quick_start"

CFG_DIRECT     = "settings.cfg"
CFG_COMPLIANCE = "settings_compliance.cfg"
CFG_VOLFRAC    = "settings_volfrac.cfg"

ELEM_PROPS     = "element_properties.dat"
GRAD_COMP      = "grad_compliance.dat"
GRAD_VOL       = "grad_vol_frac.dat"

N_ELEM         = 1600       # number of elements
VOL_FRAC_TARGET = 0.5       # target volume fraction (50%)
MAX_ITER       = 300        # max optimization iterations
MOVE           = 0.05        # OC move limit
ETA            = 0.5        # OC damping exponent
RHO_MIN        = 1e-3       # minimum density (avoid singularity)
RHO_MAX        = 1.0        # maximum density
CONV_TOL       = 1e-3
CONV_WINDOW      = 10       # convergence tolerance on density change
SIMP_SCHEDULE = {1: 1.0, 20: 2.0, 50: 3.0}
# ─────────────────────────────────────────────
# HELPERS
# ───────────────────────────────────────────
def read_element_properties(filepath):
    """Read densities from element_properties.dat (col 5, 0-indexed)."""
    rho = []
    rows = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            rows.append(parts)
            rho.append(float(parts[5]))
    return np.array(rho), rows

def write_element_properties(filepath, rows, rho):
    """Write updated densities back to element_properties.dat."""
    with open(filepath, "w") as f:
        for i, parts in enumerate(rows):
            parts[5] = f"{rho[i]:.6f}"
            f.write("  ".join(parts) + "\n")

def read_gradients(filepath, n):
    """Read n gradient values (one per line)."""
    vals = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                vals.append(float(line))
    return np.array(vals[:n])
def read_compliance_from_history(filepath):
    """Read the actual compliance value from SU2 history.csv."""
    try:
        with open(filepath) as f:
            lines = [l.strip() for l in f if l.strip()]
        # Find header
        header = lines[0].split(",")
        # Look for compliance column
        for keyword in ["TOPOL_COMPLIANCE", "Compliance", "compliance", "CFEA"]:
            for i, h in enumerate(header):
                if keyword.lower() in h.lower():
                    last = lines[-1].split(",")
                    return float(last[i])
        # Fallback: return last numeric value in last data line
        last = lines[-1].split(",")
        return float(last[-1])
    except Exception:
        return None

def update_simp_exponent(cfg_file, p_new):
    """Update TOPOL_OPTIM_SIMP_EXPONENT in a config file."""
    with open(cfg_file) as f:
        content = f.read()
    import re
    content = re.sub(
        r'TOPOL_OPTIM_SIMP_EXPONENT\s*=\s*[\d.]+',
        f'TOPOL_OPTIM_SIMP_EXPONENT= {p_new}',
        content
    )
    with open(cfg_file, "w") as f:
        f.write(content)
def run_su2(binary, cfg, label):
    """Run SU2 and check for success."""
    print(f"\n  → Running {label}...")
    result = subprocess.run(
        [binary, cfg],
        cwd=WORKDIR,
        capture_output=True, text=True
    )
    if "Exit Success" not in result.stdout:
        print(result.stdout[-3000:])
        print(result.stderr[-1000:])
        raise RuntimeError(f"{label} failed!")
    print(f"    ✓ {label} complete")

def oc_update(rho, dc, dv, vol_target):
    """
    Optimality Criteria density update.
    dc: compliance gradient (dC/drho)
    dv: volume gradient    (dV/drho)
    """
    # Bisection on Lagrange multiplier
    dc_smooth = np.convolve(np.abs(dc), np.ones(3)/3, mode='same')
    l1, l2 = 1e-9, 1e9
    while (l2 - l1) / (l2 + l1) > 1e-6:
        lmid = 0.5 * (l1 + l2)
        # OC update formula
        rho_new = rho * ((-dc / (dv * lmid)) ** ETA)
        # Apply move limits and bounds
        rho_new = np.maximum(RHO_MIN, np.maximum(rho - MOVE,
                  np.minimum(RHO_MAX, np.minimum(rho + MOVE, rho_new))))
        # Check volume constraint
        if rho_new.mean() > vol_target:
            l1 = lmid
        else:
            l2 = lmid
    return rho_new
def check_convergence(changes, tol, window):
    """Converged if last `window` changes all below tol."""
    if len(changes) < window:
        return False
    return all(c < tol for c in changes[-window:])

def main():
    os.chdir(WORKDIR)
    print("=" * 62)
    print("  SU2 Topology Optimization v2 — OC + SIMP Continuation")
    print(f"  Target vol fraction : {VOL_FRAC_TARGET}")
    print(f"  Move limit          : {MOVE}  (reduced for stability)")
    print(f"  SIMP schedule       : {SIMP_SCHEDULE}")
    print(f"  Conv window         : {CONV_WINDOW} iters < {CONV_TOL}")
    print("=" * 62)

    rho, rows = read_element_properties(ELEM_PROPS)
    print(f"\n  Elements: {len(rho)} | Initial density: {rho.mean():.3f}")

    history  = []
    changes  = []
    rho_prev = rho.copy()
    current_p = 1.0

    for iteration in range(1, MAX_ITER + 1):
        print(f"\n{'─'*62}")
        print(f"  ITERATION {iteration}")

        # ── SIMP continuation ────────────────────────────────────
        for start_iter, p_val in sorted(SIMP_SCHEDULE.items()):
            if iteration == start_iter:
                current_p = p_val
                update_simp_exponent(CFG_DIRECT, p_val)
                update_simp_exponent(CFG_COMPLIANCE, p_val)
                update_simp_exponent(CFG_VOLFRAC, p_val)
                print(f"  ★ SIMP exponent updated to p={p_val}")

        # ── Write densities ──────────────────────────────────────
        write_element_properties(ELEM_PROPS, rows, rho)

        # ── SU2 runs ─────────────────────────────────────────────
        run_su2(SU2_CFD,    CFG_DIRECT,     "Primal (DIRECT)")
        run_su2(SU2_CFD_AD, CFG_COMPLIANCE, "Adjoint (Compliance)")
        run_su2(SU2_CFD_AD, CFG_VOLFRAC,    "Adjoint (Vol Fraction)")

        # ── Read gradients & compliance ──────────────────────────
        dc = read_gradients(GRAD_COMP, N_ELEM)
        dv = read_gradients(GRAD_VOL,  N_ELEM)
        compliance = read_compliance_from_history("history.csv")
        if compliance is None:
            compliance = float(np.dot(np.abs(dc), rho))  # fallback

        vol_frac = float(rho.mean())

        # ── OC update ────────────────────────────────────────────
        rho_new = oc_update(rho, dc, dv, VOL_FRAC_TARGET)

        # ── Convergence check ────────────────────────────────────
        change = float(np.max(np.abs(rho_new - rho_prev)))
        changes.append(change)

        # Count solid/void/grey elements
        n_solid = int(np.sum(rho >= 0.99))
        n_void  = int(np.sum(rho <= RHO_MIN * 1.01))
        n_grey  = N_ELEM - n_solid - n_void

        print(f"  Compliance : {compliance:.6e}")
        print(f"  Vol Frac   : {vol_frac:.4f}  (target {VOL_FRAC_TARGET})")
        print(f"  Density    : solid={n_solid}  void={n_void}  grey={n_grey}")
        print(f"  Max Δρ     : {change:.6f}  (tol={CONV_TOL}, window={CONV_WINDOW})")
        print(f"  SIMP p     : {current_p}")

        history.append({
            "iter": iteration, "compliance": compliance,
            "vol_frac": vol_frac, "change": change,
            "solid": n_solid, "void": n_void, "grey": n_grey,
            "simp_p": current_p
        })

        # Save snapshot every 25 iters
        if iteration % 25 == 0:
            snap = f"density_iter_{iteration:03d}.dat"
            write_element_properties(snap, rows, rho_new)
            print(f"  Snapshot: {snap}")

        rho_prev = rho.copy()
        rho = rho_new

        if check_convergence(changes, CONV_TOL, CONV_WINDOW):
            print(f"\n  ✓ CONVERGED at iteration {iteration}!")
            break
    else:
        print(f"\n  ⚠ Max iterations ({MAX_ITER}) reached.")

    # ── Final output ─────────────────────────────────────────────
    write_element_properties(ELEM_PROPS, rows, rho)
    write_element_properties("density_final.dat", rows, rho)

    # Save history CSV
    with open("topology_opt_history_v2.csv", "w") as f:
        f.write("iter,compliance,vol_frac,change,solid,void,grey,simp_p\n")
        for h in history:
            f.write(f"{h['iter']},{h['compliance']:.8e},{h['vol_frac']:.6f},"
                    f"{h['change']:.6f},{h['solid']},{h['void']},{h['grey']},"
                    f"{h['simp_p']}\n")
    print(f"\n  History saved: topology_opt_history_v2.csv")

    # Final primal for VTU
    run_su2(SU2_CFD, CFG_DIRECT, "Final Primal")

    # Summary
    n_solid = int(np.sum(rho >= 0.99))
    n_void  = int(np.sum(rho <= RHO_MIN * 1.01))
    n_grey  = N_ELEM - n_solid - n_void
    print("\n" + "=" * 62)
    print("  OPTIMIZATION COMPLETE")
    print(f"  Final vol fraction : {rho.mean():.4f}  (target {VOL_FRAC_TARGET})")
    print(f"  Solid elements     : {n_solid} / {N_ELEM}")
    print(f"  Void  elements     : {n_void}  / {N_ELEM}")
    print(f"  Grey  elements     : {n_grey}  (ideally 0)")
    print(f"  Visualization      : vol_solution.vtu  (open in ParaView)")
    print(f"  History CSV        : topology_opt_history_v2.csv")
    print("=" * 62)

if __name__ == "__main__":
    main()
