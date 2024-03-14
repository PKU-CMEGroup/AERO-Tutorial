#!/bin/bash


NF=400

# Decompose fluid mesh
partnmesh sources/fluid.top $NF

# Run Matcher
matcher sources/embeddedSurface.top sources/matcher.mesh -l 5 -output data/fluidmodel
# if we consider fluid suspension line interaction, replace the previous line by 
# matcher sources/embeddedSurface.top sources/matcher.mesh -beam -p 16 -output data/fluidmodel

# Run Sower to pre-process the fluid mesh
sower -fluid -mesh sources/fluid.top -match data/fluidmodel.match.fluid -dec sources/fluid.top.dec.$NF -cpu $NF -cluster $NF -output data/fluidmodel


NS=96

#aeros --dec --nsub $NS sources/SowerFile

sower -struct -mesh sources/SowerFile -match data/fluidmodel.match.fem -dec sources/SowerFile.optDec -cpu $NS -output data/structuremodel -cluster $NS


