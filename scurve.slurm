#!/bin/bash
#SBATCH --job-name=e4_run        # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=100      # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=1G         # memory per cpu-core (4G is default)
#SBATCH --time=1:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-type=fail         # send email if job fails
#SBATCH --mail-user=ps1639@princeton.edu

source /opt/intel/oneapi/setvars.sh

#module purge
module load anaconda3/2024.10
module load intel-mkl/2024.2
module load intel/2024.2
module load intel-oneapi/2024.2
module load openmpi/oneapi-2024.2/4.1.8
#export LD_LIBRARY_PATH=/scratch/cdg4/conda/envs/gdec/lib:$LD_LIBRARY_PATH

python Scurvegen.py
#python converge_298.py
