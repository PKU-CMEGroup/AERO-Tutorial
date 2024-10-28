#!/bin/bash

NF=4

mpirun -n $NF aerof.opt FluidFile.Steady |& tee log.Steady.out

