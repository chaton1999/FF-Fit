#!/bin/bash
#SBATCH --job-name=my_job_0.5_1.0_12_4
#SBATCH --partition=long
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --mem=4G
#SBATCH --output=logs/water_output_0.5_1.0_12_4.log
#SBATCH --error=errors/water_error_0.5_1.0_12_4.log

# Your actual SLURM job command here
# For example, let's echo the job ID
echo "Job ID: $SLURM_JOB_ID"

conda activate p
cd /cluster/home/boittier/ff_energy/ff_energy/pydcm/tests/
python test_dcm.py --alpha 0.5 --n_factor 12 --l2 1.0 --json water.json --fname water test_N_repeats 




