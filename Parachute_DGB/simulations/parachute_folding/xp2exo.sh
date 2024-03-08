AEROS=/home/pavery/gcc/5.2/openmpi-1.8.3/FEM/bin/aeros
XP2EXO=/home/pavery/bin/xp2exo

# postprocess solution further with xp2exo
mpirun -np 1 $AEROS -t StructureFile
$XP2EXO DGB.top postpro/Case1.exo results/DGB.gdisplac.all.xpost results/DGB.stressvm.all.xpost

