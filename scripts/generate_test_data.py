"""Replace the website placeholders with website domains from env_config
Generate the test data"""
import json
import os
import argparse

from browser_env.env_config import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_family', type=str, required=True)
    return parser.parse_args()

def main(model_family='gpt') -> None:
    args = parse_args()
    DATASET = os.environ["DATASET"]
    if DATASET == "webarena":
        print("DATASET: webarena")
        print(f"REDDIT: {REDDIT}")
        print(f"SHOPPING: {SHOPPING}")
        print(f"SHOPPING_ADMIN: {SHOPPING_ADMIN}")
        print(f"GITLAB: {GITLAB}")
        print(f"WIKIPEDIA: {WIKIPEDIA}")
        print(f"MAP: {MAP}")
        print(f"HOMEPAGE: {HOMEPAGE}")
        inp_paths = ["config_files/wa/test_webarena.raw.json"]
        replace_map = {
            "__REDDIT__": REDDIT,
            "__SHOPPING__": SHOPPING,
            "__SHOPPING_ADMIN__": SHOPPING_ADMIN,
            "__GITLAB__": GITLAB,
            "__WIKIPEDIA__": WIKIPEDIA,
            "__MAP__": MAP,
            "__HOMEPAGE__": HOMEPAGE,
        }
    elif DATASET == "visualwebarena":
        print("DATASET: visualwebarena")
        print(f"CLASSIFIEDS: {CLASSIFIEDS}")
        print(f"REDDIT: {REDDIT}")
        print(f"SHOPPING: {SHOPPING}")
        print(f"HOMEPAGE: {HOMEPAGE}")
        inp_paths = [
            "config_files/vwa/test_classifieds.raw.json", "config_files/vwa/test_shopping.raw.json", "config_files/vwa/test_reddit.raw.json",
        ]
        replace_map = {
            "__REDDIT__": REDDIT,
            "__SHOPPING__": SHOPPING,
            "__WIKIPEDIA__": WIKIPEDIA,
            "__CLASSIFIEDS__": CLASSIFIEDS,
            "__HOMEPAGE__": HOMEPAGE,
        }
    else:
        raise ValueError(f"Dataset not implemented: {DATASET}")
        
    if args.model_family == "gpt":
        inp_paths = ["config_files/vwa/geo_task_gpt.raw.json"]
    elif args.model_family == "gemini":
        inp_paths = ["config_files/vwa/geo_task_gemini.raw.json"]
    elif args.model_family == 'qwen':
        inp_paths = ["config_files/vwa/geo_task_qwen.raw.json"]
    elif args.model_family == 'internvl':
        inp_paths = ["config_files/vwa/geo_task_internvl.raw.json"]
    
    for inp_path in inp_paths:
        output_dir = inp_path.replace('.raw.json', '')
        os.makedirs(output_dir, exist_ok=True)
        with open(inp_path, "r") as f:
            raw = f.read()
        for k, v in replace_map.items():
            raw = raw.replace(k, v)

        with open(inp_path.replace(".raw", ""), "w") as f:
            f.write(raw)
        data = json.loads(raw)
        for idx, item in enumerate(data):
            with open(os.path.join(output_dir, f"{idx}.json"), "w") as f:
                json.dump(item, f, indent=2)


if __name__ == "__main__":
    main()
