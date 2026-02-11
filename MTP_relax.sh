cd MTP_lammps
cd static_relax
cd data10

for i in `ls`
do
cd $i
sbatch ~/guanchaohong/Scripts/vasp.slurm
cd ../
done
cd ../../
