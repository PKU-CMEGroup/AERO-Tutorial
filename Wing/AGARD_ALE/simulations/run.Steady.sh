#!/bin/bash

NF=8

mpirun -N $NF aerof.opt FluidFile.Steady |& tee log.Steady.out

              


