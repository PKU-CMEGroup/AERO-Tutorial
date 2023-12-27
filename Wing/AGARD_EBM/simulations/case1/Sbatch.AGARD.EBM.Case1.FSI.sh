#!/bin/bash


#SBATCH -o AGARD.EBM.Case1.FSI.out
#SBATCH --qos=low
#SBATCH -J AGARD.EBM.Case1.FSI
#SBATCH --nodes=2 
#SBATCH --ntasks-per-node=18



source ~/.bashrc_frg


bash run.Steady.sh

bash run.FSI.sh

sleep 5


