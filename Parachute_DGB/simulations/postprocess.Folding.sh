#!/bin/bash

NS=96


# postprocess solution with sower
sower -struct -merge -con ../data/structuremodel.con -mesh ../data/structuremodel.msh -result results.Folding/structure.GDISPLAC 
sower -struct -merge -con ../data/structuremodel.con -mesh ../data/structuremodel.msh -result results.Folding/structure.STRESSVM 


# postprocess
xp2exo ../sources/Structure.top  structure.Folding.exo  results.Folding/structure.GDISPLAC.xpost  results.Folding/structure.STRESSVM.xpost 
