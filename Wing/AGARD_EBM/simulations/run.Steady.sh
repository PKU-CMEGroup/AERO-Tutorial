#!/bin/bash

NF=35
NS=1
# run Steady state
mpirun -n $NF aerof.opt FluidFile.Steady |& tee log.Steady.out

