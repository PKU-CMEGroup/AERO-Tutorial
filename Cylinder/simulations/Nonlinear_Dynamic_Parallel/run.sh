#!/bin/bash

NS=4

mpirun -n $NS aeros -d ../../sources/SowerFile.optDec StructureFile |& tee log.out

# postprocess solution with sower
sower -struct -merge -con ../../data/structuremodel.con -mesh ../../data/structuremodel.msh -result results/structure.GDISPLAC 
sower -struct -merge -con ../../data/structuremodel.con -mesh ../../data/structuremodel.msh -result results/structure.STRESSVM 
sower -struct -merge -con ../../data/structuremodel.con -mesh ../../data/structuremodel.msh -result results/structure.STRAINVM 


# postprocess
xp2exo ../../sources/Structure.top  structure.exo  results/structure.GDISPLAC.xpost  results/structure.STRESSVM.xpost  results/structure.STRAINVM.xpost

