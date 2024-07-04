from minigrid.core.actions import Actions
from mabtpg.behavior_tree.utils import Status

class Agent(object):
    def __init__(self,env=None,id=1):
        self.env = env
        self.id = id
        self.behavior_lib = None

        self.action = Actions.done
        self.bt_success = None

        self.position = (-1, -1)
        self.direction = -1
        self.carrying = None

        self.last_tick_output = None

    def bind_bt(self,bt):
        self.bt = bt
        bt.bind_agent(self)

    def step(self):
        self.action = Actions.done
        self.bt.tick()

        bt_output = self.bt.visitor.output_str

        if bt_output != self.last_tick_output:
            if self.env.print_ticks:
                # print(f"==== time:s ======")

                print(bt_output)

                # just output action
                # 分割字符串
                # parts = bt_output.split("Action", 1)
                # # 获取 'Action' 后面的内容
                # if len(parts) > 1:
                #     bt_output = parts[1].strip()  # 使用 strip() 方法去除可能的前后空格
                # else:
                #     bt_output = ""  # 如果 'Action' 不存在于字符串中，则返回空字符串
                # print("Action ", bt_output)
                # print("\n")

                self.last_tick_output = bt_output


        self.bt_success = self.bt.root.status == Status.SUCCESS
        return self.action
