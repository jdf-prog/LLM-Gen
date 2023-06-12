"""
This script is used to format user-oriented instructions into the format for generation.
It will save the self-instruct data into: ./self_instruct/test_data.json

Usage: 
    python format_data.py --input_file ./user_oriented_instructions.jsonl --output_file ./self_instruct/test_data.json

You can also format other data into the format for generation by changing the input_file and output_file.
"""
import argparse
import json
import logging
from pathlib import Path


def main(args):

    logging.info(f"Start reading data from {args.input_file}")
    with open(args.input_file, "r") as f:
        data = [json.loads(line) for line in f.readlines()]
    logging.info(f"Finish reading {len(data)} instances from {args.input_file}")
    new_data = []
    for item in data:
        for i, instance in enumerate(item['instances']):
            new_item = {}
            new_item["id"] = item["id"]+f"_instance{i}"
            new_item["instruction"] = item["instruction"]
            new_item["input"] = instance["input"]
            new_item["output"] = instance["output"]
            new_item["candidates"] = []
            new_data.append(new_item)

    args.output_file = Path(args.output_file)
    args.output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(args.output_file, "w") as f:
        json.dump(new_data, f, indent=4)
    logging.info(f"Finish writing {len(new_data)} instances to {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="./user_oriented_instructions.jsonl")
    parser.add_argument("--output_file", type=str, default="./self_instruct/test_data.json")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    main(args)

