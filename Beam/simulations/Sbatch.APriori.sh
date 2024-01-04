#!/bin/bash

#SBATCH --job-name=Beam.EBM.APriori
#SBATCH --output=Sbatch.APriori.out                                                   
#SBATCH --time=48:00:00                                                                                                      
#SBATCH --nodes=4                                                                                                         
#SBATCH --ntasks=64  



source ~/.bashrc_frg

bash run.APriori.sh

sleep 5
