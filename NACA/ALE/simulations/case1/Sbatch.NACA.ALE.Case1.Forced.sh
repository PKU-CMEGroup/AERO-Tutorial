#!/bin/bash


#SBATCH -o NACA.ALE.Case1.Forced.out
#SBATCH --qos=low
#SBATCH -J NACA.ALE.Case1.Forced
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=4



source ~/.bashrc_frg


bash run.Forced.sh

sleep 5


