import json




vh_env = {
            'goal': ["IsIn(milk,fridge) "," IsIn(apple,fridge)"],
            'init_state': ["IsClosed(fridge)"],
            "objects":["milk","apple","fridge"],
            'action_space':[["Walk","Open"],["Walk","RightGrab","RightPutIn"]]
        }

# 写入 JSON 文件
with open('vh1.json', 'w') as json_file:
    json.dump(vh_env, json_file, indent=4)  # indent 参数用于使输出格式更美观


