#!/bin/bash


#SBATCH -o Sbatch.Steady.out
#SBATCH --qos=low
#SBATCH -J NACA.EBM.Steady
#SBATCH --nodes=1 
#SBATCH --ntasks=4



source ~/.bashrc_frg


bash run.Steady.sh
bash postprocess.Steady.sh

sleep 5


