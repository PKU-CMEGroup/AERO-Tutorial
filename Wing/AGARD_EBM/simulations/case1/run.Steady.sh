#!/bin/bash


# run Steady state
mpirun -n 35 aerof.opt FluidFile.Steady |& tee log.Steady.out



#postprocess fluid solution
sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh -result results.Steady/Pressure.bin -output postpro.Steady/Pressure
sower -fluid -merge -con ../../data/OUTPUT.con -mesh ../../data/OUTPUT.msh -result results.Steady/Mach.bin -output postpro.Steady/Mach


# Convert fluid outputs to .exo format
xp2exo ../../sources/fluid.top     fluid_solution.Steady.exo     postpro.Steady/Pressure.xpost postpro.Steady/Mach.xpost 



