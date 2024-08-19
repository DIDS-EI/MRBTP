


from mabtpg.envs.virtualhome.envs.vh_env import VHEnvTest


env = VHEnvTest()
env.reset()
# cur_cond_set = env.agents[0].condition_set = {"IsRightHandEmpty(self)", "IsLeftHandEmpty(self)",
#                                               "IsStanding(self)"}

env.comm.add_character('Chars/Female1')
env.comm.add_character('Chars/Female3')
env.comm.add_character('Chars/Male1')
env.comm.add_character('Chars/Male6')

# env.comm.add_character('Chars/Male2')

# script = ['<char0> [walk] <tv> (1)']
# script2 = ['<char1> [walk] <tv> (1)']

# script = [
# '<char0> [walk] <kitchen> (1)',
# '<char0> [find] <condimentshaker> (1)',
# '<char0> [grab] <condimentshaker> (1)',
#
#
# '<char1> [walk] <kitchen> (1)',
#     '<char1> [find] <poundcake> (1)',
#     '<char1> [grab] <poundcake> (1)',
# '<char1> [walk] <bowl> (1)',
#
#
# '<char2> [walk] <kitchen> (1)',
#     '<char2> [find] <chicken> (1)',
#     '<char2> [grab] <chicken> (1)',
#     '<char2> [walk] <fridge> (1)',
#     '<char2> [open] <fridge> (1)',
#
#     '<char0> [find] <microwave> (1)',
#     '<char0> [open] <microwave> (1)',
#     '<char0> [find] <stove> (1)',
#     '<char0> [open] <stove> (1)',
#
# '<char3> [walk] <kitchen> (1)'
#
#           '<char3> [walk] <kitchen> (1)'
#           '<char3> [grab] <wine> (1)',
#     '<char3> [walk] <kitchen> (1)'
#     '<char3> [walk] <fridge> (1)',
# '<char3> [walk] <stove> (1)',
# '<char3> [walk] <bed> (1)'
#
# '<char3> [walk] <kitchen> (1)'
#
# ]


script = [

    '<char0> [find] <stove> (1)',
    '<char0> [open] <stove> (1)',

    # '<char1> [walk] <kitchen> (1)',
    '<char1> [walk] <bowl> (1)',
    '<char1> [grab] <bowl> (1)',



          '<char3> [walk] <kitchen> (1)'
          '<char3> [grab] <wine> (1)',
        '<char3> [walk] <fridge> (1)',
        '<char3> [open] <fridge> (1)',
    '<char3> [walk] <microwave> (1)',
    '<char3> [open] <microwave> (1)',


    '<char2> [walk] <kitchen> (1)',
    '<char2> [grab] <chicken> (1)',
    '<char2> [walk] <poundcake> (1)',
    '<char2> [grab] <poundcake> (1)',
'<char2> [walk] <kitchen> (1)',


    # visit
    '<char2> [walk] <book> (1)',
'<char2> [walk] <apple> (1)',
'<char2> [walk] <fridge> (1)',
'<char2> [walk] <kitchen> (1)',

]



for s in script:
    success, message  = env.run_script([s])
    print("success:",success,"message:",message)

# env.run_script(script)
# env.run_script(script)
# env.run_script(script2)