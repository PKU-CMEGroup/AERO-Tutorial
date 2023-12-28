#!/bin/bash

NF=4

partnmesh sources/fluid.top $NF
sower -fluid -mesh sources/fluid.top -dec sources/fluid.top.dec.${NF} -cpu $NF -cluster $NF -output data/fluidmodel

