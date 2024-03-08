#!/bin/bash

#SBATCH --job-name=PID.DGB.APriori
#SBATCH --output=Sbatch.APriori.out                                                   
#SBATCH --time=96:00:00                                                                                                                                                                                                              
#SBATCH --ntasks=200



source ~/.bashrc_frg

bash run.APriori.sh

sleep 5
