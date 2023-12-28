#!/bin/bash

NF=8

# decompose the mesh into 4 subdomains
partnmesh sources/fluid.top $NF

# match fluid domain mesh and matcher mesh
matcher sources/fluid.top sources/matcher.top  -output data/fluidmodel


# Run Sower to pre-process the fluid mesh
sower -fluid -mesh sources/fluid.top -match data/fluidmodel.match.fluid  -dec sources/fluid.top.dec.$NF -cpu $NF -cluster $NF -output data/fluidmodel


