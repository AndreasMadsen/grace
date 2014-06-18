#!/bin/sh
#PBS -N gmm-plot
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=1
#PBS -m eba
#PBS -M amwebdk@gmail.com

cd $PBS_O_WORKDIR

python gmm_plot.py
