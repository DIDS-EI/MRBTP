from tdw.controller import Controller
from tdw.tdw_utils import TDWUtils
from tdw.add_ons.benchmark import Benchmark

c = Controller()
b = Benchmark()
c.add_ons.append(b)
b.start()
for i in range(1000):
    c.communicate([])
b.stop()
print(b.fps)

commands = [TDWUtils.create_empty_room(12, 12)]
commands.extend(TDWUtils.create_avatar(position={"x": 0, "y": 1.5, "z": 0}))
c.communicate(commands)
b.start()
for i in range(1000):
    c.communicate([])
b.stop()
print(b.fps)
c.communicate({"$type": "terminate"})