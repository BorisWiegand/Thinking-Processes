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

from typing import override
from graphviz import Digraph, Graph

from thinking_processes.diagram import Diagram

class EvaporatingCloud(Diagram):
    """
    an evaporating cloud, also known as conflict resolution diagram

    https://en.wikipedia.org/wiki/Evaporating_cloud 
    """

    def __init__(
            self, objective: str = '?',
            need_a: str = '?', need_b: str = '?',
            conflict_part_a: str = '?', conflict_part_b: str = '?'):
        self.__objective = objective
        self.__need_a = need_a
        self.__need_b = need_b
        self.__conflict_part_a = conflict_part_a
        self.__conflict_part_b = conflict_part_b
        self.__assumptions_between_conflict_parts: list[tuple[str,bool|None]] = []
        self.__assumptions_on_need_a: list[tuple[str,bool|None]] = []
        self.__assumptions_on_need_b: list[tuple[str,bool|None]] = []

    def add_assumption_on_the_conflict(self, text: str, is_true: bool|None = None):
        self.__assumptions_between_conflict_parts.append((text, is_true))

    def add_assumption_on_need_a(self, text: str, is_true: bool|None = None):
        self.__assumptions_on_need_a.append((text, is_true))

    def add_assumption_on_need_b(self, text: str, is_true: bool|None = None):
        self.__assumptions_on_need_b.append((text, is_true))

    @override
    def to_graphviz(self) -> Graph:
        graph = Digraph(graph_attr=dict(rankdir="RL", nodesep='0.5'))
        graph.node(
            'objective', self.__objective, 
            fillcolor='lightgreen', shape='rect', style='rounded,filled',
        )
        with graph.subgraph(graph_attr=dict(concentrate='true', rank='same')) as subgraph:
            for i,(assumption, is_true) in enumerate(self.__assumptions_on_need_b):
                self.__add_assumption_node(
                    subgraph, 
                    f'assumption_b_{i}', assumption, is_true,
                    'need_b', None
                )
        with graph.subgraph(graph_attr=dict(rank="same")) as subgraph:
            subgraph.node(
                'need_a', self.__need_a, 
                fillcolor='lightblue', shape='rect', style='rounded,filled',
            )
            subgraph.node(
                'need_b', self.__need_b, 
                fillcolor='lightblue', shape='rect', style='rounded,filled',
            )
        graph.edge('need_a', 'objective')
        graph.edge('need_b', 'objective')
        with graph.subgraph(graph_attr=dict(concentrate='true', rank='same')) as subgraph:
            for i,(assumption, is_true) in enumerate(self.__assumptions_on_need_a):
                self.__add_assumption_node(
                    subgraph, 
                    f'assumption_a_{i}', assumption, is_true,
                    'need_a', None
                )
        with graph.subgraph(graph_attr=dict(rank="same")) as subgraph:
            subgraph.node(
                'conflict_part_a', self.__conflict_part_a, 
                fillcolor='darkorange', shape='rect', style='rounded,filled',
            )
            subgraph.node(
                'conflict_part_b', self.__conflict_part_b, 
                fillcolor='darkorange', shape='rect', style='rounded,filled',
            )
            subgraph.edge('conflict_part_a', 'conflict_part_b', dir='both')
        graph.edge('conflict_part_a', 'need_a')
        graph.edge('conflict_part_b', 'need_b')
        with graph.subgraph(graph_attr=dict(concentrate='true')) as subgraph:
            for i,(assumption, is_true) in enumerate(self.__assumptions_between_conflict_parts):
                self.__add_assumption_node(
                    subgraph, 
                    f'assumption_c_{i}', assumption, is_true,
                    'conflict_part_a', 'conflict_part_b'
                )
        return graph

    def __add_assumption_node(
            self, graph: Digraph, node_id: str, 
            assumption: str, is_true: bool|None,
            target_a: str, target_b: str|None):
        if is_true is None:
            color = 'gray'
        elif is_true:
            color = 'green'
        else:
            color = 'red'
        graph.node(node_id, assumption, color=color)
        graph.edge(node_id, target_a, dir='none', color='gray')
        if target_b is not None:
            graph.edge(node_id, target_b, dir='none', color='gray')