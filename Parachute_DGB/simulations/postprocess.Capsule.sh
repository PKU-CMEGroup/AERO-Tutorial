#!/bin/bash

# merge results.Capsule for original mesh
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
       -result results.Capsule/Mach  -output postpro.Capsule/Mach -name Mach

##########################################################################################
#WARNING: the number of digits in the suffix ".001" is the length of NF
##############################################################
COUNT=$(ls -1 results.Capsule/fluidmodel.msh.*.001 | wc -l)

# convert the binary mesh files to xpost format
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.Capsule/fluidmodel.con.$i \
         -mesh results.Capsule/fluidmodel.msh.$i. -dec results.Capsule/fluidmodel.dec.$i.
  mv topo.xpost postpro.Capsule/fluidmodel.top.$i
  mv topo.xpost.dec postpro.Capsule/fluidmodel.top.$i.dec
done

# merge results.Capsule for refined meshes
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.Capsule/fluidmodel.con.$i \
         -mesh results.Capsule/fluidmodel.msh.$i. -result results.Capsule/Mach.$i. \
         -output postpro.Capsule/Mach.$i -name Mach
done

##########################################################################################


COUNT=$(ls -1 postpro.Capsule/fluidmodel.top.???? | wc -l)

# convert mesh and results.Capsule to exodus format for paraview
xp2exo ../sources/fluid.top postpro.Capsule/fluidmodel.e postpro.Capsule/Mach.xpost
for i in $(seq -f %04.0f $COUNT);
do 
  echo $i
  xp2exo postpro.Capsule/fluidmodel.top.$i postpro.Capsule/fluidmodel.e-s.$i postpro.Capsule/fluidmodel.top.$i.dec postpro.Capsule/Mach.$i.xpost
done