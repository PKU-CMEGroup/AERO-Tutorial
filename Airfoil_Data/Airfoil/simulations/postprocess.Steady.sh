#!/bin/bash

sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Steady/Mach.bin -output postpro.Steady/Mach
    
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Steady/Pressure.bin -output postpro.Steady/Pressure
    
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Steady/PressureCoefficient.bin -output postpro.Steady/PressureCoefficient




xp2exo ../sources/fluid.top fluid_solution.Steady.exo \
                   postpro.Steady/Mach.xpost postpro.Steady/Pressure.xpost \
                   postpro.Steady/PressureCoefficient.xpost 
                   




