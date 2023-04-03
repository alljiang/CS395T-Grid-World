from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

GRID_WORLD_DIMENSIONS = (5, 5) # (width, height)
END_LOCATION = (0, 0)
NUM_OBSTACLES = 1
OBSTACLE_LOCATIONS = [(2, 2)]
NUM_GATES = 2
GATE_LOCATIONS = [((1, 1), Direction.DOWN), ((2, 3), Direction.RIGHT)]
# GATE_LOCATIONS = [((2, 1), Direction.UP), ((2, 4), Direction.LEFT)]

class Simulator:

    def __init__(self):
        self.agent_location = (GRID_WORLD_DIMENSIONS[0] - 1, GRID_WORLD_DIMENSIONS[1] - 1)
        pass

    def print_grid(self):
        # print header
        print('    ', end='')
        for c in range(GRID_WORLD_DIMENSIONS[1]):
            print(c, end='   ')
        print()
        print()

        for r in range(GRID_WORLD_DIMENSIONS[0]):
            print(str(r) + "   ", end='')

            gate_on_bottom_list = []
            for c in range(GRID_WORLD_DIMENSIONS[1]):
                gate_on_right = self.check_gate((r, c), Direction.RIGHT)
                gate_on_bottom = self.check_gate((r, c), Direction.DOWN)

                gate_on_bottom_list.append(gate_on_bottom)

                if (r, c) == self.agent_location:
                    print('A', end='')
                elif (r, c) == END_LOCATION:
                    print('E', end='')
                elif (r, c) in OBSTACLE_LOCATIONS:
                    print('B', end='')
                else:
                    print('O', end='')
                
                if gate_on_right:
                    print(' ║ ', end='')
                else:
                    print('   ', end='')

            print()
            print('    ', end='')

            for c in range(GRID_WORLD_DIMENSIONS[1]):
                if gate_on_bottom_list[c]:
                    print('═══', end='')
                else:
                    print('   ', end='')

            print()

    def check_gate(self, location, direction):
        for gate in GATE_LOCATIONS:
            if gate[0] == location and gate[1] == direction:
                return True
            # check if the gate is in the opposite direction
            if gate[1] == Direction.UP and direction == Direction.DOWN:
                return gate[0] == (location[0] + 1, location[1])
            if gate[1] == Direction.DOWN and direction == Direction.UP:
                return gate[0] == (location[0] - 1, location[1])
            if gate[1] == Direction.LEFT and direction == Direction.RIGHT:
                return gate[0] == (location[0], location[1] + 1)
            if gate[1] == Direction.RIGHT and direction == Direction.LEFT:
                return gate[0] == (location[0], location[1] - 1)
            
        return False
