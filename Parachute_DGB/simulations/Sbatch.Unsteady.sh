#!/bin/bash

#SBATCH --job-name=PID.DGB.Unsteady
#SBATCH --output=Sbatch.Unsteady.out                                                   
#SBATCH --time=96:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=200



source ~/.bashrc_frg

bash run.Unsteady.sh

sleep 5
