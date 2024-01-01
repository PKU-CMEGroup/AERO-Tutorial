#!/bin/bash

mpirun -n 1 aeros StructureFile |& tee log.out

# postprocess
xp2exo ../../sources/Structure.top structure.exo postpro/structure.GEIGENPA.xpost
