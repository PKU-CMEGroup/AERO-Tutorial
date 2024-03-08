#!/bin/bash

##########################################################################################
#WARNING: the number of digits in the suffix ".001" is the length of NF
##############################################################
COUNT=$(ls -1 results.Unsteady/fluidmodel.msh.*.001 | wc -l)

# convert the binary mesh files to xpost format
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.Unsteady/fluidmodel.con.$i \
         -mesh results.Unsteady/fluidmodel.msh.$i. -dec results.Unsteady/fluidmodel.dec.$i.
  mv topo.xpost postpro.Unsteady/fluidmodel.top.$i
  mv topo.xpost.dec postpro.Unsteady/fluidmodel.top.$i.dec
done

# merge results.Unsteady for refined meshes
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.Unsteady/fluidmodel.con.$i \
         -mesh results.Unsteady/fluidmodel.msh.$i. -result results.Unsteady/Mach.$i. \
         -output postpro.Unsteady/Mach.$i -name Mach
done


COUNT=$(ls -1 postpro.Unsteady/fluidmodel.top.???? | wc -l)

# convert mesh and results.Unsteady to exodus format for paraview
for i in $(seq -f %04.0f $COUNT);
do 
  xp2exo postpro.Unsteady/fluidmodel.top.$i postpro.Unsteady/fluidmodel.e-s.$i postpro.Unsteady/Mach.$i.xpost
done
