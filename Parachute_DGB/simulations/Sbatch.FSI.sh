#!/bin/bash

#SBATCH --job-name=PID.DGB.FSI
#SBATCH --output=Sbatch.FSI.out                                                   
#SBATCH --time=120:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=496



source ~/.bashrc_frg

bash run.FSI.sh

sleep 5

