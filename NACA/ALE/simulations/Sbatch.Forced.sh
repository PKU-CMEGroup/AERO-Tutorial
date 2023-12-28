#!/bin/bash


#SBATCH -o Sbatch.Forced.out
#SBATCH --qos=low
#SBATCH -J NACA.ALE.Forced
#SBATCH --nodes=1 
#SBATCH --ntasks=4



source ~/.bashrc_frg


bash run.Forced.sh
bash postprocess.Forced.sh

sleep 5


