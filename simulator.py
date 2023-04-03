from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 5

class GateState(Enum):
    OPEN = 1
    CLOSED = 2
    NONE = 3

GRID_WORLD_DIMENSIONS = (5, 5) # (width, height)
START_LOCATION = (GRID_WORLD_DIMENSIONS[0] - 1, GRID_WORLD_DIMENSIONS[1] - 1)
END_LOCATION = (0, 0)
NUM_OBSTACLES = 1
OBSTACLE_LOCATIONS = [(2, 2)]
NUM_GATES = 2
GATE_LOCATIONS = [((1, 1), Direction.DOWN), ((2, 3), Direction.RIGHT)]
# GATE_LOCATIONS = [((2, 1), Direction.UP), ((2, 4), Direction.LEFT)]

class Simulator:

    def __init__(self):
        self.reset()
        pass
    
    def reset(self):
        self.agent_location = START_LOCATION
        self.gate_states = [GateState.CLOSED] * NUM_GATES

    def print_grid(self):
        # print header
        print('    ', end='')
        for c in range(GRID_WORLD_DIMENSIONS[1]):
            print(c, end='   ')
        print()
        print()

        for r in range(GRID_WORLD_DIMENSIONS[0]):
            print(str(r) + "   ", end='')

            gate_bottom_state_list = []
            for c in range(GRID_WORLD_DIMENSIONS[1]):
                gate_right_state = self.check_gate((r, c), Direction.RIGHT)
                gate_bottom_state = self.check_gate((r, c), Direction.DOWN)

                gate_bottom_state_list.append(gate_bottom_state)

                if (r, c) == self.agent_location:
                    print('A', end='')
                elif (r, c) == END_LOCATION:
                    print('E', end='')
                elif (r, c) in OBSTACLE_LOCATIONS:
                    print('B', end='')
                else:
                    print('O', end='')
                
                if gate_right_state == GateState.CLOSED:
                    print(' ║ ', end='')
                elif gate_right_state == GateState.OPEN:
                    print(' ╬ ', end='')
                else:
                    print('   ', end='')

            print()
            print('    ', end='')

            for c in range(GRID_WORLD_DIMENSIONS[1]):
                if gate_bottom_state_list[c] == GateState.CLOSED:
                    print('═══', end='')
                elif gate_bottom_state_list[c] == GateState.OPEN:
                    print('╬╬╬', end='')
                else:
                    print('   ', end='')

            print()

    def check_gate(self, location, direction) -> GateState:
        for gate_index in range(len(GATE_LOCATIONS)):
            gate = GATE_LOCATIONS[gate_index]
            if gate[0] == location and gate[1] == direction:
                return self.gate_states[gate_index]
            # check if the gate is in the opposite direction
            if gate[1] == Direction.UP and direction == Direction.DOWN:
                if gate[0] == (location[0] + 1, location[1]):
                    return self.gate_states[gate_index]
            if gate[1] == Direction.DOWN and direction == Direction.UP:
                if gate[0] == (location[0] - 1, location[1]):
                    return self.gate_states[gate_index]
            if gate[1] == Direction.LEFT and direction == Direction.RIGHT:
                if gate[0] == (location[0], location[1] + 1):
                    return self.gate_states[gate_index]
            if gate[1] == Direction.RIGHT and direction == Direction.LEFT:
                if gate[0] == (location[0], location[1] - 1):
                    return self.gate_states[gate_index]
        return GateState.NONE

    def move(self, direction):
        new_location = ()
        if direction == Direction.UP:
            new_location = (self.agent_location[0] - 1, self.agent_location[1])
        elif direction == Direction.DOWN:
            new_location = (self.agent_location[0] + 1, self.agent_location[1])
        elif direction == Direction.LEFT:
            new_location = (self.agent_location[0], self.agent_location[1] - 1)
        elif direction == Direction.RIGHT:
            new_location = (self.agent_location[0], self.agent_location[1] + 1)
        elif direction == Direction.NONE:
            new_location = self.agent_location

        # make sure the new location is valid
        if new_location[0] < 0 or new_location[0] >= GRID_WORLD_DIMENSIONS[0] or \
            new_location[1] < 0 or new_location[1] >= GRID_WORLD_DIMENSIONS[1]:
            print("Invalid move: out of bounds")
            exit(1)
        if new_location in OBSTACLE_LOCATIONS:
            print("Invalid move: obstacle")
            exit(1)

        # check if there is a gate in the way
        gate_state = self.check_gate(self.agent_location, direction)
        if gate_state == GateState.CLOSED:
            print("Invalid move: gate in the way")
            exit(1)