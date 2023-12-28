#!/bin/bash

sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Steady/Mach.bin -output postpro.Steady/Mach
    
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Steady/Pressure.bin -output postpro.Steady/Pressure


xp2exo ../sources/fluid.top fluid_solution.Steady.exo \
                   postpro.Steady/Mach.xpost postpro.Steady/Pressure.xpost  


xp2exo ../sources/embeddedSurface.top embeddedSurface.Steady.exo \
                   postpro.Steady/EmbeddedSurfacePressureCoefficient.xpost




