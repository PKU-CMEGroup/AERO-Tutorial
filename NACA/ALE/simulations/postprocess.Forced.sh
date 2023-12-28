#!/bin/bash

sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Forced/Mach.bin -output postpro.Forced/Mach
    
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Forced/Pressure.bin -output postpro.Forced/Pressure
    
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Forced/PressureCoefficient.bin -output postpro.Forced/PressureCoefficient

sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
	-result results.Forced/SkinFriction.bin -output postpro.Forced/SkinFriction



xp2exo ../sources/fluid.top fluid_solution.Forced.exo \
                   postpro.Forced/Mach.xpost postpro.Forced/Pressure.xpost \
                   postpro.Forced/PressureCoefficient.xpost postpro.Forced/SkinFriction.xpost
                   




