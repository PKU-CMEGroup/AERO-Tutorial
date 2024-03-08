#!/bin/bash

##########################################################################################
#WARNING: the number of digits in the suffix ".001" is the length of NF
##############################################################
COUNT=$(ls -1 results.FSI/fluidmodel.msh.*.001 | wc -l)

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
         -mesh results.FSI/fluidmodel.msh.$i. -result results.FSI/Mach.$i. \
         -output postpro.FSI/Mach.$i -name Mach
done


COUNT=$(ls -1 postpro.FSI/fluidmodel.top.???? | wc -l)

# convert mesh and results.FSI to exodus format for paraview
for i in $(seq -f %04.0f $COUNT);
do 
  xp2exo postpro.FSI/fluidmodel.top.$i postpro.FSI/fluidmodel.e-s.$i postpro.FSI/Mach.$i.xpost
done



xp2exo ../sources/embeddedSurface.top  postpro.FSI/embeddedsurface.exo \
       results.FSI/EmbeddedSurfaceDisplacement.xpost results.FSI/EmbeddedSurfacePressureCoefficient.xpost
##########################################################################################


for i in {1..2}
    do
    j=`expr $i - 1`
    echo item: $i
    sower -struct -merge -con ../data/structuremodel.con -mesh ../data/structuremodel.msh -result results.FSI/structure.GDISPLAC.$i -frequency 1 -width 20 -precision 15
    sower -struct -merge -con ../data/structuremodel.con -mesh ../data/structuremodel.msh -result results.FSI/structure.STRESSVM.$i -frequency 1 -width 20 -precision 15

    # postprocess solution further with xp2exo
    $xp2exo ../sources/Structure.top postpro.FSI/structuremodel.$j.exo results.FSI/structure.GDISPLAC.$i.xpost results.FSI/structure.STRESSVM.$i.xpost

done