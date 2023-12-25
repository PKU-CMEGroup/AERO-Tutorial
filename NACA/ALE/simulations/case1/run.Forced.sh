#!/bin/bash

NF=4

mpirun -n $NF aerof.opt FluidFile.Forced |& tee log.Forced.out

sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh \
	-result results.Forced/Mach.bin -output postpro.Forced/Mach
    
sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh \
	-result results.Forced/Pressure.bin -output postpro.Forced/Pressure
    
sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh \
	-result results.Forced/PressureCoefficient.bin -output postpro.Forced/PressureCoefficient

sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh \
	-result results.Forced/SkinFriction.bin -output postpro.Forced/SkinFriction



xp2exo ../../sources/fluid.top fluid_solution.Forced.exo \
                   ../../sources/fluid.top.dec.${NF} \
                   postpro.Forced/Mach.xpost postpro.Forced/Pressure.xpost \
                   postpro.Forced/PressureCoefficient.xpost postpro.Forced/SkinFriction.xpost
                   




