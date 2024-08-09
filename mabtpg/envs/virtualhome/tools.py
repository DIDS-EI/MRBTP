

def get_classify_objects_dic():
    SURFACES = {"kitchentable", "towelrack", "bench", "kitchencabinet", "mousemat", "boardgame", "coffeetable","fryingpan", \
                "radio", "cuttingboard", "floor", "tvstand", "bathroomcounter", "oventray", "chair", "kitchencounter","rug", \
                "bookshelf", "nightstand", "cabinet", "desk", "stove", "bed", "sofa", "plate", "bathroomcabinet"}
    # 厨房桌子, 毛巾架, 长凳, 厨房橱柜, 鼠标垫, 桌游, 咖啡桌, 煎锅, \
    # 收音机, 切菜板, 地板, 电视架, 浴室台面, 烤箱托盘, 椅子, 厨房台面, 地毯, \
    # 书架, 床头柜, 柜子, 书桌, 炉灶, 床, 沙发, 盘子, 浴室橱柜

    SITTABLE = {"bathtub", "chair", "toilet", "bench", "bed", "rug", "sofa"}
    # 浴缸, 椅子, 厕所, 长凳, 床, 地毯, 沙发

    CAN_OPEN = {"coffeemaker", "cookingpot", "toothpaste", "coffeepot", "kitchencabinet", "washingmachine", "window","printer", \
                "curtains", "closet", "box", "microwave", "hairproduct", "dishwasher", "radio", "fridge", "toilet","book", \
                "garbagecan", "magazine", "nightstand", "cabinet", "milk", "desk", "stove", "door", "folder",
                "clothespile", "bathroomcabinet", "oven"}
    # 咖啡机, 烹饪锅, 牙膏, 咖啡壶, 厨房橱柜, 洗衣机, 窗户, 打印机, \
    # 窗帘, 衣柜, 盒子, 微波炉, 护发产品, 洗碗机, 收音机, 冰箱, 厕所, 书, \
    # 垃圾桶, 杂志, 床头柜, 柜子, 牛奶, 书桌, 炉灶, 门, 文件夹, 衣物堆, 浴室橱柜, 烤箱


    CONTAINERS = {"coffeemaker", "kitchencabinet", "washingmachine", "printer", "toaster", "closet", "box", "microwave",\
                  "dishwasher", "fryingpan", "fridge", "toilet", "garbagecan", "sink", "bookshelf", "nightstand","cabinet",\
                  "stove", "folder", "clothespile", "bathroomcabinet","oven","cookingpot", "desk"}
    # 咖啡机, 厨房橱柜, 洗衣机, 打印机, 烤面包机, 衣柜, 盒子, 微波炉, \
    # 洗碗机, 煎锅, 冰箱, 厕所, 垃圾桶, 水槽, 书架, 床头柜, 柜子, 炉灶, 文件夹, 衣物堆, 浴室橱柜

    GRABBABLE = {"sundae", "toothpaste", "clothesshirt", "crackers", "pudding", "alcohol", "boardgame", "wallphone","remotecontrol", \
                 "whippedcream", "hanger", "cutlets", "candybar", "wine", "toiletpaper", "slippers", "cereal", "apple","magazine", \
                 "wineglass", "milk", "cupcake", "folder", "wallpictureframe", "cellphone", "coffeepot", "crayons","box", \
                 "fryingpan", "radio", "chips", "cuttingboard", "lime", "mug", "rug", "carrot", "cutleryfork","clothespile", \
                 "notes", "plum", "cookingpot", "toy", "salmon", "peach", "condimentbottle", "hairproduct", "salad","mouse", \
                 "clock", "washingsponge", "bananas", "dishbowl", "oventray", "chocolatesyrup", "creamybuns", "pear","chair", \
                 "condimentshaker", "bellpepper", "paper", "plate", "facecream", "breadslice", "candle", "towelrack","pancake", \
                 "cutleryknife", "kitchenknife", "milkshake", "dishwashingliquid", "keyboard", "towel", "toothbrush", "book", "juice","waterglass", \
                 "barsoap", "mincedmeat", "clothespants", "chicken", "poundcake", "pillow", "pie",
                 "rag","duster","papertowel","brush"}
    # 圣代, 牙膏, 衬衫, 饼干, 布丁, 酒精, 桌游, 墙电话, 遥控器, \
    # 鲜奶油, 衣架, 切片肉, 糖果, 酒, 卫生纸, 拖鞋, 麦片, 苹果, 杂志, \
    # 酒杯, 牛奶, 纸杯蛋糕, 文件夹, 墙壁画框, 手机, 咖啡壶, 蜡笔, 盒子, \
    # 煎锅, 收音机, 薯片, 切菜板, 青柠, 杯子, 地毯, 胡落哇, 餐具叉, 衣物堆, \
    # 笔记, 李子, 烹饪锅, 玩具, 鲑鱼, 桃子, 调料瓶, 护发产品, 沙拉, 鼠标, \
    # 时钟, 洗碗海绵, 香蕉, 碗, 烤箱托盘, 巧克力糖浆, 奶油面包, 梨, 椅子, \
    # 调料瓶, 彩椒, 纸张, 盘子, 面霜, 面包片, 蜡烛, 毛巾架, 煎饼, 餐具刀, \
    # 奶昔, 洗碗液, 键盘, 毛巾, 牙刷, 书, 果汁, 水杯, 香皂, 肉末, 裤子, \
    # 鸡肉, 磅蛋糕, 枕头, 馅饼
    # 抹布, 掸子, 纸巾, 刷子


    # cleaning_tools = {"rag", "duster", "papertowel", "brush"}
    # cutting_tools={"cutleryknife","kitchenknife"}
    cleaning_tools = {"rag"}
    cutting_tools={"kitchenknife"}




    HAS_SWITCH = {"coffeemaker", "cellphone", "candle", "faucet", "washingmachine", "printer", "wallphone","remotecontrol", \
                  "computer", "toaster", "microwave", "dishwasher", "clock", "radio", "lightswitch", "fridge",
                  "tablelamp", "stove", "tv","oven"}
    # 咖啡机, 手机, 蜡烛, 水龙头, 洗衣机, 打印机, 墙电话, 遥控器, \
    # 电脑, 烤面包机, 微波炉, 洗碗机, 时钟, 收音机, 开关, 冰箱, 台灯, 炉灶, 电视

    HAS_PLUG = {"wallphone", "coffeemaker", "lightswitch", "cellphone", "fridge", "toaster", "tablelamp", "microwave", "tv", \
                "clock", "radio", "washingmachine","mouse", "keyboard", "printer","oven","dishwasher"}
    # 墙电话, 咖啡机, 开关, 手机, 冰箱, 烤面包机, 台灯, 微波炉, 电视, \
    # 鼠标, 时钟, 键盘, 收音机, 洗衣机, 打印机


    EATABLE = {"sundae", "breadslice", "whippedcream", "condimentshaker", "chocolatesyrup", "candybar", "creamybuns","pancake", \
               "poundcake", "cereal", "cupcake", "pudding", "salad", "pie", "carrot", "milkshake"}
    # 圣代, 面包片, 鲜奶油, 调料瓶, 巧克力糖浆, 糖果, 奶油面包, 煎饼, \
    # 磅蛋糕, 麦片, 纸杯蛋糕, 布丁, 沙拉, 馅饼, 胡萝卜, 奶昔

    # CUTABLE = set()
    CUTABLE = {"apple","bananas","breadslice", "cutlets","poundcake","pancake","pie","carrot","chicken","lime","salmon", "peach",\
               "pear","plum","bellpepper"}
    # 无可切割物品

    WASHABLE={"apple","bananas","carrot","chicken","lime","salmon", "peach","pear","plum","rag","cutlets"}

    RECIPIENT = {"dishbowl", "wineglass", "coffeemaker", "cookingpot", "box", "mug", "toothbrush", "coffeepot","fryingpan", \
                 "waterglass", "sink", "plate", "washingmachine"}
    # 碗, 酒杯, 咖啡机, 烹饪锅, 盒子, 杯子, 牙刷, 咖啡壶, 煎锅, \
    # 水杯, 水槽, 盘子, 洗衣机

    POURABLE = {"wineglass", "milk", "condimentshaker", "toothpaste", "bottlewater", "mug", "condimentbottle", "hairproduct", \
                "dishwashingliquid", "alcohol", "wine", "juice", "waterglass", "facecream"}
    # 酒杯, 牛奶, 调料瓶, 牙膏, 瓶装水, 杯子, 调料瓶, 护发产品, \
    # 洗碗液, 酒精, 酒, 果汁, 水杯, 面霜

    DRINKABLE = {"milk", "bottlewater", "wine", "alcohol", "juice"}
    # 牛奶, 瓶装水, 酒, 酒精, 果汁

    # switch on #candle  cellphone wallphone washingmachine不行# faucet 浴室龙头
    AllObject = SURFACES | SITTABLE | CAN_OPEN | CONTAINERS | GRABBABLE |\
                 HAS_SWITCH | CUTABLE | EATABLE | RECIPIENT | POURABLE | DRINKABLE

    # 定义类别字典
    CATEGORIES = {
        "SURFACES": SURFACES,
        # "SITTABLE": SITTABLE,
        "CAN_OPEN": CAN_OPEN,
        "CONTAINERS": CONTAINERS,
        "GRABBABLE": GRABBABLE,
        "HAS_SWITCH": HAS_SWITCH,
    }

    category_to_objects = {category: set() for category in CATEGORIES.keys()}
    object_to_category = {}

    for category, objects in CATEGORIES.items():
        for obj in objects:
            category_to_objects[category].add(obj)
            if obj in object_to_category:
                object_to_category[obj].add(category)
            else:
                object_to_category[obj] = {category}

    return category_to_objects, object_to_category

# category_to_objects, object_to_category = get_classify_objects_dic()

def add_object_to_scene(comm, object_id, class_name, target_name, target_id=None, relat_pos=[0,0,0],\
                        category=None,position=None, properties=None, rotation=[0.0, 0.0, 0.0, 1.0], scale=[1.0, 1.0, 1.0]):

    # Retrieve current environment graph
    _, env_g = comm.environment_graph()

    target_pos=[0,0,0]
    if target_id is None:
        if target_name:
            for node in env_g['nodes']:
                if node['class_name'] == target_name:
                    target_id = node['id']
                    target_pos = node['obj_transform']['position']
                    break
        if target_id is None:
            print("Target ID or name not found in environment.")
            return False, "Target not found"
            # return env_g
    position = [0]*3
    for i in range(3):
        position[i] = target_pos[i] + relat_pos[i]
    print("target_position:",target_pos)
    print("position:", position)
    # Define the new object
    new_object = {
        'id': object_id,
        'category': category if category else 'Food',  # You might want to make this a parameter if you plan to add non-food items.
        'class_name': class_name,
        'prefab_name': f'{class_name}_new_{object_id}',  # Assuming the prefab name follows a specific pattern; adjust as needed.
        'obj_transform': {
            'position': position,
            'rotation': rotation,
            'scale': scale
        },
        'bounding_box': {
            'center': position,
            'size': [0.13, 0.24, 0.13]  # You might need a way to set this based on the object.
        },
        'properties': properties if properties else ['GRABBABLE','MOVABLE','CAN_OPEN'],
        'states': []  # Assuming default state; adjust as needed.  'CLOSED'
    }

    # Define the relation
    new_relation = [{
        "from_id": object_id,
        "to_id": target_id,   # target_id,
        # "relation_type": "ON"
        "relation_type": "INSIDE"
    },
    {
        "from_id": object_id,
        "to_id": 127,   # target_id,
        "relation_type": "ON"
        # "relation_type": "INSIDE"
    }]


    # Add the new object and relation to the environment graph
    env_g['nodes'].append(new_object)
    for rel in new_relation:
        env_g['edges'].append(rel)

    # Expand the scene with the new object
    success, message = comm.expand_scene(env_g)
    print(f"Expansion result: {success}, {message}")

    return success, message
    # return env_g

# Final id = 358
# Fridge  id 162, 163   category Appliances
# Milk  category food
# new_nodes = [
#       {'id': 400,
#        'category': 'Food',
#        'class_name': 'milk',
#        'prefab_name': 'Milk_myx',   # FMGP_PRE_Milk_1024
#        'obj_transform':
#            {'position': [-9.487717, 2.50537186e-06, 1.3743968],# [-9.487717, 2.20537186e-06, 1.3743968]
#             'rotation': [0.0, 0.0, 0.0, 1.0],
#             'scale': [1.0, 1.0, 1.0]},
#        'bounding_box': {
#            'center': [-9.487717, 2.50537186e-06, 1.3743968],
#            'size': [0.123023987, 0.240758, 0.123024985]},
#        'properties': ['GRABBABLE', 'DRINKABLE', 'POURABLE', 'CAN_OPEN', 'MOVABLE'],
#        'states': ['CLOSED']},
#    ]
# new_edges = [
#       {
#          "from_id":400,
#          "to_id": 162, #138,
#          "relation_type":"INSIDE"
#       }
#    ]
#
# _, env_g = comm.environment_graph()
# # print("graph:",env_g['nodes'])
# for i in range(len(new_nodes)):
#     env_g['nodes'].append(new_nodes[i])
# for i in range(len(new_edges)):
#     env_g['edges'].append(new_edges[i])
# success, message = comm.expand_scene(env_g)
# print("exp:",success,message)