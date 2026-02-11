#!/bin/bash

#SBATCH -J lammps_gch
#SBATCH -p cpu
#SBATCH -n 1
#SBATCH --ntasks-per-node=40
#SBATCH -o %j.out
#SBATCH -e %j.err

module purge
module load intel-parallel-studio/cluster.2020.1

ulimit -s unlimited
ulimit -l unlimited

lmp -i in.zz
