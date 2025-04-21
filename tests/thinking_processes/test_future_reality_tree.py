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

from thinking_processes import FutureRealityTree

class TestCurrentRealityTree(unittest.TestCase):

    def test_create_illegal_conntection(self):
        frt = FutureRealityTree()
        
        engine_starts = frt.add_desirable_effect("Car's engine will start")
        build_fence = frt.add_injection("Build a fence between road and pool")
        cannot_roll_into_pool = frt.add_intermediate_effect('Car parked at the road cannot roll into the pool')

        self.assertRaises(ValueError, lambda: frt.add_causal_relation([cannot_roll_into_pool], build_fence))
        self.assertRaises(ValueError, lambda: frt.add_causal_relation([engine_starts], build_fence))

    def test_create_and_plot_tree(self):
        frt = FutureRealityTree()
        
        engine_starts = frt.add_desirable_effect("Car's engine will start")

        build_fence = frt.add_injection("Build a fence between road and pool")
        frt.add_negative_effect(build_fence, 'Car can roll into the fence')

        cannot_roll_into_pool = frt.add_intermediate_effect("Car parked at the road does not roll into the pool")
        no_water_in_fuel_line = frt.add_intermediate_effect("There is no water in the fuel line")
        fuel_to_the_engine = frt.add_intermediate_effect("Fuel is getting to the engine")

        frt.add_causal_relation([build_fence], cannot_roll_into_pool)
        frt.add_causal_relation([cannot_roll_into_pool], no_water_in_fuel_line)
        frt.add_causal_relation([no_water_in_fuel_line], fuel_to_the_engine)
        frt.add_causal_relation([fuel_to_the_engine], engine_starts)

        airintake = frt.add_intermediate_effect("Air intake is free of water")
        air_circulation = frt.add_intermediate_effect("Air is able to circulate")
        ac_working = frt.add_desirable_effect("Air conditioning is working")
        frt.add_causal_relation([cannot_roll_into_pool], airintake)
        frt.add_causal_relation([airintake], air_circulation)
        frt.add_causal_relation([air_circulation], ac_working)

        radio_sounds_good = frt.add_desirable_effect("Radio sounds good")
        speakers_not_underwater = frt.add_intermediate_effect("Speakers are not underwater")
        frt.add_causal_relation([cannot_roll_into_pool], speakers_not_underwater)
        frt.add_causal_relation([speakers_not_underwater], radio_sounds_good)

        with TemporaryDirectory() as tempdir:
            path_to_plot = os.path.join(tempdir, 'frt.png')
            frt.plot(view=False, filepath=path_to_plot)
            self.assertTrue(os.path.exists(path_to_plot))

if __name__ == '__main__':
    unittest.main()