"""
Convert SU2 surface VTU files to FWH binary format.
Replaces the original vtu2bin.py with Python 3 compatible version.
Author: Riddhi - GSoC 2026 pre-application study
"""
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import glob
import sys
import struct

def read_pressure_from_vtu(filename):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    data = reader.GetOutput()
    for i in range(reader.GetNumberOfPointArrays()):
        if reader.GetPointArrayName(i) == 'Pressure':
            return vtk_to_numpy(data.GetPointData().GetArray(i))
    raise ValueError(f"No Pressure field in {filename}")

def read_coords_normals_from_vtu(filename):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    data = reader.GetOutput()
    coords = vtk_to_numpy(data.GetPoints().GetData())
    # Compute normals
    normals_filter = vtk.vtkPolyDataNormals()
    surface = vtk.vtkGeometryFilter()
    surface.SetInputData(data)
    surface.Update()
    normals_filter.SetInputData(surface.GetOutput())
    normals_filter.ComputePointNormalsOn()
    normals_filter.Update()
    normals = vtk_to_numpy(normals_filter.GetOutput().GetPointData().GetNormals())
    return coords, normals

def write_binary_fwh(data_array, filename="fwh_bin.dat"):
    ntime, ndof = data_array.shape
    with open(filename, 'wb') as f:
        f.write(struct.pack('i', 535532))  # magic number
        f.write(struct.pack('i', ntime))
        f.write(struct.pack('i', ndof))
        f.write(struct.pack(f'{ntime*ndof}f', *data_array.flatten()))
    print(f"Written: {filename} ({ntime} timesteps x {ndof} panels)")

if __name__ == '__main__':
    vtu_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    files = sorted(glob.glob(f"{vtu_dir}/surface_flow_*.vtu"))
    if not files:
        raise FileNotFoundError(f"No surface_flow_*.vtu files in {vtu_dir}")
    
    print(f"Found {len(files)} VTU files")
    
    # Read pressure time series
    pressure_data = []
    for f in files:
        p = read_pressure_from_vtu(f)
        pressure_data.append(p)
        print(f"  {f}: {len(p)} points, P range [{p.min():.2f}, {p.max():.2f}]")
    
    array = np.array(pressure_data, dtype=np.float32)
    print(f"\nPressure array shape: {array.shape} (timesteps x panels)")
    write_binary_fwh(array, "fwh_bin.dat")
    
    # Write CoordinatesNormals.dat for FWH solver
    coords, normals = read_coords_normals_from_vtu(files[0])
    cn = np.column_stack([coords, normals, np.ones(len(coords))])
    np.savetxt("CoordinatesNormals.dat", cn)
    print(f"Written: CoordinatesNormals.dat ({len(coords)} panels)")
    
    # Write sample Observers.dat (4 observers around cylinder)
    observers = np.array([
        [0.0,  5.0, 0.0],
        [5.0,  0.0, 0.0],
        [0.0, -5.0, 0.0],
        [-5.0, 0.0, 0.0],
    ])
    np.savetxt("Observers.dat", observers)
    print(f"Written: Observers.dat (4 observers)")
