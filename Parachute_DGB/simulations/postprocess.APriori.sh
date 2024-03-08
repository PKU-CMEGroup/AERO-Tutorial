#!/bin/bash

##########################################################################################
#WARNING: the number of digits in the suffix ".001" is the length of NF
##############################################################
COUNT=$(ls -1 results.APriori/fluidmodel.msh.*.001 | wc -l)

# convert the binary mesh files to xpost format
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.APriori/fluidmodel.con.$i \
         -mesh results.APriori/fluidmodel.msh.$i. -dec results.APriori/fluidmodel.dec.$i.
  mv topo.xpost postpro.APriori/fluidmodel.top.$i
  mv topo.xpost.dec postpro.APriori/fluidmodel.top.$i.dec
done


# merge results.APriori for refined meshes
for i in $(seq -f %04.0f 1 $COUNT);
do
  sower -fluid -merge -con results.APriori/fluidmodel.con.$i \
         -mesh results.APriori/fluidmodel.msh.$i. -result results.APriori/Pressure.bin.$i. \
         -output postpro.APriori/Pressure.$i -name Pressure
done

##########################################################################################


COUNT=$(ls -1 postpro.APriori/fluidmodel.top.???? | wc -l)

# convert mesh and results.APriori to exodus format for paraview
for i in $(seq -f %04.0f $COUNT);
do 
  xp2exo postpro.APriori/fluidmodel.top.$i postpro.APriori/fluidmodel.e-s.$i postpro.APriori/fluidmodel.top.$i.dec postpro.APriori/Pressure.$i.xpost 
done
