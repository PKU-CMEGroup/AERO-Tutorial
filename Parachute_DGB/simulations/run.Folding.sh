#!/bin/bash

NS=96
# multiple-domain nonlinear structure,  explicit
mpirun -n $NS aeros -d ../sources/SowerFile.optDec StructureFile.Folding
