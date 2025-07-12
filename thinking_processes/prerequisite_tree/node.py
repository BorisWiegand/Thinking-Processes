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

from graphviz import Digraph


class Obstacle:
    """ 
    node of a prerequisite tree, which represents an obstacle to a goal or solution
    """

    def __init__(self, id: str, obstacle: str):
        self.__id = id
        self.__obstacle = obstacle
        self.__solutions: list[Solution] = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def text(self) -> str:
        return self.__obstacle
    
    def add_solution(self, solution: str) -> 'Solution':
        child_node = Solution(f'{self.__id}.{len(self.__solutions)}', solution)
        self.__solutions.append(child_node)
        return child_node
    
    def get_total_nr_of_sub_obstacles(self) -> int:
        return sum(
            solution.get_total_nr_of_obstacles()
            for solution in self.__solutions
        )
    
    def add_to_graphviz_graph(self, graph: Digraph, parent_node_id: str):
        graph.node(self.id, self.text, fillcolor='red', style='filled', shape='hexagon')
        graph.edge(self.id, parent_node_id)
        for solution in self.__solutions:
            solution.add_to_graphviz_graph(graph, self.id)
    
class Solution:
    """ 
    node of a prerequisite tree, which represent a solution to an obstacle
    """

    def __init__(self, id: str, solution: str):
        self.__id = id
        self.__solution = solution
        self.__obstacles: list[Obstacle] = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def text(self) -> str:
        return self.__solution
    
    def add_obstacle(self, obstacle: str) -> Obstacle:
        child_node = Obstacle(f'{self.__id}.{len(self.__obstacles)}', obstacle)
        self.__obstacles.append(child_node)
        return child_node
    
    def get_total_nr_of_obstacles(self) -> int:
        return len(self.__obstacles) + sum(
            obstacle.get_total_nr_of_sub_obstacles()
            for obstacle in self.__obstacles
        )
    
    def add_to_graphviz_graph(self, graph: Digraph, parent_node_id: str):
        graph.node(self.id, self.text, style='rounded', shape='rect')
        graph.edge(self.id, parent_node_id)
        for obstacle in self.__obstacles:
            obstacle.add_to_graphviz_graph(graph, self.id)

