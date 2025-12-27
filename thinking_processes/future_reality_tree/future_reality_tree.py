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

from thinking_processes.future_reality_tree.causal_relation import CausalRelation
from thinking_processes.future_reality_tree.node import Node
from thinking_processes.diagram import Diagram

class FutureRealityTree(Diagram):
    """
    you can use a future reality tree to analyze necessary injections that cause a set of desirable effects.
    """

    def __init__(self):
        self.__desirable_effects: set[Node] = set()
        self.__injections: set[Node] = set()
        self.__intermediate_effects: set[Node] = set()
        self.__negative_effects: set[Node] = set()
        self.__causal_relations: list[CausalRelation] = []

    def add_desirable_effect(self, text: str) -> Node:
        """
        adds a node representing a desirable effect to this future reality tree.

        Args:
            text (str): statement of the node, e.g. "we get more customers"

        Returns:
            Node: the created node. you can use this to create connections to it
        """
        node = Node(f'desirable_effect_{len(self.__desirable_effects)+1}', text)
        self.__desirable_effects.add(node)
        return node

    def add_injection(self, text: str) -> Node:
        """
        adds a node representing an injection to this future reality tree.

        Args:
            text (str): statement of the node, e.g. "we train our sales people"

        Returns:
            Node: the created node. you can use this to create connections from it
        """
        node = Node(f'injection_{len(self.__injections)+1}', text)
        self.__injections.add(node)
        return node

    def add_intermediate_effect(self, text: str) -> Node:
        """
        adds a node representing an intermediate effect to this future reality tree.

        Args:
            text (str): statement of the node, e.g. "our sales people are well trained"

        Returns:
            Node: the created node. you can use this to create connections from it
        """
        node = Node(f'intermediate_effect_{len(self.__intermediate_effects)+1}', text)
        self.__intermediate_effects.add(node)
        return node
    
    def add_negative_effect(self, injection: Node, text: str): 
        if injection not in self.__injections:
            raise ValueError(f'{node} is not an injection')
        node = Node(f'negative_effect_{len(self.__negative_effects)+1}', text) 
        self.__negative_effects.add(node)
        self.add_causal_relation([injection], node)
        return node

    def add_causal_relation(self, causes: list[Node], effect: Node):
        """
        adds a causal relation (an arrow) from a list of causes to an effect.
        read cause1 AND cause2 AND ... causeN causes effect.

        Args:
            causes (list[Node]): 
            a group of nodes. the connections of multiple nodes will be highlighted with an ellipsis
            representing an AND-relationship
            effect (Node): the effect of the relation
        """
        if not causes:
            raise ValueError('causes must not be empty')
        for cause in causes:
            if cause in self.__desirable_effects:
                raise ValueError(f'desirable effect "{cause.text}" must not be a cause')
        if effect in self.__injections:
            raise ValueError(f'injection "{effect.text}" must not be an effect')
        self.__causal_relations.append(CausalRelation(causes, effect))
        
    @override
    def to_graphviz(self) -> Graph:
        graph = Digraph(graph_attr=dict(rankdir="BT"))
        for node in self.__desirable_effects:
            graph.node(node.id, node.text, fillcolor='lightgreen', style='filled,rounded', shape='rect')
        for node in self.__negative_effects:
            graph.node(node.id, node.text, fillcolor='red', style='filled,rounded', shape='rect')
        for node in self.__injections:
            graph.node(node.id, node.text, fillcolor='lightblue', style='filled', shape='hexagon')
        for node in self.__intermediate_effects:
            graph.node(node.id, node.text, style='rounded', shape='rect')
        for i,relation in enumerate(self.__causal_relations):
            if len(relation.causes) == 1:
                graph.edge(str(relation.causes[0].id), str(relation.effect.id))
            else:
                with graph.subgraph(name=f'cluster_{i}', graph_attr=dict(style='rounded')) as subgraph:
                    for cause in relation.causes:
                        mid_of_edge_id = f'{cause.id}-{relation.effect.id}'
                        subgraph.node(mid_of_edge_id, label='', margin='0', height='0', width='0')
                        graph.edge(str(cause.id), mid_of_edge_id, arrowhead='none')
                        graph.edge(mid_of_edge_id, str(relation.effect.id))
        return graph
    