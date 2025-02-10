#!/bin/bash


NS=4

# run simulation
mpirun -n $NS aeros -d ../sources/SowerFile.optDec StructureFile
aeros -t StructureFile