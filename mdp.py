from simulator import *

class MDP:

    def __init__(self, simulator: Simulator):
        self.reset(simulator)

    def reset(self, simulator: Simulator):
        simulator.reset()
        self.navigating_around_obstacle = False

    def step(self, simulator: Simulator):
        # up_blocked := agent_row = 0 | (agent_row = (obstacle_row + 1) & agent_col = obstacle_col);
        # left_blocked := agent_col = 0 | (agent_col = (obstacle_col + 1) & agent_row = obstacle_row);
        # down_blocked := agent_row = 4 | (agent_row = (obstacle_row - 1) & agent_col = obstacle_col);
        up_blocked = simulator.agent_location[0] == 0 or (
            simulator.agent_location[0] == (simulator.obstacle_locations[0][0] + 1) 
            and simulator.agent_location[1] == simulator.obstacle_locations[0][1])
        left_blocked = simulator.agent_location[1] == 0 or (
            simulator.agent_location[1] == (simulator.obstacle_locations[0][1] + 1)
            and simulator.agent_location[0] == simulator.obstacle_locations[0][0])
        down_blocked = simulator.agent_location[0] == 4 or (
            simulator.agent_location[0] == (simulator.obstacle_locations[0][0] - 1)
            and simulator.agent_location[1] == simulator.obstacle_locations[0][1])
        
        # up_gate1_blocked := !gate1_open & (
        #     (agent_row = gate1_row & agent_col = gate1_col & gate1_dir = up) |
        #     (agent_row = (gate1_row + 1) & agent_col = gate1_col & gate1_dir = down)
        # );
        # down_gate1_blocked := !gate1_open & (
        #     (agent_row = gate1_row & agent_col = gate1_col & gate1_dir = down) |
        #     (agent_row = (gate1_row - 1) & agent_col = gate1_col & gate1_dir = up)
        # );
        # left_gate1_blocked := !gate1_open & (
        #     (agent_row = gate1_row & agent_col = gate1_col & gate1_dir = left) |
        #     (agent_row = gate1_row & agent_col = (gate1_col + 1) & gate1_dir = right)
        # );
        # right_gate1_blocked := !gate1_open & (
        #     (agent_row = gate1_row & agent_col = gate1_col & gate1_dir = right) |
        #     (agent_row = gate1_row & agent_col = (gate1_col - 1) & gate1_dir = left)
        # );
        up_gate1_blocked = simulator.gate_states[0] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[0][0] and GATE_LOCATIONS[0][1] == Direction.UP) or
            (simulator.agent_location == (GATE_LOCATIONS[0][0][0] + 1, GATE_LOCATIONS[0][0][1]) and GATE_LOCATIONS[0][1] == Direction.DOWN)
        )
        down_gate1_blocked = simulator.gate_states[0] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[0][0] and GATE_LOCATIONS[0][1] == Direction.DOWN) or
            (simulator.agent_location == (GATE_LOCATIONS[0][0][0] - 1, GATE_LOCATIONS[0][0][1]) and GATE_LOCATIONS[0][1] == Direction.UP)
        )
        left_gate1_blocked = simulator.gate_states[0] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[0][0] and GATE_LOCATIONS[0][1] == Direction.LEFT) or
            (simulator.agent_location == (GATE_LOCATIONS[0][0][0], GATE_LOCATIONS[0][0][1] + 1) and GATE_LOCATIONS[0][1] == Direction.RIGHT)
        )
        right_gate1_blocked = simulator.gate_states[0] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[0][0] and GATE_LOCATIONS[0][1] == Direction.RIGHT) or
            (simulator.agent_location == (GATE_LOCATIONS[0][0][0], GATE_LOCATIONS[0][0][1] - 1) and GATE_LOCATIONS[0][1] == Direction.LEFT)
        )

        # up_gate2_blocked := !gate2_open & (
        #     (agent_row = gate2_row & agent_col = gate2_col & gate2_dir = up) |
        #     (agent_row = (gate2_row + 1) & agent_col = gate2_col & gate2_dir = down)
        # );
        # down_gate2_blocked := !gate2_open & (
        #     (agent_row = gate2_row & agent_col = gate2_col & gate2_dir = down) |
        #     (agent_row = (gate2_row - 1) & agent_col = gate2_col & gate2_dir = up)
        # );
        # left_gate2_blocked := !gate2_open & (
        #     (agent_row = gate2_row & agent_col = gate2_col & gate2_dir = left) |
        #     (agent_row = gate2_row & agent_col = (gate2_col + 1) & gate2_dir = right)
        # );
        # right_gate2_blocked := !gate2_open & (
        #     (agent_row = gate2_row & agent_col = gate2_col & gate2_dir = right) |
        #     (agent_row = gate2_row & agent_col = (gate2_col - 1) & gate2_dir = left)
        # );

        up_gate2_blocked = simulator.gate_states[1] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[1][0] and GATE_LOCATIONS[1][1] == Direction.UP) or
            (simulator.agent_location == (GATE_LOCATIONS[1][0][0] + 1, GATE_LOCATIONS[1][0][1]) and GATE_LOCATIONS[1][1] == Direction.DOWN)
        )
        down_gate2_blocked = simulator.gate_states[1] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[1][0] and GATE_LOCATIONS[1][1] == Direction.DOWN) or
            (simulator.agent_location == (GATE_LOCATIONS[1][0][0] - 1, GATE_LOCATIONS[1][0][1]) and GATE_LOCATIONS[1][1] == Direction.UP)
        )
        left_gate2_blocked = simulator.gate_states[1] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[1][0] and GATE_LOCATIONS[1][1] == Direction.LEFT) or
            (simulator.agent_location == (GATE_LOCATIONS[1][0][0], GATE_LOCATIONS[1][0][1] + 1) and GATE_LOCATIONS[1][1] == Direction.RIGHT)
        )
        right_gate2_blocked = simulator.gate_states[1] == GateState.CLOSED and (
            (simulator.agent_location == GATE_LOCATIONS[1][0] and GATE_LOCATIONS[1][1] == Direction.RIGHT) or
            (simulator.agent_location == (GATE_LOCATIONS[1][0][0], GATE_LOCATIONS[1][0][1] - 1) and GATE_LOCATIONS[1][1] == Direction.LEFT)
        )

        # go_up := 
        # case
        #     agent_row = 0 & agent_col = 0 : FALSE;
        #     navigating_around_obstacle : FALSE;
        #     !up_blocked : TRUE;
        #     TRUE : FALSE;
        # esac;

        # go_left := 
        # case
        #     agent_row = 0 & agent_col = 0 : FALSE;
        #     go_up : FALSE;
        #     !left_blocked : TRUE;
        #     TRUE : FALSE;
        # esac;

        # go_down := 
        # case
        #     agent_row = 0 & agent_col = 0 : FALSE;
        #     go_up | go_left : FALSE;
        #     !down_blocked : TRUE;
        #     TRUE : FALSE;
        # esac;
        if simulator.agent_location == (0, 0):
            go_up = False
        elif self.navigating_around_obstacle:
            go_up = False
        elif not up_blocked:
            go_up = True
        else:
            go_up = False

        if simulator.agent_location == (0, 0):
            go_left = False
        elif go_up:
            go_left = False
        elif not left_blocked:
            go_left = True
        else:
            go_left = False

        if simulator.agent_location == (0, 0):
            go_down = False
        elif go_up or go_left:
            go_down = False
        elif not down_blocked:
            go_down = True
        else:
            go_down = False
    
        # next(navigating_around_obstacle) :=
        # case
        #     up_blocked & left_blocked : TRUE;
        #     !left_blocked & !left_gate1_blocked & !left_gate2_blocked : FALSE;
        #     TRUE : navigating_around_obstacle;
        # esac;
        if up_blocked and left_blocked:
            self.navigating_around_obstacle = True
        elif not left_blocked and not left_gate1_blocked and not left_gate2_blocked:
            self.navigating_around_obstacle = False
        else:
            pass

        if go_up and not up_gate1_blocked and not up_gate2_blocked:
            simulator.move(Direction.UP)
        elif go_left and not left_gate1_blocked and not left_gate2_blocked:
            simulator.move(Direction.LEFT)
        elif go_down and not down_gate1_blocked and not down_gate2_blocked:
            simulator.move(Direction.DOWN)
        else:
            simulator.move(Direction.NONE)
        