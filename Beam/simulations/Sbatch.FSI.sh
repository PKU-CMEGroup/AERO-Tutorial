#!/bin/bash

#SBATCH --job-name=Beam.EBM.FSI
#SBATCH --output=Sbatch.FSI.out                                                   
#SBATCH --time=96:00:00                                                                                                      
#SBATCH --nodes=4                                                                                                         
#SBATCH --ntasks=65



source ~/.bashrc_frg

bash run.FSI.sh

sleep 5
