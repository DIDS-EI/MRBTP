"""
example =
[
    {
        'Environment': 2,
        'Instruction': 'Place the apple on the kitchen counter and make sure the kitchen cabinet is open.',
        'Goals': ['IsOn_apple_kitchencounter', 'IsOpen_kitchencabinet'],
        'Actions': ['Walk_apple', 'RightGrab_apple', 'Walk_kitchencounter', 'RightPut_apple_kitchencounter'],
        'Vital Action Predicates': ['Walk', 'RightGrab', 'RightPut'],
        'Vital Objects': ['apple', 'kitchencounter']
    }
    ......
]
"""
# from mabtpg.algos.llm_client.tools import goal_transfer_str, act_str_process
