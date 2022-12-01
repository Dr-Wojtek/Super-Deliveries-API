# Code by Alex Stråe, Sweden, AKA Dr-Wojtek @ GitHub

from flask import Flask, request
from flask_restful import Api, Resource
from flask_jsonpify import jsonify
from sqlalchemy import create_engine, text
from sorcery import dict_of
import operator, random, copy
from os import path
import os, sys, time
from supertech import *

engine = create_engine('sqlite:///db/SuperDeliveries.db', future=True)
app = Flask(__name__)
api = Api(app)

def by_distance(order):
    return order.get('distance')

def by_direction(order):
    return order.get('address').direction


logistics_office = thirty_seventh_and_fifth

class Orders(Resource):
    def get(self):
        all_delivery_orders = []
        with engine.connect() as conn:
            query = conn.execute(text("SELECT id, name, weight, value FROM orders"))
            for id, name, weight, value in query:
                all_delivery_orders.append(
                {'id': id, 'name': name, 'weight': int(weight), 'value': int(value)})
        todays_locations = list(city_graph.keys())
        todays_locations.remove(logistics_office)
        for order in all_delivery_orders:
            dice = random.randint(0, len(todays_locations) - 1)
            order['address'] = todays_locations.pop(dice)
        orders_destinations = copy.deepcopy(all_delivery_orders)
        for order in orders_destinations:
            order['address'] = str(order['address'])

        return jsonify(orders_destinations)

    def post(self):
        new_orders = request.get_json()
        with engine.connect() as conn:
            for order in new_orders:
                conn.execute(text("INSERT INTO orders (id, name, weight, value) VALUES ("+ str(order.get("id")) + ", '"+ order.get("name") + "', " \
                              + str(order.get("weight")) + ", " + str(order.get("value")) +");"))
            conn.commit()
        return new_orders

    def put(self):
        updated_order = request.get_json()
        with engine.connect() as conn:
            query = conn.execute(text("SELECT id FROM orders WHERE id = " + str(updated_order[0].get("id")) + ";"))
            for id in query:
                with engine.connect() as conn:
                    for order in updated_order:
                        conn.execute(text("UPDATE orders SET name = '" + order.get("name") + "', weight = " + str(order.get("weight")) + \
                                            ", value = " + str(order.get("value")) + " WHERE id = " + str(order.get("id")) + ";"))
                    conn.commit()
                    return updated_order
            return updated_order, 403

    def delete(self, id):
        with engine.connect() as conn:
            conn.execute(text("DELETE FROM orders WHERE id=" + str(id) + ""))
            conn.commit()
        return

class Addresses(Resource):
    def get(self):
        with engine.connect() as conn:
            query = conn.execute(text("SELECT id, name, coordinate_x, coordinate_y FROM addresses"))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return jsonify(result)

class LimitingFactor(Resource):
    def post(self, limiting_factor=0):
        all_delivery_orders = request.get_json()
        chosen_delivery_orders = []
        if limiting_factor != 0:
            items_to_deliver = Supertech.dynamic_knapsack(all_delivery_orders, 'weight', int(limiting_factor))
            for order in all_delivery_orders:
                if order['name'] in items_to_deliver:
                    chosen_delivery_orders.append(order)
        else:
            chosen_delivery_orders = all_delivery_orders.copy()

        return jsonify(chosen_delivery_orders)

class CreateResults(Resource):
    def post(self):
        chosen_delivery_orders = request.get_json()
        new_trip = Supertech(logistics_office, city_graph)
        for order in chosen_delivery_orders:
            order['address'] = eval(order['address'])
        distance_by_foot = 0
        distance_by_shortest = 0
        distance_by_direction = 0
        distance_by_super = 0
        final_path = []
        #This calculates distance for every order from the office and sorts ASC. Needed for the next method below.
        for order in chosen_delivery_orders:
            target, distance, path = new_trip.a_star(new_trip.map, logistics_office, order.get('address'))
            order['distance'] = distance
            distance_by_foot += distance * 2
            order['path'] = path
        chosen_delivery_orders.sort(key=by_distance)
        chosen_delivery_orders.append({'name': 'Return to Base', 'weight': 0, 'value': 0, 'address': logistics_office,
                                       'distance': chosen_delivery_orders[-1].get('distance'), 'path': []})

        # This calculates route after shortest distance from office.
        # Often yields the weakest result. Uses A* once per order to calculate distance.
        starting_location = new_trip.start
        for order in chosen_delivery_orders:
            target, distance, path = new_trip.a_star(new_trip.map, starting_location, order.get('address'))
            starting_location = order.get('address')
            distance_by_shortest += distance

        # This calculates route after direction.
        # Often yields better result than by shortest distance from office; sometimes even the best. A* not needed.
        chosen_delivery_orders.pop(-1)
        optimized_route = chosen_delivery_orders.copy()
        optimized_route.sort(key=by_direction)
        optimized_route.append({'name': 'Return to Base', 'weight': 0, 'value': 0, 'address': logistics_office,
                                'distance': chosen_delivery_orders[-1].get('distance'), 'path': []})
        starting_location = new_trip.start
        for order in optimized_route:
            target, distance, path = new_trip.a_star(new_trip.map, starting_location, order.get('address'))
            starting_location = order.get('address')
            distance_by_direction += distance

        # This calculates route with Super Deliveries logic and A*, getting the closest next drop-off,
        # as long as it is in the same direction from the office.
        optimized_route.pop(-1)
        super_optimized_route = []
        # Getting all empty directions, if any:
        number_per_direction = {'N)': 0, 'NE': 0, 'E)': 0, 'SE': 0, 'S)': 0, 'SW': 0, 'W)': 0, 'NW': 0}
        for order in optimized_route:
            for direction in number_per_direction:
                if direction == order['address'].direction[3:5]:
                    number_per_direction[direction] += 1
                    break
        # Sorting clockwise, starting with first direction after empty directions(s).
        # If no empty directions it starts with direction with the least deliveries:
        directions_asc = sorted(number_per_direction.items(), key=operator.itemgetter(1))
        first_direction = directions_asc[0][0]
        compass = ['N)', 'NE', 'E)', 'SE', 'S)', 'SW', 'W)', 'NW']
        index = compass.index(first_direction)
        if optimized_route[0]['address'] == logistics_office:
            super_optimized_route.append(optimized_route.pop(0))
        for i in range(index, len(compass)):
            for delivery_order in optimized_route:
                if delivery_order['address'].direction[3:5] == compass[i]:
                    super_optimized_route.append(delivery_order)
        for i in range(0, index):
            for delivery_order in optimized_route:
                if delivery_order['address'].direction[3:5] == compass[i]:
                    super_optimized_route.append(delivery_order)

        # Time for A* to optimize within direction and then to closest in next direction.
        # Uncomment print statements for verbose A* sorting.
        for i in range(len(super_optimized_route) - 1):
            if super_optimized_route[i]['address'] == logistics_office:
                continue
            current_dir = super_optimized_route[i]['address'].direction[3:5]
            if super_optimized_route[i + 1]['address'].direction[3:5] == current_dir:
                current_distance_next = new_trip.a_star(new_trip.map, super_optimized_route[i]['address'],
                                                        super_optimized_route[i + 1]['address'])[1]
                current_next_address = super_optimized_route[i + 1]
                grab = None
                for delivery_order in super_optimized_route:
                    if delivery_order['address'].direction[3:5] == current_dir:
                        already_delivered_order = None
                        if i > 0:
                            already_delivered_order = super_optimized_route[i - 1]
                        if delivery_order != super_optimized_route[
                            i] and delivery_order != already_delivered_order and delivery_order != current_next_address:
                            other_target_distance = new_trip.a_star(new_trip.map, super_optimized_route[i]['address'],
                                                                    delivery_order['address'])[1]
                            if other_target_distance < current_distance_next:
                                current_distance_next = other_target_distance
                                grab = delivery_order
                if grab:
                    # print("FOUND CLOSER TARGET WITHIN DIRECTION")
                    # print("PUTTING " + grab['name'] + " AFTER " + super_optimized_route[i]['name'] )
                    super_optimized_route.remove(grab)
                    super_optimized_route.insert(i + 1, grab)

            elif super_optimized_route[i]['address'].direction[3:5] != super_optimized_route[i + 1][
                                                                           'address'].direction[3:5]:
                next_dir = super_optimized_route[i + 1]['address'].direction[3:5]
                current_distance_next = new_trip.a_star(new_trip.map, super_optimized_route[i]['address'],
                                                        super_optimized_route[i + 1]['address'])[1]
                grab = None
                for delivery_order in super_optimized_route:
                    if delivery_order['address'].direction[3:5] == next_dir:
                        other_target_distance = \
                        new_trip.a_star(new_trip.map, super_optimized_route[i]['address'], delivery_order['address'])[1]
                        if other_target_distance < current_distance_next:
                            current_distance_next = other_target_distance
                            grab = delivery_order
                if grab:
                    # print("FOUND CLOSER TARGET FOR NEXT DIRECTION")
                    # print("PUTTING " + grab['name'] + " AFTER " + super_optimized_route[i]['name'])
                    super_optimized_route.remove(grab)
                    super_optimized_route.insert(i + 1, grab)

        # Optimizing finished. Calculating final distance.
        super_optimized_route.append({'name': 'Return to Base', 'weight': 0, 'value': 0, 'address': logistics_office,
                                      'distance': super_optimized_route[-1].get('distance'), 'path': []})
        starting_location = new_trip.start
        for order in super_optimized_route:
            target, distance, path = new_trip.a_star(new_trip.map, starting_location, order.get('address'))
            for address in path:
                final_path.append(address)
            starting_location = order.get('address')
            distance_by_super += distance

        # Update database with latest result before returning all results:
        program_runs = 0
        counter_super_best = 0
        with engine.connect() as conn:
            conn.execute(text("UPDATE history SET program_runs = program_runs + 1"))
            conn.commit()
        if distance_by_super <= distance_by_direction and distance_by_super <= distance_by_shortest:
            with engine.connect() as conn:
                conn.execute(text("UPDATE history SET super_best_counter = super_best_counter + 1"))
                conn.commit()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT program_runs FROM history"))
            for row in result:
                program_runs = row[0]
            result = conn.execute(text("SELECT super_best_counter FROM history"))
            for row in result:
                counter_super_best = row[0]

        results = dict_of(distance_by_foot, distance_by_shortest, distance_by_direction, distance_by_super, final_path, program_runs, counter_super_best)
        results['logistics_office'] = logistics_office.name
        return jsonify(results)

api.add_resource(Orders, '/orders', '/orders/<id>')
api.add_resource(Addresses, '/addresses')
api.add_resource(LimitingFactor, '/limitingFactor/<limiting_factor>')
api.add_resource(CreateResults, '/createResults')

if __name__ == '__main__':
    app.run(port='5002')
