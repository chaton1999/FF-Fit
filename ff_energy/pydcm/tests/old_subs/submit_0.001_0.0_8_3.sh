#!/bin/bash
#SBATCH --job-name=my_job_0.001_0.0_8_3
#SBATCH --partition=long
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=4G
#SBATCH --output=logs/methanol_perm_output_0.001_0.0_8_3.log
#SBATCH --error=errors/methanol_perm_error_0.001_0.0_8_3.log

# Your actual SLURM job command here
# For example, let's echo the job ID
echo "Job ID: $SLURM_JOB_ID"

conda activate p

cd /cluster/home/boittier/ff_energy/ff_energy/pydcm/tests/
echo /cluster/home/boittier/miniforge3/envs/p/bin/python
python test_dcm.py --alpha 0.001 --n_factor 8 --l2 0.0 --json methanol_perm.json --fname methanol_perm test_N_repeats 


