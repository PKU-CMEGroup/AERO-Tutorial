#!/bin/bash
NF=64

# merge results.FSI for original mesh
sower -fluid -merge -con ../data/fluidmodel.con -mesh ../data/fluidmodel.msh \
       -result results.FSI/Mach.bin  -output postpro.FSI/Mach -name Mach

##########################################################################################
#WARNING: the number of digits in the suffix ".01" is the length of NF
##############################################################
COUNT=$(ls -1 results.FSI/fluidmodel.msh.*.01 | wc -l)

# convert the binary mesh files to xpost format
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.FSI/fluidmodel.con.$i \
         -mesh results.FSI/fluidmodel.msh.$i. -dec results.FSI/fluidmodel.dec.$i.
  mv topo.xpost postpro.FSI/fluidmodel.top.$i
  mv topo.xpost.dec postpro.FSI/fluidmodel.top.$i.dec
done

# merge results.FSI for refined meshes
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.FSI/fluidmodel.con.$i \
         -mesh results.FSI/fluidmodel.msh.$i. -result results.FSI/Mach.bin.$i. \
         -output postpro.FSI/Mach.$i -name Mach
done

##########################################################################################
COUNT=$(ls -1 postpro.FSI/fluidmodel.top.???? | wc -l)

# convert mesh and results.FSI to exodus format for paraview
xp2exo ../sources/fluid.top postpro.FSI/fluidmodel.e ../sources/fluid.top.dec.$NF postpro.FSI/Mach.xpost
for i in $(seq -f %04.0f $COUNT);
do 
  xp2exo postpro.FSI/fluidmodel.top.$i postpro.FSI/fluidmodel.e-s.$i postpro.FSI/fluidmodel.top.$i.dec postpro.FSI/Mach.$i.xpost
done
xp2exo ../sources/embeddedSurface.top  postpro.FSI/EmbeddedSurfaceDisplacement.exo  postpro.FSI/EmbeddedSurfaceDisplacement.xpost
xp2exo ../sources/Structure.top        postpro.FSI/structure_solution.FSI.exo results.FSI/structure.GDISPLAC.xpost
