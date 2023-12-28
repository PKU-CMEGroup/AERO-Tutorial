#!/bin/bash

NF=4

mpirun -n $NF aerof.opt FluidFile.Forced |& tee log.Forced.out

