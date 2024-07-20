


from mabtpg.envs.virtualhome.envs.vh_env import VHEnvTest


env = VHEnvTest()
env.reset()
# cur_cond_set = env.agents[0].condition_set = {"IsRightHandEmpty(self)", "IsLeftHandEmpty(self)",
#                                               "IsStanding(self)"}

env.comm.add_character('Chars/Female1')
env.comm.add_character('Chars/Male2')

script = ['<char0> [walk] <tv> (1)']
script2 = ['<char1> [walk] <tv> (1)']

env.run_script(script)
env.run_script(script2)