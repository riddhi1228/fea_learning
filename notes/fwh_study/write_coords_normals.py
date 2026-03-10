"""
Extract coordinates and compute normals from SU2 surface VTU.
For 2D cases, normals are computed from edge geometry directly.
"""
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np

filename = '/home/riddhi/SU2/TestCases/unsteady/square_cylinder/surface_flow_00001.vtu'

reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(filename)
reader.Update()
data = reader.GetOutput()

coords = vtk_to_numpy(data.GetPoints().GetData())
npts = len(coords)

# For 2D surface: normals point outward from cylinder center (0,0)
# Normal = (x,y) / ||(x,y)|| for each point
normals_xy = coords[:, :2].copy()
mags = np.linalg.norm(normals_xy, axis=1, keepdims=True)
mags[mags == 0] = 1.0
normals_xy = normals_xy / mags

# Area element (panel width) — uniform for structured surface mesh
dS = np.ones(npts) * (4.0 / npts)  # perimeter=4 for unit square / npts

# Format: x, y, z, nx, ny, nz, dS
cn = np.column_stack([
    coords,           # x, y, z
    normals_xy,       # nx, ny
    np.zeros(npts),   # nz (2D)
    dS                # panel area
])

np.savetxt('/home/riddhi/SU2PY_FWH/CoordinatesNormals.dat', cn)
print(f"Written CoordinatesNormals.dat: {npts} panels")
print(f"Sample: {cn[0]}")

# Write Observers.dat — 4 observers at distance 10 chord lengths
observers = np.array([
    [ 0.0, 10.0, 0.0],
    [10.0,  0.0, 0.0],
    [ 0.0,-10.0, 0.0],
    [-10.0, 0.0, 0.0],
])
np.savetxt('/home/riddhi/SU2PY_FWH/Observers.dat', observers)
print("Written Observers.dat: 4 observers")
