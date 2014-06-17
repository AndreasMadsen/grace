#!/bin/sh
#PBS -N kmeans-gap
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=8
#PBS -m eba
#PBS -M amwebdk@gmail.com

cd $PBS_O_WORKDIR

python kmeans_gap_job.py 8
