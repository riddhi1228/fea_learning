# Building SU2 v8.4.0 with Adjoint Support on WSL2

## Working Configuration
- OS: Ubuntu 22.04 (WSL2)
- SU2: v8.4.0 "Harrier"
- MPI: disabled (WSL2 MPI has MPI_Win_create bug)

## Correct meson command
```bash
python3 meson.py build_nompi \
  --prefix=/home/user/SU2/install \
  -Dwith-mpi=disabled \
  -Denable-autodiff=true \
  -Denable-directdiff=true
```

## Build and install
```bash
cd build_nompi
ninja -j8
ninja install
```

## Add to ~/.bashrc
```bash
export SU2_RUN=/home/user/SU2/install/bin
export SU2_HOME=/home/user/SU2
export PATH=$PATH:$SU2_RUN
export PYTHONPATH=$PYTHONPATH:$SU2_RUN
```

## Binaries location after install
- SU2_CFD → primal solver
- SU2_CFD_AD → adjoint solver (requires -Denable-autodiff=true)

## Common errors
- enable-mpi=false → wrong, use -Dwith-mpi=disabled
- MPI_Win_create error → means you're using old MPI build, use install/bin/ binaries
