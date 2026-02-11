cd MTP_lammps
cd static_relax

for i in `ls`
do
echo $i
cd $i
for j in `ls`
do
cd $j
a=`ls -l |grep "^-"|wc -l`
echo $a
if [ $a -lt 6 ]
then
	sbatch ~/guanchaohong/Scripts/vasp.slurm
fi
cd ../
done
cd ../
done
