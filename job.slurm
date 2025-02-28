#!/bin/bash
#SBATCH --job-name=run-staged    # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=40              # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=1G         # memory per cpu-core (4G is default)
#SBATCH --time=06:30:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-type=fail         # send email if job fails
#SBATCH --mail-user=ps1639@princeton.edu

module purge
module load anaconda3/2023.9
module load intel-mkl/2020.1/1/64
module load intel/19.1/64/19.1.1.217
module load openmpi/intel-16.0/2.0.0/64

#export LD_LIBRARY_PATH=/scratch/cdg4/conda/envs/gdec/lib:$LD_LIBRARY_PATH

python run_staged.py