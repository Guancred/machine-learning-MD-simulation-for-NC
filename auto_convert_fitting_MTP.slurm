#!/bin/bash

#SBATCH -J gch
#SBATCH -p cpu
#SBATCH --ntasks-per-node=40
#SBATCH --output=python.out
#SBATCH -N 1
#SBATCH --exclusive

module purge
module load intel-parallel-studio/cluster.2019.5

export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export I_MPI_FABRICS=shm:ofi

ulimit -s unlimited
ulimit -l unlimited

#a=$(seq 2000)
b=1

cd MTP_lammps
mkdir -p  vasprun_files json_files
cd static_relax

for j in `ls`
do
      cd $j
      for k in `ls`
      do
         cp $k/vasprun.xml ../../vasprun_files/vasprun$b
	 b=$((b+1))
      done
      cd ../

done
cd ../../

python process_vasprun_to_mtpdata.py
python fitting-MTP.py


