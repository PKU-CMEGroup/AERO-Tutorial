#!/bin/bash

NF=4

# decompose the mesh into 4 subdomains
partnmesh sources/fluid.top $NF

# preprocess distance to wall file with sower
sower -fluid -mesh sources/fluid.top -dec sources/fluid.top.dec.${NF} -cpu $NF -cluster $NF -output data/OUTPUT

# generate the distance to the wall file
cd2tet -mesh sources/fluid.top -output sources/fluid.sinus

# preprocess distance to wall file with sower
sower -fluid -split -mesh data/OUTPUT.msh -con data/OUTPUT.con -cluster ${NF} -result sources/fluid.sinus.dwall -ascii -output data/OUTPUT.dwall
