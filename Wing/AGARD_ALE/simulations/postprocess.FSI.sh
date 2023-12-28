#!/bin/bash


#postprocess fluid solution
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh -result results.FSI/Pressure.bin -output postpro.FSI/Pressure
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh -result results.FSI/Mach.bin -output postpro.FSI/Mach
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh -result results.FSI/Displacement.bin -output postpro.FSI/Displacement

#convert fluid outputs .xpost to .exo format
xp2exo ../sources/fluid.top     fluid_solution.FSI.exo        postpro.FSI/Pressure.xpost postpro.FSI/Mach.xpost postpro.FSI/Displacement.xpost 

#postprocess structure solution
xp2exo ../sources/Structure.top  structure_solution.FSI.exo   postpro.FSI/structure.GDISPLAC.xpost


