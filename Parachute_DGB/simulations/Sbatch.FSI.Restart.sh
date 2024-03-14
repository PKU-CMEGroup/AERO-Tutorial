#!/bin/bash

#SBATCH --job-name=PID.DGB.FSI.Restart
#SBATCH --output=Sbatch.FSI.Restart.out                                                   
#SBATCH --time=48:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=496



source ~/.bashrc_frg

bash run.FSI.Restart.sh

sleep 5

