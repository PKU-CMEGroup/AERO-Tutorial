#!/bin/bash

NF=35
NS=1
# run Steady state
mpirun -n $NF aerof.opt FluidFile.FSI : -n $NS aeros StructureFile.FSI |& tee log.FSI.out

