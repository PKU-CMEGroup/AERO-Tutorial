#!/bin/bash

#SBATCH --job-name=PID.DGB.Pingpong
#SBATCH --output=Sbatch.Pingpong.out                                                   
#SBATCH --time=96:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=496



source ~/.bashrc_frg

bash run.Pingpong.sh

sleep 5
