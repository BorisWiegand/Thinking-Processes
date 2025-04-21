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

from thinking_processes import PrerequisiteTree

class TestPrerequisiteTree(unittest.TestCase):

    def test_create_and_plot_tree(self):
        prt = PrerequisiteTree(objective='Repair the handbrake')
        
        missing_knowledge = prt.add_obstacle('Cannot repair the handbrake')

        learn = missing_knowledge.add_solution('Learn to repair the handbrake')
        learn.add_obstacle('No time to learn')

        let_repair = missing_knowledge.add_solution('Let someone else repair the handbrake')
        no_money = let_repair.add_obstacle('No money to let repair the handbrake')
        no_money.add_solution('Save money')

        with TemporaryDirectory() as tempdir:
            path_to_plot = os.path.join(tempdir, 'ec.png')
            prt.plot(view=False, filepath=path_to_plot)
            self.assertTrue(os.path.exists(path_to_plot))

if __name__ == '__main__':
    unittest.main()