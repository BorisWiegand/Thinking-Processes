'''
    This file is part of thinking-processes (More Info: https://github.com/BorisWiegand/thinking-processes).

    thinking-processes is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    thinking-processes is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with thinking-processes. If not, see <https://www.gnu.org/licenses/>.
'''
import os
from tempfile import TemporaryDirectory
import unittest

from thinking_processes import CurrentRealityTree

class TestCurrentRealityTree(unittest.TestCase):

    def test_create_and_plot_tree(self):
        crt = CurrentRealityTree()
        
        engine_not_start = crt.add_node("Car's engine will not start")
        engine_needs_fuel = crt.add_node('Engine needs fuel in order to run')
        no_fuel_to_engine = crt.add_node('Fuel is not getting to the engine')
        water_in_fuel_line = crt.add_node('There is water in the fuel line')
        crt.add_causal_relation([engine_needs_fuel, no_fuel_to_engine], engine_not_start)
        crt.add_causal_relation([water_in_fuel_line], no_fuel_to_engine)

        air_conditioning_not_working = crt.add_node('Air conditioning is not working')
        air_not_circulating = crt.add_node('Air is not able to circulate')
        air_intake_full_of_water = crt.add_node('The air intake is full of water')
        crt.add_causal_relation([air_not_circulating], air_conditioning_not_working)
        crt.add_causal_relation([air_intake_full_of_water], air_not_circulating)

        radio_distorted = crt.add_node('Radio sounds distorted')
        speakers_obstructed = crt.add_node('The speakers are obstructed')
        speakers_underwater = crt.add_node('The speakers are underwater')
        crt.add_causal_relation([speakers_obstructed], radio_distorted)
        crt.add_causal_relation([speakers_underwater], speakers_obstructed)

        car_in_pool = crt.add_node('The car is in the swimming pool')
        crt.add_causal_relation([car_in_pool], speakers_underwater)
        crt.add_causal_relation([car_in_pool], air_intake_full_of_water)
        crt.add_causal_relation([car_in_pool], water_in_fuel_line)

        handbreak_faulty = crt.add_node('The handbreak is faulty')
        handbreak_stops_car = crt.add_node('The handbreak stops the car from rolling into the swimming pool')
        crt.add_causal_relation([handbreak_faulty, handbreak_stops_car], car_in_pool)

        with TemporaryDirectory() as tempdir:
            path_to_plot = os.path.join(tempdir, 'crt.png')
            crt.plot(view=False, filepath=path_to_plot)
            self.assertTrue(os.path.exists(path_to_plot))

    def test_from_txt_file_empty(self):
        crt = CurrentRealityTree.from_txt_file('tests/resources/crt/empty.txt')
        self.assertEqual(crt.get_nr_of_nodes(), 0)
        self.assertEqual(crt.get_nr_of_causal_relations(), 0)

    def test_from_txt_file_two_nodes(self):
        crt = CurrentRealityTree.from_txt_file('tests/resources/crt/two_nodes.txt')
        self.assertEqual(crt.get_nr_of_nodes(), 2)
        self.assertEqual(crt.get_nr_of_causal_relations(), 0)

    def test_from_txt_file_node_id_collision(self):
        self.assertRaises(
            ValueError, 
            lambda: CurrentRealityTree.from_txt_file('tests/resources/crt/node_id_collision.txt')
        )

    def test_from_txt_file_wikipedia_example(self):
        crt = CurrentRealityTree.from_txt_file('tests/resources/crt/wikipedia_example.txt')
        self.assertEqual(crt.get_nr_of_nodes(), 13)
        self.assertEqual(crt.get_nr_of_causal_relations(), 10)

    def test_delete_node(self):
        crt = CurrentRealityTree.from_txt_file('tests/resources/crt/wikipedia_example.txt')
        self.assertEqual(crt.get_nr_of_nodes(), 13)
        self.assertEqual(crt.get_nr_of_causal_relations(), 10)
        crt.delete_node(crt.get_node_by_id(11))
        self.assertEqual(crt.get_nr_of_nodes(), 12)
        self.assertEqual(crt.get_nr_of_causal_relations(), 6)

    def test_save_as_drawio(self):
        crt = CurrentRealityTree.from_txt_file('tests/resources/crt/wikipedia_example.txt')
        with TemporaryDirectory() as tempdir:
            path_to_plot = os.path.join(tempdir, 'crt.xml')
            crt.save_as_drawio(path_to_plot)
            self.assertTrue(os.path.exists(path_to_plot))

if __name__ == '__main__':
    unittest.main()