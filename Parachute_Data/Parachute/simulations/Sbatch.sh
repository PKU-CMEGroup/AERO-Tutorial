#!/bin/bash

#SBATCH --job-name=PID.RS
#SBATCH --output=Sbatch.RS.out                                                   
#SBATCH --time=120:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=4



source ~/.bashrc_frg

bash run.sh
bash postprocess.sh

sleep 5

