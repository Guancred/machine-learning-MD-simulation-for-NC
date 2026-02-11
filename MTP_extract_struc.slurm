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

mkdir -p MTP_lammps
cd MTP_lammps
mkdir -p static_relax structures XDAT_data

for file in $1 $2 $3 $4 $5
do
cp ../$file/XDATCAR XDAT_data/XDATCAR$file
done

python ../extract_structures.py
num=199

cd structures
a=`ls -l |grep "^-"|wc -l`
echo $a
cd ../

for seqs in $(seq $(($a/200)))
do
echo $seqs
mkdir static_relax/data$seqs
    for i in `ls structures/`
    do
        cd static_relax/data$seqs
        b=`ls -l |grep "^d"|wc -l`
	echo $b
        if [ $b -gt 199 ]
	then
		cd ../../
		break
        fi
        cd ../../
        mkdir static_relax/data$seqs/$i
        mv structures/$i static_relax/data$seqs/$i/POSCAR
        cp ~/guanchaohong/Scripts/MLIP-LAMMPS/INCAR static_relax/data$seqs/$i/
        cp ~/guanchaohong/Scripts/MLIP-LAMMPS/KPOINTS static_relax/data$seqs/$i/
        cp ../$1/POTCAR static_relax/data$seqs/$i/
    done

done
cd ../



