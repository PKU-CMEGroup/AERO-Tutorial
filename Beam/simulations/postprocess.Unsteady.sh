#!/bin/bash
NF=64

# merge results.Unsteady for original mesh
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
       -result results.Unsteady/Mach.bin  -output postpro.Unsteady/Mach -name Mach

##########################################################################################
#WARNING: the number of digits in the suffix ".01" is the length of NF
##############################################################
COUNT=$(ls -1 results.Unsteady/fluidmodel.msh.*.01 | wc -l)

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
         -mesh results.Unsteady/fluidmodel.msh.$i. -result results.Unsteady/Mach.bin.$i. \
         -output postpro.Unsteady/Mach.$i -name Mach
done

##########################################################################################


COUNT=$(ls -1 postpro.Unsteady/fluidmodel.top.???? | wc -l)

# convert mesh and results.Unsteady to exodus format for paraview
xp2exo ../sources/fluid.top postpro.Unsteady/fluidmodel.e ../sources/fluid.top.dec.$NF postpro.Unsteady/Mach.xpost
for i in $(seq -f %04.0f $COUNT);
do 
  xp2exo postpro.Unsteady/fluidmodel.top.$i postpro.Unsteady/fluidmodel.e-s.$i postpro.Unsteady/fluidmodel.top.$i.dec postpro.Unsteady/Mach.$i.xpost
done
xp2exo ../sources/embeddedSurface.top  postpro.Unsteady/EmbeddedSurfaceDisplacement.exo  postpro.Unsteady/EmbeddedSurfaceDisplacement.xpost
