#!/bin/bash

#SBATCH --job-name=PID.DGB.Capsule
#SBATCH --output=Sbatch.Capsule.out                                                   
#SBATCH --time=96:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=400



source ~/.bashrc_frg

bash run.Capsule.sh

sleep 5
