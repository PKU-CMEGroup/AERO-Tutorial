#!/bin/bash

#SBATCH --job-name=PID.DGB.Folding
#SBATCH --output=Sbatch.Folding.out                                                   
#SBATCH --time=96:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=96



source ~/.bashrc_frg

bash run.Folding.sh

sleep 5

