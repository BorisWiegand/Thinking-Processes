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

from thinking_processes import EvaporatingCloud

class TestCurrentRealityTree(unittest.TestCase):

    def setUp(self):
        self.ec = EvaporatingCloud(
            objective='Reduce cost per unit',
            need_a='Reduce setup cost per unit',
            need_b='Reduce carrying cost per unit',
            conflict_part_a='Run larger batches',
            conflict_part_b='Run smaller batches'
        )
        self.ec.add_assumption_on_the_conflict('small is the opposite of large', is_true=True)
        self.ec.add_assumption_on_the_conflict('there is only one meaning to the word "batch"', is_true=False)
        self.ec.add_assumption_on_need_a("setup cost is fixed and can't be reduced")
        self.ec.add_assumption_on_need_a("the machine being set up is a bottleneck with no spare capacity")
        self.ec.add_assumption_on_need_b("smaller batches reduce carrying cost")

    def test_plot_evaporating_cloud(self):
        with TemporaryDirectory() as tempdir:
            path_to_plot = os.path.join(tempdir, 'ec.png')
            self.ec.plot(view=False, filepath=path_to_plot)
            self.assertTrue(os.path.exists(path_to_plot))

    def test_to_and_from_string(self):
        recovered_ec = EvaporatingCloud.from_string(self.ec.to_string())
        self.assertEqual(self.ec, recovered_ec)

    def test_remove_assumption(self):
        self.assertEqual(5, self.ec.get_total_nr_of_assumptions())
        self.ec.remove_assumption('smaller batches reduce carrying cost')
        self.assertEqual(4, self.ec.get_total_nr_of_assumptions())
        self.ec.remove_assumption('smaller batches reduce carrying cost')
        self.assertEqual(4, self.ec.get_total_nr_of_assumptions())

if __name__ == '__main__':
    unittest.main()