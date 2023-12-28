#!/bin/bash

NF=35
NS=1
# run Steady state
mpirun -n $NF aerof.opt FluidFile.FSI : -n $NS aeros StructureFile.FSI |& tee log.FSI.out



#postprocess fluid solution
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh -result results.FSI/Pressure.bin -output postpro.FSI/Pressure
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh -result results.FSI/Mach.bin -output postpro.FSI/Mach


# Convert fluid outputs to .exo format
xp2exo ../sources/fluid.top     fluid_solution.FSI.exo     postpro.FSI/Pressure.xpost postpro.FSI/Mach.xpost 
xp2exo ../sources/embeddedSurface.top  embeddedSurface.FSI.exo  postpro.FSI/EmbeddedSurfaceDisplacement.xpost postpro.FSI/EmbeddedSurfacePressureCoefficient.xpost

xp2exo ../sources/Structure.top  structure_solution.FSI.exo postpro.FSI/structure.GDISPLAC.xpost 


