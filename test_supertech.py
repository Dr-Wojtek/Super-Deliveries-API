import unittest
import supertech

# Unit tests for methods
class SupertechTest(unittest.TestCase):

    # Test dynamic knapsack's ability to:
    # 1) calculate that value of order #3 is higher than #1 + #2 together
    # 2) Only return order #3
    # 3) Store the name of the order(s)
    def test_dynamic_knapsack(self):
        all_delivery_orders = [
    {
        "id": 1,
        "name": "Ravenclaws Diadem",
        "value": 11560,
        "weight": 4
    },
    {
        "id": 2,
        "name": "The Ocarina of Time",
        "value": 7500,
        "weight": 2
    },
    {
        "id": 3,
        "name": "Anduril (flame of the west)",
        "value": 20000,
        "weight": 6
    }
        ]
        delivery_orders = supertech.Supertech.dynamic_knapsack(all_delivery_orders, 'weight', 6)
        # print(str(delivery_orders))
        self.assertEqual("Anduril (flame of the west)", delivery_orders[1])

    def test_database_engine(self):
        new_trip = supertech.Supertech(supertech.thirty_seventh_and_fifth, supertech.city_graph)
        self.assertIsNotNone(new_trip)

    # Test a_stars ability to:
    # 1) Produce concurrent results
    # 2) Finds the shortest path (I know the shortest route to specified location is 7)
    def test_a_star(self):
        new_trip = supertech.Supertech(supertech.thirty_seventh_and_fifth, supertech.city_graph)
        target, distance, path = new_trip.a_star(new_trip.map, supertech.thirty_seventh_and_fifth, supertech.thirty_third_and_madison)
        target, distance2, path2 = new_trip.a_star(new_trip.map, supertech.thirty_seventh_and_fifth,
                                                 supertech.thirty_third_and_madison)
        # print(str(target) + str(distance) + str(path)
        self.assertEqual(distance, 7)
        self.assertEqual(distance, distance2)
        self.assertEqual(path, path2)

if __name__ == '__main__':
    unittest.main()