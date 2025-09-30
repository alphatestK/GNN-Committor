#!/bin/bash

export BLAS=MKL
export USE_MKLDNN=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PLUMED_NUM_THREADS=8
export OPENMM_NUM_THREADS=1


gmx_mpi grompp -f md.mdp -c ../../data/b.gro -p ../../data/topol.top -o calixarene.tpr
gmx_mpi mdrun -deffnm calixarene -plumed plumed.dat -gpu_id 0 &
