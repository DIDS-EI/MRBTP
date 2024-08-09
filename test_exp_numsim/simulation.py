
from mabtpg.utils.tools import print_colored
def simulation(dataset,num_agent,agents_actions,dmr):
    start = dataset["start_num"]
    goal = dataset["goal_num"]
    from mabtpg.envs.numerical_env.numerical_env import NumEnv
    env = NumEnv(num_agent=num_agent, start=start, goal=goal)
    env.set_agent_actions(dataset["total_actions"],agents_actions)

    behavior_lib = [agent.behavior_lib for agent in env.agents]
    dmr.get_btml_and_bt_ls(behavior_lib=behavior_lib,comp_actions_BTML_dic=dataset['comp_btml_ls'])

    for i,agent in enumerate(env.agents):
        agent.bind_bt(dmr.bt_ls[i])


    print_colored(f"start: {start}", "blue")
    env.print_ticks = True
    done = False
    max_env_step=500
    env_steps = 0
    new_env_step = 0
    agents_steps=0
    obs = set()
    while not done:
        print_colored(f"==================================== {env_steps} ==============================================","blue")
        obs,done,_,_,agents_one_step = env.step()
        env_steps += 1
        agents_steps += agents_one_step
        print_colored(f"state: {obs}","blue")
        if obs>=goal:
            done = True
            break
        if env_steps>=max_env_step:
            break
    print(f"\ntask finished!")
    print_colored(f"goal:{goal}", "blue")
    print("obs>=goal:",obs>=goal)
    if obs>=goal:
        done = True

    return done,env_steps,agents_steps