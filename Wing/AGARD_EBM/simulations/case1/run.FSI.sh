#!/bin/bash


# run Steady state
mpirun -n 35 aerof.opt FluidFile.FSI : -n 1 aeros StructureFile.FSI |& tee log.FSI.out



#postprocess fluid solution
sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh -result results.FSI/Pressure.bin -output postpro.FSI/Pressure
sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh -result results.FSI/Mach.bin -output postpro.FSI/Mach


# Convert fluid outputs to .exo format
xp2exo ../../sources/fluid.top     fluid_solution.FSI.exo     postpro.FSI/Pressure.xpost postpro.FSI/Mach.xpost 
xp2exo ../../sources/embeddedSurf.top  embeddedSurf_solution.FSI.exo  postpro.FSI/EmbeddedSurfaceDisplacement.xpost postpro.FSI/EmbeddedSurfacePressureCoefficient.xpost

xp2exo ../../sources/Structure.top  structure_solution.FSI.exo postpro.FSI/structure.GDISPLAC 


