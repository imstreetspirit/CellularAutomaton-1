import math

R_MAX = 0.5
R_MAX_SQUARED = R_MAX ** 2

class SimCell(object):

    def __init__(self, x, y):
        self.state = 'E'
        self.next_state = 'E'
        self.x = x
        self.y = y
        self.utility_score = 0
        self.distance = math.inf
        self.visited_dijkstra = False


    def set_state(self, state):
        self.next_state = state
        if state == 'T':
            self.distance = 0
            self.visited_dijkstra = True
        if state == 'O':
            self.state = 'O'
            self.next_state = 'O'
            self.utility_score = math.inf
            self.visited_dijkstra = True

    def is_available(self):
        if self.next_state == 'E' or self.state == 'T' or self.next_state == 'T':
            if self.next_state != 'P':
                return True
        else:
            return False

    def set_next_state(self):
        self.state = self.next_state

    def update_utility_score(self, target):
        self.utility_score = math.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)

    def set_utility_score(self, score):
        self.utility_score = score

    def get_score(self, dijsktra=False):
        if dijsktra:
            if self.state == 'P' or self.state == 'O':
                return math.inf
            else:
                return self.distance
        else:
            if self.state == 'P' or self.state == 'O':
                return math.inf
            else:
                return self.utility_score

    def get_avoidance_cost(self):
        if self.state == 'P':
            return math.exp(1 / (-1 * R_MAX_SQUARED))
        else:
            return 0

    def is_target(self):
        if self.state == 'T':
            return True
        else:
            return False

    def set_distance(self, dist):
        if self.state == 'O':
            pass
        else:
            self.distance = dist

    def get_distance(self):
        return self.distance

    def is_not_obstacle(self):
        if self.state == 'O':
            return False
        else:
            return True

    def is_person(self):
        if self.state == 'P':
            return True
        else:
            return False

    def is_visited(self):
        return self.visited_dijkstra
