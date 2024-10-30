#!/bin/bash


#SBATCH -o Sbatch.Generate_Data.out
#SBATCH --qos=low
#SBATCH -J NACA.Flap.Steady
#SBATCH --nodes=1 
#SBATCH --ntasks=1
#BATCH --time=12:00:00


source ~/.bashrc_frg

python generate_data.py
sleep 5


