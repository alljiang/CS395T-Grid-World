from simulator import *
from mdp import MDP

simulator = Simulator()

mdp = MDP(simulator)
simulator.print_grid()

step = 0
while not simulator.agent_is_at_end():
    print("Step", step)
    step += 1
    mdp.step(simulator)
    simulator.print_grid()
