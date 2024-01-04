#!/bin/bash

NF=64
NS=1
# single-domain nonlinear structure,  explicit-explicit
mpirun -n $NF aerof.opt FluidFile.FSI.Restart : -n 1 aeros StructureFile.FSI.Restart 
