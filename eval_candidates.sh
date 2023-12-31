#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --job-name=eval_candidates
#SBATCH --output ../../jobs/%j.out
#SBATCH --gres=gpu:6000:1
#SBATCH --nodes=1
#SBATCH -n 3

data_dir="./data"
dataset="self_instruct"
set="test"
num_workers=1
overwrite="False"
metrics="rouge1,rouge2,rougeL,rougeLsum,bleu"
echo "dataset: $dataset"
echo "set: $set"
python eval_candidates.py \
    --data_dir $data_dir \
    --dataset $dataset \
    --set $set \
    --num_workers $num_workers \
    --metrics $metrics \
    --overwrite $overwrite \
    --save_prepared True \