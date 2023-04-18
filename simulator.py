from enum import Enum
import random

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
NUM_GATES = 2
GATE_PROBABILITY_OPEN = 0.2
GATE_PROBABILITY_CLOSE = 0.9
OBSTACLE_LOCATIONS = [(1, 0)]
GATE_LOCATIONS = [((0, 2), Direction.RIGHT), ((0, 4), Direction.DOWN)]

COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_END = '\033[0m'

RANDOMIZE = True
# RANDOMIZE = False

class Simulator:
    
    def reset(self):
        self.agent_location = START_LOCATION
        self.gate_states = [GateState.CLOSED] * NUM_GATES
        self.obstacle_locations = OBSTACLE_LOCATIONS
        self.gate_locations = GATE_LOCATIONS
        self.breadcrumbs = [[False for x in range(GRID_WORLD_DIMENSIONS[1])] for y in range(GRID_WORLD_DIMENSIONS[0])]
        self.breadcrumbs[START_LOCATION[0]][START_LOCATION[1]] = True

        if RANDOMIZE:
            self.randomize()

    def randomize(self):
        obstacle_location = (random.randint(0, GRID_WORLD_DIMENSIONS[0] - 1), random.randint(0, GRID_WORLD_DIMENSIONS[1] - 1))
        while obstacle_location == START_LOCATION or obstacle_location == END_LOCATION:
            obstacle_location = (random.randint(0, GRID_WORLD_DIMENSIONS[0] - 1), random.randint(0, GRID_WORLD_DIMENSIONS[1] - 1))

        gate1_location = (random.randint(0, GRID_WORLD_DIMENSIONS[0] - 1), random.randint(0, GRID_WORLD_DIMENSIONS[1] - 1))
        gate2_location = (random.randint(0, GRID_WORLD_DIMENSIONS[0] - 1), random.randint(0, GRID_WORLD_DIMENSIONS[1] - 1))
        gate1_direction = random.choice(list(Direction))
        gate2_direction = random.choice(list(Direction))

        while gate1_direction == Direction.NONE:
            gate1_direction = random.choice(list(Direction))
        while gate2_direction == Direction.NONE:
            gate2_direction = random.choice(list(Direction))

        self.obstacle_locations = [obstacle_location]
        self.gate_locations = [(gate1_location, gate1_direction), (gate2_location, gate2_direction)]
         
        print("Randomized with:")
        print("Obstacle location:", obstacle_location)
        print("Gate 1 location:", gate1_location)
        print("Gate 1 direction:", gate1_direction)
        print("Gate 2 location:", gate2_location)
        print("Gate 2 direction:", gate2_direction)

    def print_grid(self):
        # print header
        print("=====================================")
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
                    print(COLOR_GREEN + 'A' + COLOR_END, end='')
                elif (r, c) == END_LOCATION:
                    print('E', end='')
                elif (r, c) in self.obstacle_locations:
                    print('B', end='')
                else:
                    if self.breadcrumbs[r][c]:
                        print(COLOR_RED + 'O' + COLOR_END, end='')
                    else:
                        print('O', end='')
                
                if gate_right_state == GateState.CLOSED:
                    print(' ║ ', end='')
                elif gate_right_state == GateState.OPEN:
                    print(' ╬ ', end='')
                else:
                    print('   ', end='')

            print()
            print('   ', end='')

            for c in range(GRID_WORLD_DIMENSIONS[1]):
                if gate_bottom_state_list[c] == GateState.CLOSED:
                    print('═══ ', end='')
                elif gate_bottom_state_list[c] == GateState.OPEN:
                    print('╬╬╬ ', end='')
                else:
                    print('    ', end='')

            print()

    def check_gate(self, location, direction) -> GateState:
        for gate_index in range(len(self.gate_locations)):
            gate = self.gate_locations[gate_index]
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
        if new_location in self.obstacle_locations:
            print("Invalid move: obstacle")
            exit(1)

        # check if there is a gate in the way
        gate_state = self.check_gate(self.agent_location, direction)
        if gate_state == GateState.CLOSED:
            print("Invalid move: gate in the way")
            exit(1)

        # update the agent location
        self.agent_location = new_location
        self.breadcrumbs[new_location[0]][new_location[1]] = True

        # determine if the gate should open or close
        for gate_index in range(len(self.gate_locations)):
            if self.gate_states[gate_index] == GateState.OPEN:
                if random.random() < GATE_PROBABILITY_CLOSE:
                    self.gate_states[gate_index] = GateState.CLOSED
            elif self.gate_states[gate_index] == GateState.CLOSED:
                if random.random() < GATE_PROBABILITY_OPEN:
                    self.gate_states[gate_index] = GateState.OPEN
    
    def agent_is_at_end(self):
        return self.agent_location == END_LOCATION