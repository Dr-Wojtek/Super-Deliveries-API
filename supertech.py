# Code by Alex Stråe, Sweden, AKA Dr-Wojtek @ GitHub

from math import inf
from heapq import heappop, heappush
from sqlalchemy import create_engine, text
from os import path

engine = create_engine('sqlite:///db/SuperDeliveries.db', future=True)


class GraphVertex:
    def __init__(self, name, x, y, id):
        self.name = name
        self.pos = (x, y)
        self.direction = ""
        self.visit_number = []
        self.id = id
    # heappush needs to know which object is smaller according to heap rules.
    # locations have no specified size, therefore implement less-than method which says, current location is smaller to whichever compared location:
    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return str(self.id)

# Loading addresses and creating map graph
city_graph = {}
with engine.connect() as conn:
    all_addresses = conn.execute(text("SELECT id, name, coordinate_x, coordinate_y FROM addresses"))
    for id, name, x, y in all_addresses:
        globals()[id] = GraphVertex(name, int(x), int(y), id)
        city_graph.update({globals()[id] : None})

for key in city_graph:
    with engine.connect() as conn:
        all_neighbors = conn.execute(text("SELECT adj1, adj1_distance, adj2, adj2_distance, adj3, adj3_distance, adj4, adj4_distance FROM addresses WHERE id = '" + key.id + "'"))
        for adj1, adj1_distance, adj2, adj2_distance, adj3, adj3_distance, adj4, adj4_distance in all_neighbors:
            if adj4 != "":
                city_graph.update({key: {(eval(adj1), adj1_distance), (eval(adj2), adj2_distance),
                                         (eval(adj3), adj3_distance), (eval(adj4), adj4_distance)}})
            elif adj3 != "":
                city_graph.update({key: {(eval(adj1), adj1_distance), (eval(adj2), adj2_distance),
                                         (eval(adj3), adj3_distance)}})
            elif adj2 != "":
                city_graph.update({key: {(eval(adj1), adj1_distance), (eval(adj2), adj2_distance)}})

            else:
                city_graph.update({key: {(eval(adj1), adj1_distance)}})

class Supertech:
    def __init__(self, start_pos, map):
        self.start = start_pos
        self.map = map
        for address in map:
            self.sort_direction(self.start, address)

    def sort_direction(self, start, address):
        if address == start:
            address.direction = 'A (N)'
        elif address.pos[0] > start.pos[0]:
            if abs(address.pos[0] - start.pos[0]) >= 2:
                if address.pos[1] < start.pos[1]:
                    address.direction = 'B (NE)'
                elif address.pos[1] == start.pos[1]:
                    address.direction = 'C (E)'
                elif abs(address.pos[1] - start.pos[1]) == 1:
                    address.direction = 'C (E)'
                elif abs(address.pos[1] - start.pos[1]) == 2:
                    address.direction = 'D (SE)'
            elif abs(address.pos[0] - start.pos[0]) >= 1:
                if address.pos[1] < start.pos[1]:
                    address.direction = 'A (N)'
                elif address.pos[1] == start.pos[1]:
                    address.direction = 'C (E)'
                else:
                    address.direction = 'E (S)'
            else:
                if address.pos[1] > start.pos[1]:
                    address.direction = 'E (S)'
                else:
                    address.direction = 'A (N)'
        else:
            if abs(address.pos[0] - start.pos[0]) >= 2:
                if address.pos[1] < start.pos[1]:
                    address.direction = 'H (NW)'
                elif address.pos[1] == start.pos[1]:
                    address.direction = 'G (W)'
                else:
                    if abs(address.pos[1] - start.pos[1]) == 1:
                        address.direction = 'G (W)'
                    else:
                        address.direction = 'F (SW)'
            else:
                if address.pos[1] > start.pos[1]:
                    address.direction = 'E (S)'
                elif address.pos[1] == start.pos[1]:
                    address.direction = 'G (W)'
                else:
                    address.direction = 'A (N)'

    # implementation of 'The Knapsack Problem' using dynamic programming and mods to fit list of order dicts
    def dynamic_knapsack(ado, limiting_factor, limiting_factor_cap):
        rows = len(ado) + 1
        cols = limiting_factor_cap + 1
        # setup 2d-array to withhold orders. Rows are for orders.
        # Columns are for the limiting factor, most likely weight. One column for each total unit of limiting factor.
        matrix = [[] for i in range(rows)]
        for i in range(rows):
            matrix[i] = [-1 for j in range(cols)]
            # populate columns for each order. First row and column are filled of 0, since in the
            # first round of each item, we have to have something to compare to.
            for j in range(cols):
                if i == 0 or j == 0:
                    matrix[i][j] = []
                    matrix[i][j].append(0)
                # If current order is within our limiting factor requirement, we might want to include it:
                elif ado[i-1][limiting_factor] <= j:
                    include_order = []
                    exclude_order = []
                    # the core of the algo: Get current order's value and add to it value from earlier most valuable config
                    # that won't make us exceed our limiting factor.
                    # matrix[i-1][j-ado[i-1][limiting_factor]][0] = last row, at column with config with factor = (factor cap - this objects factor)
                    include_order.append(ado[i-1]['value'] + matrix[i-1][j-ado[i-1][limiting_factor]][0])
                    # and get the name so we know where the value comes from! Useless algo if we don't do this.
                    include_order.append(ado[i-1]['name'])
                    # above grabbed the name from current order, but we also need the names from the last most valuable
                    # config if it turns out this is the new most valuable config.
                    if len(matrix[i-1][j-ado[i-1][limiting_factor]]) > 1:
                        for x in range(1, len(matrix[i-1][j-ado[i-1][limiting_factor]])):
                            include_order.append(matrix[i-1][j-ado[i-1][limiting_factor]][x])
                    # and now we look if we already found a combination with this limiting factor worth more:
                    for orders in matrix[i-1][j]:
                        exclude_order.append(orders)
                    matrix[i][j] = []
                    # Which was more valuable, this new combination or the last?:
                    if include_order[0] > exclude_order[0]:
                        for order in include_order:
                            matrix[i][j].append(order)
                    else:
                        for order in exclude_order:
                            matrix[i][j].append(order)
                # And if the object is too heavy, it cannot be included, so we skip it
                # by copying last row's most valuable config.
                else:
                    matrix[i][j] = []
                    for order in matrix[i-1][j]:
                        matrix[i][j].append(order)
        return matrix[rows-1][limiting_factor_cap]

    # for A *: calculate difference between coordinates and therefor distance between current loc (c) and target (t)
    def heuristic(self, c, t):
        x_dist = abs(c.pos[0] - t.pos[0])
        y_dist = abs(c.pos[0] - t.pos[0])
        return x_dist + y_dist

    # A* search algorithm. s = starting location. t = target location
    def a_star(self, map, s, t):
        paths_and_distances = {}
        # add all addresses in map to dict, with corresponding distance to start loc (which is unknown, therefor inf)
        for address in map:
            paths_and_distances[address] = [inf, [s.name]]
        # distance to start, from start, is zero.
        paths_and_distances[s][0] = 0
        # create heap for calculation, starting with start location
        addresses_to_calculate = [(0, s)]
        while addresses_to_calculate and paths_and_distances[t][0] is inf:
            # get current location, and current distance to calculate
            c_distance, c_loc = heappop(addresses_to_calculate)
            # get distance to adjacent location (adj)
            for adj, extra_distance in map[c_loc]:
                # and add to it the dist to target, so we know whether we are moving in the right direction
                new_distance = c_distance + extra_distance + self.heuristic(adj, t)
                # This might be part of the final path. We need to know how we got here.
                new_path = paths_and_distances[c_loc][1] + [c_loc.name]
                # If this is the shorter way to target from start loc, update current known distance and path
                if new_distance < paths_and_distances[adj][0]:
                    paths_and_distances[adj][0] = new_distance
                    paths_and_distances[adj][1] = new_path
                    # push new location and distance there onto heap
                    heappush(addresses_to_calculate, (c_distance + extra_distance, adj))

        return t.name, paths_and_distances[t][0], paths_and_distances[t][1]
