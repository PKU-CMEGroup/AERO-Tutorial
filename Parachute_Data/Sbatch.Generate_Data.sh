#!/bin/bash


#SBATCH -o Sbatch.Generate_Data.out
#SBATCH --qos=low
#SBATCH -J Parachute
#SBATCH --nodes=1 
#SBATCH --ntasks=1
#BATCH --time=12:00:00


source ~/.bashrc_frg

python generate_data.py > generate_data.log
sleep 5


