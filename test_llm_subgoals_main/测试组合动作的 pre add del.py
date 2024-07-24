import copy


class ACT:
    def __init__(self,name,pre,add,del_set):
        self.name = name
        self.pre = pre
        self.add = add
        self.del_set = del_set

A = ACT(
    name="A",
    pre={3,6,9},
    add={5},
    del_set={1,2,3,4,'delA'},
)

B = ACT(
    name="B",
    pre={5,11,'handempty'},
    add={1},
    del_set={2,3,4,5,'handempty'},
)

C = ACT(
    name="C",
    pre={0},
    add={100},
    del_set={9},
)

cond_act_ls=[A,B,C]
# cond_act_ls=[]
# for i in range(10):
#     a=ACT()
composite_action_model = {
    "pre": set(), # 组合动作的前提条件是所有动作的前提条件，但需要减去之前所有动作的增加效果
    "add": set(), # 组合动作的增加效果是所有动作的增加效果的并集，减去它们各自其后续动作的删除效果
    "n_add": set(),
    "del_set": set(),# 组合动作的删除效果是所有动作的删除效果的并集，减去它们各自其后续动作的增加效果
}


# add
sum_del =  [set() for _ in range(len(cond_act_ls)+1)]
# sum_del[0] 表示第0个动作，所有动作的删除效果之和,包括它自己的
tmp_sum_del=set()
for i in range(len(cond_act_ls)-1,0,-1):
    print(f"{i}: {cond_act_ls[i].name}")
    tmp_sum_del |= cond_act_ls[i].del_set
    sum_del[i] = copy.deepcopy(tmp_sum_del)
print("sum_del",sum_del)


# pre
sum_add = set()
for i, a in enumerate(cond_act_ls):
    composite_action_model["pre"] |= a.pre-sum_add
    composite_action_model["add"] |= (a.add-sum_del[i+1])

    composite_action_model["del_set"] |= a.del_set
    composite_action_model["del_set"] -= a.add
    # composite_action_model["del_set"] |= (a.del_set-sum_add)

    composite_action_model["n_add"] |= a.add
    composite_action_model["n_add"] -= a.del_set

    sum_add |= a.add


# composite_action_model["add"]  = composite_action_model["add"] - composite_action_model["pre"]
# composite_action_model["del_set"] = composite_action_model["del_set"] - composite_action_model["add"]

print(composite_action_model)



