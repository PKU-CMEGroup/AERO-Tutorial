#!/bin/bash

#SBATCH --job-name=PID.DGB.FSI.Postpro
#SBATCH --output=Sbatch.FSI.Postpro.out                                                   
#SBATCH --time=120:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=2



source ~/.bashrc_frg

bash postprocess.FSI.sh

sleep 5

