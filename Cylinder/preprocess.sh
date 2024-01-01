#!/bin/bash

NS=4

aeros --dec --nsub $NS sources/SowerFile

sower -struct -mesh sources/SowerFile -dec sources/SowerFile.optDec -cpu $NS -output data/structuremodel -cluster $NS
