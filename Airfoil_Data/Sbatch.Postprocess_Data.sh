#!/bin/bash


#SBATCH -o Sbatch.Postprocess_Data.out
#SBATCH --qos=low
#SBATCH -J NACA.Steady
#SBATCH --nodes=1 
#SBATCH --ntasks=1
#BATCH --time=12:00:00


source ~/.bashrc_frg

python postprocess_data.py
sleep 5

