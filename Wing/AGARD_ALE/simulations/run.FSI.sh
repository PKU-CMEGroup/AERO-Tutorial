#!/bin/bash

NF=8
NS=1


mpirun -n $NF aerof.opt FluidFile.FSI : -n $NS aeros StructureFile.FSI |& tee log.FSI.out