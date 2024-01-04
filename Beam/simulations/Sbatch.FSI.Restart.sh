#!/bin/bash

#SBATCH --job-name=Beam.EBM.FSI.Restart
#SBATCH --output=Sbatch.FSI.Restart.out                                                   
#SBATCH --time=48:00:00                                                                                                      
#SBATCH --nodes=4                                                                                                         
#SBATCH --ntasks=65



source ~/.bashrc_frg

bash run.FSI.Restart.sh

sleep 5
