#!/bin/bash


#SBATCH -o AGARD.ALE.Case1.FSI.out
#SBATCH --qos=low
#SBATCH -J AGARD.ALE.Case1.FSI
#SBATCH --nodes=1 
#SBATCH --ntasks-per-node=9



source ~/.bashrc_frg


bash run.Steady.sh

bash run.FSI.sh

sleep 5


