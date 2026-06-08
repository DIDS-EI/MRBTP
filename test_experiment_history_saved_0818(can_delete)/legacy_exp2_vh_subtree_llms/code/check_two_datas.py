import json
import sys

json_type_ls = ["homo_30","llm4_homo_30_1"]


json_datasets_ls = []
for json_type in json_type_ls:
    json_path = f"vh_{json_type}.json"
    with open(json_path, 'r') as file:
        json_datasets_ls.append(json.load(file))

for data,llm_data in zip(json_datasets_ls[0],json_datasets_ls[1]):
    for key,value in llm_data.items():
        if key=="init_state" or key=="total_time" or key=="multi_robot_subtree_ls" or key=="llm_time" or  key=="reflect_times":
            continue
        d = data[key]
        l = llm_data[key]
        if key=="goal":
            d = frozenset(d)
            l = frozenset(l)
        if  d != l:
            print(data["id"])
            print(f"{key}: {data[key]} != {llm_data[key]}")
            sys.exit(1)
