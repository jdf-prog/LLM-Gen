# LLM-Gen

## What LLM-Gen for?
Currently there are various open-source LLMs. However, different LLMs are trained with different prompting templates to function properly. 
Otherwise, you might get funny responses with problems like halluciations, repetitions, etc, damaging the quality of generation severely.

While most LLMs along with their docs are available on Hugging Face 🤗, it's really annoying to refer all those docs and get the corresponding prompting templates, 
let alone the adaptions of special tokens, eos token configuration during generation. 

Thanks to [FastChat](https://github.com/lm-sys/FastChat), who is consistently working on build a unified framework for 
most current LLMs, we could easily get the prompt format through their [`conversation.py`](https://github.com/lm-sys/FastChat/blob/main/fastchat/conversation.py)
However, while FastChat supports easy-to-build command line and web inferface, they did not provide a script 
for **large-scale generation** in our local machine. Therefore, here we implement this script with FastChat Toolkits to 
facilitate the LLM community.

## Usage

### Installation
```bash
pip install -r requirements.txt
```
### Data Formats

Please refer the example data for [`./data/self_instruct/test_data.json`](./data/self_instruct/test_data.json)
```json
[
    {
        "id": "user_oriented_task_0_instance0",
        "instruction": "The sentence you are given might be too wordy, complicated, or unclear. Rewrite the sentence and make your writing clearer by keeping it concise. Whenever possible, break complex sentences into multiple sentences and eliminate unnecessary words.",
        "input": "If you have any questions about my rate or if you find it necessary to increase or decrease the scope for this project, please let me know.",
        "output": "If you have any questions about my rate or find it necessary to increase or decrease this project's scope, please let me know.",
        "candidates": []
    },
    ...
]
```
We provide a script [`./data/format_data.py`](./data/format_data.py) to help the transforming the self-instruct format data into our generation data format above.

For example, with following bash command, you can finish the formating.
```bash
cd ./data
python format_data.py --input_file ./user_oriented_instructions.jsonl --output_file ./self_instruct/test_data.json
```

Typically, we treat each data with a dataset name and a set name (train/val/test). In the above example, `self_instruct` is the dataset name and `test` is the corresponding set name.
Each data file is expected to located at `./data/{dataset_name}/{set_name}_data.json` for the sake of generation script.

### Generation of candidates
To generate candidates for the data at `{data_dir}/{data_name}/{set_name}_data.json`, you can simply change the `data_dir` in [`_generate_candidates.sh`](./_generate_candidates.sh), 
and `{dataset_name}`, `{set_name}` in [`generate_candidates.sh`](./generate_candidates.sh), by selecting the hugging face model by `model`, you are ready to generate by running the shell
```bash
dataset="self_instruct"
set="test"
prompt_max_length=256
output_max_length=256
cmd="bash"
model="chavinlo/alpaca-13b"
${cmd} _generate_candidates.sh "$dataset" "$set" "$model" "$prompt_max_length" "$output_max_length"
```

### Evaluating Candidates

To evaluate candidates with auto metrics, you can refer to [`eval_candidates.sh`](./eval_candidates.sh)

```bash
data_dir="./data"
dataset="self_instruct"
set="test"
num_workers=1
overwrite="False"
metrics="rouge1,rouge2,rougeL,rougeLsum,bleu,bertscore,bleurt,bartscore"
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
```

By specifying `save_prepared` as `True`, the script will finally aggrerate all the candidate from all LLMs along with their evaluated scores into a single file
`./data/{dataset_name}/{set_name}_data_prepared.json`, whose format is like followings.
```json
[
    {
        "id": "unified_chip2/69962",
        "instruction": "",
        "input": "I've always wondered what the difference is between a skeptic and a denier.",
        "output": "A skeptic is someone who questions the validity of something, while a denier is someone who outright rejects something without evidence or reason.",
        "candidates": [
            {
                "decoding_method": "top_p_sampling",
                "model": "oasst-sft-4-pythia-12b-epoch-3.5",
                "text": "A skeptic is someone who doubts or expresses ...",
                "scores": {
                    "logprobs": -0.02404022216796875,
                    "bleu": 5.656152750894142,
                    "bertscore": 0.7549101114273071,
                    "rouge1": 0.2857142857142857,
                    "rouge2": 0.1272727272727273,
                    "rougeL": 0.23214285714285715,
                    "rougeLsum": 0.23214285714285715
                }
            },
            ...
        ],
    },
    ...
]
```

### Note
LLM-Gen is used to construct dataset [**MixInstruct**](https://huggingface.co/datasets/llm-blender/mix-instruct). 
It's also part of project [**LLM-Blender**](https://github.com/yuchenlin/LLM-Blender)