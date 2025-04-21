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
from graphviz import Digraph

from thinking_processes.prerequisite_tree.node import Obstacle

class PrerequisiteTree:
    """
    you can use a prerequisite to analyze how to overcome obstacles in order to achieve a desirable effect or goal.
    """

    def __init__(self, objective: str):
        """
        creates a new prerequisite tree with the given objective
        """
        self.__objective = objective
        self.__obstacles: list[Obstacle] = []

    def add_obstacle(self, obstacle: str) -> Obstacle:
        """
        adds a new obstacle node that is directly linked to the root node (=objective) of this tree. 

        Args:
            obstacle (str): text of this obstacle node

        Returns:
            Obstacle: an obstacle node. can be used to add solutions to this tree
        """
        node = Obstacle(str(len(self.__obstacles)), obstacle)
        self.__obstacles.append(node)
        return node
    
    def plot(self, view: bool = True, filepath: str|None = None):
        """
        plots this prerequisite tree.

        Args:
            view (bool, optional): set to False if you do not want to immediately view the diagram. Defaults to True.
            filepath (str | None, optional): path to the file in which you want to save the plot. Defaults to None.
        """
        graph = Digraph(graph_attr=dict(rankdir="BT"))
        graph.node('objective', self.__objective, fillcolor='green', style='filled,rounded')
        for obstacle in self.__obstacles:
            obstacle.add_to_graphviz_graph(graph, 'objective')

        #we do not want to see the generated .dot code 
        # => write it to a temporary file
        with TemporaryDirectory(delete=filepath is not None) as tempdir:
            graph.render(filename=os.path.join(tempdir, 'prt.gv'), view=view, outfile=filepath)