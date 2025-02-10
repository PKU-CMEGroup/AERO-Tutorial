#!/bin/bash

##########################################################################################
#WARNING: the number of digits in the suffix ".001" is the length of NF
##########################################################################################
sower -struct -merge -con ../data/structuremodel.con -mesh ../data/structuremodel.msh -result results/structure.GDISPLAC -frequency 1 -width 20 -precision 15
sower -struct -merge -con ../data/structuremodel.con -mesh ../data/structuremodel.msh -result results/structure.STRESSVM -frequency 1 -width 20 -precision 15

# postprocess solution further with xp2exo
xp2exo ./Structure.top postpro/structuremodel.exo results/structure.GDISPLAC.xpost results/structure.STRESSVM.xpost
