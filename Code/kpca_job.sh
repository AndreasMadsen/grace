#!/bin/sh
#PBS -N kpca
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=1
#PBS -m eba
#PBS -M frederik.ubuntu.wolgast@gmail.com

cd $PBS_O_WORKDIR

python clustering_pca_10.py 
