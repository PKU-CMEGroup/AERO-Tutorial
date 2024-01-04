#!/bin/bash

#SBATCH --job-name=Beam.EBM.Unsteady
#SBATCH --output=Sbatch.Unsteady.out                                                   
#SBATCH --time=48:00:00                                                                                                      
#SBATCH --nodes=4                                                                                                         
#SBATCH --ntasks=64  



source ~/.bashrc_frg

bash run.Unsteady.sh

sleep 5
