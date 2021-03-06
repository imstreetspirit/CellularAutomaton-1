from Simulation.SimCell import SimCell
from Simulation.Pedestarian import Pedestarian
from typing import List
import math
from random import randint
class SimGrid:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = []
        self.targetCell = None # type: List[List[SimCell]]
        self.sim_time = 0
        self.persons = [] # type: List[Pedestarian]
        for row in range(size_y):
            line = []
            for column in range(size_x):
                line.append(SimCell(column, row))
            self.grid.append(line)

    def get_grid(self):
        return self.grid

    def print_grid(self):
        for i in range(0, self.size_y):
            for j in range(0, self.size_x):
                print(self.grid[i][j].distance, end="  ")
            print(" ")

        for i in range(0, self.size_y):
            for j in range(0, self.size_x):
                print(self.grid[i][j].state, end="  ")
            print(" ")

    def set_target(self, x, y):
        self.targetCell = SimCell(x, y)
        self.grid[y][x].set_state('T')

    def get_pedestrians(self):
        indices = [[i, j] for i, row in enumerate(self.grid) \
                   for j, cell in enumerate(row) if cell.state == "P"]
        return indices

    def set_pedestarians(self, ped_list: List):
        speeds = [10, 20, 50, 100]
        for value in ped_list:
            self.grid[value[0]][value[1]].state = 'P'
            self.grid[value[0]][value[1]].next_state = 'P'
            self.persons.append(Pedestarian(value[0], value[1], speeds[randint(0,len(speeds) - 1)]))

    def set_obstacles(self, obs_list: List):
        for value in obs_list:
            self.grid[value[0]][value[1]].set_state('O')

    def update_utilities(self):
        for row in range(self.size_y):
            for column in range(self.size_x):
                    self.grid[row][column].update_utility_score(self.targetCell)

    def update_distances(self):
        row = self.targetCell.y
        column = self.targetCell.x
        i = self.size_x * self.size_y - 1
        min_x, min_y = self.find_distance_to_target(row, column)
        while(i >= 0):
            #print(min_x, min_y)
            min_x, min_y = self.find_distance_to_target(min_x, min_y)
            if min_x == -1 or min_y == -1:
                min_x, min_y = self.find_new_cell()
                if min_x == -2 or min_y == -2:
                    i = -1
            i -= 1

    def find_new_cell(self):
        smallest = math.inf
        r = -2
        c = -2
        for row in range(self.size_y):
            for column in range(self.size_x):
                if self.grid[row][column].get_distance() < math.inf and not self.grid[row][column].is_visited():
                    if smallest >= self.grid[row][column].get_distance():
                        smallest = self.grid[row][column].get_distance()
                        r, c = row, column
        return r, c



    def simulate_next_step(self, dijsktra=False):
        for row in range(self.size_y):
            for column in range(self.size_x):
                self.grid[row][column].set_next_state()

    def simulate_one_step(self, dijsktra=False):
        for person in self.persons:
            row = person.y
            column = person.x
            if self.grid[row][column].is_person() and person.is_active():
                if self.sim_time % person.adj_speed == 0:
                    if self.update_movement(row, column, dijsktra, person):
                        self.grid[row][column].set_state('E')
        self.sim_time += 1

    def update_movement(self, row, column, dijsktra, person):
        neighbouring_cells = {}
        if row != 0 and self.grid[row - 1][column].is_available():
            if self.grid[row - 1][column].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row - 1, column)] = self.grid[row - 1][column].get_score(dijsktra) + self.get_avoidance_score(row - 1, column)

        if column != 0 and self.grid[row][column -1].is_available():
            if self.grid[row][column - 1].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row, column - 1)] = self.grid[row][column - 1].get_score(dijsktra) + self.get_avoidance_score(row, column - 1)

        if row !=0 and column !=0 and self.grid[row - 1][column - 1].is_available():
            if self.grid[row - 1][column - 1].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row-1, column-1)] = self.grid[row - 1][column-1].get_score(dijsktra) + self.get_avoidance_score(row-1, column - 1)

        if row != self.size_y - 1 and self.grid[row + 1][column].is_available():
            if self.grid[row+1][column].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row+1, column)] = self.grid[row + 1][column].get_score(dijsktra) + self.get_avoidance_score(row+1, column)

        if column != self.size_x - 1 and self.grid[row][column + 1].is_available():
            if self.grid[row][column + 1].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row, column+1)] = self.grid[row][column+1].get_score(dijsktra) + self.get_avoidance_score(row, column + 1)

        if row != self.size_y - 1 and column != self.size_x - 1 and self.grid[row + 1][column + 1].is_available():
            if self.grid[row + 1][column + 1].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row+1, column+1)] = self.grid[row+1][column+1].get_score(dijsktra) + self.get_avoidance_score(row+1, column+1)

        if row != 0 and column != self.size_x - 1 and self.grid[row - 1][column + 1].is_available():
            if self.grid[row - 1][column + 1].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row-1, column+1)] = self.grid[row-1][column+1].get_score(dijsktra) + self.get_avoidance_score(row-1, column+1)

        if row != self.size_y - 1 and column != 0 and self.grid[row + 1][column - 1].is_available():
            if self.grid[row + 1][column - 1].is_target():
                person.found_target(self.sim_time)
                return True
            neighbouring_cells[(row+1, column-1)] = self.grid[row+1][column-1].get_score(dijsktra) + self.get_avoidance_score(row+1, column-1)
        if len(neighbouring_cells) < 1:
            self.grid[row][column].set_state('P')
            return False
        min_row, min_column = min(neighbouring_cells, key=neighbouring_cells.get)
        self.grid[min_row][min_column].set_state('P')
        person.set_coordinate(min_row, min_column)
        return True

    def get_avoidance_score(self, row, column):
        score = 0
        if row != 0 :
            score += self.grid[row - 1][column].get_avoidance_cost()

        if column != 0:
            score += self.grid[row][column - 1].get_avoidance_cost()

        if row !=0 and column !=0 :
            score += self.grid[row - 1][column-1].get_avoidance_cost()

        if row != self.size_y - 1 :
            score += self.grid[row + 1][column].get_avoidance_cost()

        if column != self.size_x - 1 :
            score += self.grid[row][column+1].get_avoidance_cost()

        if row != self.size_y - 1 and column != self.size_x - 1 :
            score += self.grid[row+1][column+1].get_avoidance_cost()

        if row != 0 and column != self.size_x - 1 :
            score += self.grid[row-1][column+1].get_avoidance_cost()

        if row != self.size_y - 1 and column != 0:
            score += self.grid[row+1][column-1].get_avoidance_cost()
        return score

    def merge_dicts(d1, d2):
        return {} if any(d1[k] != d2[k] for k in d1.keys() & d2) else dict(d1, **d2)

    def find_distance_to_target(self, row, column):
        node_dist = self.grid[row][column].get_distance()
        neighbouring_cells = {}
        if row != 0:
            if node_dist + 1 < self.grid[row - 1][column].get_distance():
                self.grid[row - 1][column].set_distance(node_dist + 1)
            if not self.grid[row - 1][column].is_visited():
                neighbouring_cells[(row - 1, column)] = self.grid[row - 1][column].get_distance()

        if column != 0:
            if node_dist + 1 < self.grid[row][column - 1].get_distance():
                self.grid[row][column - 1].set_distance(node_dist + 1)
            if not self.grid[row][column - 1].is_visited():
                neighbouring_cells[(row, column - 1)] = self.grid[row][column - 1].get_distance()

        if row != 0 and column != 0:
            if node_dist + 1 < self.grid[row - 1][column -1].get_distance():
                self.grid[row - 1][column -1].set_distance(node_dist + math.sqrt(2))
            if not self.grid[row - 1][column - 1].is_visited():
                neighbouring_cells[(row - 1, column - 1)] = self.grid[row - 1][column - 1].get_distance()

        if row != self.size_y - 1:
            if node_dist + 1 < self.grid[row + 1][column].get_distance():
                self.grid[row + 1][column].set_distance(node_dist + 1)
            if not self.grid[row + 1][column].is_visited():
                neighbouring_cells[(row + 1, column)] = self.grid[row + 1][column].get_distance()

        if column != self.size_x - 1:
            if node_dist + 1 < self.grid[row][column + 1].get_distance():
                self.grid[row][column + 1].set_distance(node_dist + 1)
            if not self.grid[row][column + 1].is_visited():
                neighbouring_cells[(row, column + 1)] = self.grid[row][column + 1].get_distance()

        if row != self.size_y - 1 and column != self.size_x - 1:
            if node_dist + 1 < self.grid[row + 1][column + 1].get_distance():
                self.grid[row + 1][column + 1].set_distance(node_dist + math.sqrt(2))
            if not self.grid[row + 1][column + 1].is_visited():
                neighbouring_cells[(row + 1, column + 1)] = self.grid[row + 1][column + 1].get_distance()

        if row != 0 and column != self.size_x - 1:
            if node_dist + 1 < self.grid[row - 1][column + 1].get_distance():
                self.grid[row - 1][column + 1].set_distance(node_dist + math.sqrt(2))
            if not self.grid[row - 1][column + 1].is_visited():
                neighbouring_cells[(row - 1, column + 1)] = self.grid[row - 1][column + 1].get_distance()

        if row != self.size_y - 1 and column != 0:
            if node_dist + 1 < self.grid[row + 1][column - 1].get_distance():
                self.grid[row + 1][column - 1].set_distance(node_dist + math.sqrt(2))
            if not self.grid[row + 1][column - 1].is_visited():
                neighbouring_cells[(row + 1, column - 1)] = self.grid[row + 1][column - 1].get_distance()
        if len(neighbouring_cells) < 1:
            self.grid[row][column].visited_dijkstra = True
            return -1, -1

        self.grid[row][column].visited_dijkstra = True
        return min(neighbouring_cells, key=neighbouring_cells.get)



