from mabtpg.behavior_tree.base_nodes import Action
from mabtpg.behavior_tree import Status

from mabtpg.envs.gridenv.minigrid_computation_env.base.WareHouseAction import WareHouseAction

class VHAction(WareHouseAction):
    can_be_expanded = True
    num_args = 1


    SurfacePlaces = {"kitchentable","plate","nightstand","desk","cabinet","bathroomcounter","stove"} # put
    SittablePlaces =  {"bed","sofa","chair","Bench"}  # sit
    CanOpenPlaces= {"fridge","dishwasher","microwave","stove","cabinet"}  # open
    CanPutInPlaces={"fridge","dishwasher","microwave","stove","cabinet"}  # put in
    Objects={"bananas",'chicken', 'cutlets','breadslice','chips','chocolatesyrup',
             'cupcake','milk','juice','wine',
             'cutleryknife','fryingpan','dishbowl','plate',
             'book',"waterglass"
             }  # grab
    HasSwitchObjects = {"tv","faucet","lightswitch","dishwasher","coffeemaker","toaster","microwave",
                        "tablelamp","computer"}  # switch on #candle  cellphone wallphone washingmachine不行# faucet 浴室龙头


    AllObject = SurfacePlaces | SittablePlaces | CanOpenPlaces | CanPutInPlaces | Objects |\
                 HasSwitchObjects


    # ===================
    SURFACES = SurfacePlaces
    SITTABLE = SittablePlaces
    CAN_OPEN = CanOpenPlaces
    CONTAINERS = CanPutInPlaces
    GRABBABLE = Objects
    HAS_SWITCH = HasSwitchObjects



    # AllObject = SURFACES | SITTABLE | CAN_OPEN | CONTAINERS | GRABBABLE | HAS_SWITCH


    # SurfacePlaces = set()  # put
    # SittablePlaces = set()  # sit
    # CanOpenPlaces= {"fridge"}  # open
    # CanPutInPlaces=CanOpenPlaces  # put in
    # Objects={'milk','chicken',
    #          }  # grab
    # HasSwitchObjects = set()  # switch on #candle cellphone wallphone washingmachine不行# faucet 浴室龙头

    @property
    def action_class_name(self):
        return self.__class__.__name__


    def change_condition_set(self):
        pass


    def bind_agent(self, agent):
        self.agent = agent
        self.env = agent.env

        self.get_action_model()


    # def update(self):
    #     if self.env.simulation_mode == self.env.SimulationMode.computing:
    #         self.computing_update()
    #     if self.env.simulation_mode == self.env.SimulationMode.simulator:
    #         self.simulator_update()
    #
    #
    # def computing_update(self):
    #
    #     pass
    #
    # def simulator_update(self) -> Status:
    #     # script = [f'<char0> [{self.__class__.__name__.lower()}] <{self.args[0].lower()}> (1)']
    #
    #     # if self.num_args==1:
    #     #     script = [f'<char0> [{self.action_class_name.lower()}] <{self.args[0].lower()}> (1)']
    #     # else:
    #     #     script = [f'<char0> [{self.action_class_name.lower()}] <{self.args[0].lower()}> (1) <{self.args[1].lower()}> (1)']
    #
    #     if self.num_args==1:
    #         script = [f'<char0> [{self.action_class_name.lower()}] <{self.args[0].lower()}> (1)']
    #     else:
    #         script = [f'<char0> [{self.action_class_name.lower()}] <{self.args[0].lower()}> (1) <{self.args[1].lower()}> (1)']
    #
    #
    #     self.env.run_script(script,verbose=True,camera_mode="PERSON_FROM_BACK") # FIRST_PERSON
    #     print("script: ",script)
    #     self.change_condition_set()
    #
    #     return Status.RUNNING