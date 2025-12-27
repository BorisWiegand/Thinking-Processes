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
from typing import override
from graphviz import Digraph, Graph

from thinking_processes.prerequisite_tree.node import Obstacle, Solution
from thinking_processes.diagram import Diagram

class PrerequisiteTree(Diagram):
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
    
    def get_total_nr_of_obstacles(self) -> int:
        return len(self.__obstacles) + sum(
            obstacle.get_total_nr_of_sub_obstacles()
            for obstacle in self.__obstacles
        )
    
    @override
    def to_graphviz(self) -> Graph:
        graph = Digraph(graph_attr=dict(rankdir="BT"))
        graph.node('objective', self.__objective, fillcolor='green', style='filled,rounded')
        for obstacle in self.__obstacles:
            obstacle.add_to_graphviz_graph(graph, 'objective')
        return graph

    @staticmethod
    def from_txt_file(path_to_txt: str) -> 'PrerequisiteTree':
        """
        creates a PrerequisiteTree from a .txt file. 
        See PrerequisiteTree.from_string for the expected file content.

        Args:
            path_to_txt (str): e.g. 'a_folder/prt.txt'

        Returns:
            PrerequisiteTree: 
            a PrerequisiteTree with nodes defined in the file content.
        """
        with open(path_to_txt, 'r') as f:
            return PrerequisiteTree.from_string(f.read())
        
    @staticmethod
    def from_string(s: str) -> 'PrerequisiteTree':
        """
        parses a new PrerequisiteTree from a string.

        Example:
            | Repair the handbreak
            | Cannot repair the handbreak
            |   Learn to repair the handbreak
            |       No time to learn
            |   Let someone repair the handbreak
            |       No money
            |           Save money

        Args:
            s (str): see above for the format

        Raises:
            ValueError: if there is an error in the format that prevents creating the tree

        Returns:
            CurrentRealityTree: if the format is correct
        """
        lines = [l for l in s.splitlines() if l.strip()]
        if not lines:
            raise ValueError('the tree must at least contain an objective')
        prt = PrerequisiteTree(lines[0])
        def indentation(line: str) -> int:
            for i, c in enumerate(line):
                if c not in (' ', '\t'):
                    return i
            return 0
        def parse_obstacles(current_node: PrerequisiteTree|Solution, i: int, current_indentation: int):
            if len(lines) > i + 1:
                direct_child_indentation = indentation(lines[i+1])
                if direct_child_indentation > current_indentation:
                    obstacle = current_node.add_obstacle(lines[i+1].strip())
                    parse_solutions(obstacle, i+1, direct_child_indentation)
                    for j, successor_line in enumerate(lines[i+2:]):
                        if indentation(successor_line) == direct_child_indentation:
                            obstacle = current_node.add_obstacle(successor_line.strip())
                            parse_solutions(obstacle, i+j+2, direct_child_indentation)
                        elif indentation(successor_line) < direct_child_indentation:
                            break
        def parse_solutions(current_node: Obstacle, i: int, current_indentation: int):
            if len(lines) > i + 1:
                direct_child_indentation = indentation(lines[i+1])
                if direct_child_indentation > current_indentation:
                    solution = current_node.add_solution(lines[i+1].strip())
                    parse_obstacles(solution, i+1, direct_child_indentation)
                    for j, successor_line in enumerate(lines[i+2:]):
                        if indentation(successor_line) == direct_child_indentation:
                            solution = current_node.add_solution(successor_line.strip())
                            parse_obstacles(solution, i+j+2, direct_child_indentation)
                        elif indentation(successor_line) < direct_child_indentation:
                            break
        parse_obstacles(prt, 0, 0)
        return prt