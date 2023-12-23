#!/bin/bash

NF=4

mpirun -N $NF aerof.opt FluidFile.Steady |& tee log.Steady.out

sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh \
	-result results.Steady/Mach.bin -output postpro.Steady/Mach
    
sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh \
	-result results.Steady/Pressure.bin -output postpro.Steady/Pressure


xp2exo ../../sources/fluid.top fluid_solution.exo \
                   ../../sources/fluid.top.dec.${NF} \
                   postpro.Steady/Mach.xpost postpro.Steady/Pressure.xpost  


xp2exo ../../sources/structure.top structure_solution.exo \
                   postpro.Steady/EmbeddedSurfacePressureCoefficient.xpost




