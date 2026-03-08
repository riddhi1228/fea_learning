# MPI Error Fix for SU2 on WSL2

## Error
MPI_Win_create fails with MPI_ERR_WIN: invalid window
This happens when SU2 is built with MPI enabled on WSL2.

## Fix
Rebuild SU2 without MPI:
python3 meson.py build_nompi --prefix=/home/user/SU2/install \
  -Denable-mpi=false \
  -Denable-autodiff=true \
  -Denable-directdiff=true

## Why
WSL2's OpenMPI implementation has issues with shared memory windows.
Single machine users don't need MPI anyway.
