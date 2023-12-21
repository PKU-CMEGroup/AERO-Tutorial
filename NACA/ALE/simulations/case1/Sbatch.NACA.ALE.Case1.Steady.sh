#!/bin/bash


#SBATCH -o NACA.ALE.Case1.Steady.out
#SBATCH --qos=low
#SBATCH -J NACA.ALE.Case1.Steady
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=4



source ~/.bashrc_frg


bash run.Steady.sh

sleep 5


