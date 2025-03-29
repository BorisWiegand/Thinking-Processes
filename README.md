# Thinking Processes

This Python package helps you to draw diagrams used in the Thinking Processes from the Theory of Constraints. 
For more information, see https://en.wikipedia.org/wiki/Thinking_processes_(theory_of_constraints) 

### Prerequisites

Python 3.11+

### Installing

```bash
pip install thinking-processes
```

### Current Reality Tree

In this example, we find root causes for undesired effects by drawing a Current Reality Tree:

```python
from thinking_processes import CurrentRealityTree

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

crt.plot(view=True, filepath='crt.png')
```

The resulting tree looks like this:

![Current Reality Tree](crt.png)

## Development

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Running the tests

All tests in the "tests" directory are based on the unittest package.

### Deployment

```bash
make rm -R dist build thinking-processes.egg-info || python -m build && twine upload --skip-existing --verbose dist/*
```

You should also create a tag for the current version

```bash
git tag -a [version] -m "describe what has changed"
git push --tags
```

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

If you have any questions, feel free to ask one of our authors:

* **Boris Wiegand** - boris.wiegand@stahl-holding-saar.de