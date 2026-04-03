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
from itertools import chain
from typing import override

from graphviz import Digraph, Graph
from more_itertools import first

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
            graph.node(node.id, node.text, fillcolor='white', style='rounded', shape='rect')
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
    
    @override
    def to_string(self):
        return '\n'.join([
            '\n'.join(
                f'{node.id}: {node.text}'
                for node in sorted(chain(
                    self.__injections,
                    self.__intermediate_effects, 
                    self.__desirable_effects, 
                ))
            ),
            '\n'.join(
                (
                    f'{causal_relation.effect.id}:{",".join(c.id for c in causal_relation.causes)}:{causal_relation.effect.text}'
                    if causal_relation.effect in self.__negative_effects
                    else f'{",".join(c.id for c in causal_relation.causes)} -> {causal_relation.effect.id}'
                )
                for causal_relation in sorted(self.__causal_relations, key=lambda c: (c.causes, c.effect))
            )
        ])
    
    @staticmethod
    def from_string(s: str) -> 'FutureRealityTree':
        """
        parses a new FutureRealityTree from a string.

        Example:
            | 1: Car's engine will not start
            | 2: Engine needs fuel in order to run
            | 3: Fuel is not getting to the engine
            | 4: There is water in the fuel line
            | 5: Air conditioning is not working
            | 6: Air is not able to circulate
            | 7: The air intake is full of water
            | 8: Radio sounds distorted
            | 9: The speakers are obstructed
            | 10: The speakers are underwater
            | 11: The car is in the swimming pool
            | 12: The handbreak is faulty
            | 13: The handbreak stops the car\\nfrom rolling into the swimming pool
            | 
            | 2,3 -> 1
            | 4 -> 3
            | 6 => 5
            | 7 -> 6
            | 9 -> 8
            | 10 -> 9
            | 10 <= 11
            | 11 <- 12 13
            | 11 -> 7
            | 11 -> 4

        Args:
            s (str): see above for the format

        Raises:
            ValueError: if there is an error in the format that prevents creating the tree

        Returns:
            FutureRealityTree: if the format is correct
        """
        def get_node_text_from_line(line: str) -> str:
            return line.split(':', maxsplit=1)[1].strip()
        frt = FutureRealityTree()
        for line in s.splitlines():
            if '->' in line:
                cause_ids, effect_id = line.split('->')
                effect_id=effect_id.strip()
                frt.add_causal_relation(
                    [
                        first(node for node in chain(frt.__injections, frt.__intermediate_effects) if node.id == cause_id)
                        for cause_id in map(str.strip, cause_ids.split(','))
                    ],
                    first(node for node in chain(frt.__intermediate_effects, frt.__desirable_effects) if node.id == effect_id)
                )
            elif line.startswith('desirable_effect_'):
                frt.add_desirable_effect(get_node_text_from_line(line))
            elif line.startswith('injection_'):
                frt.add_injection(get_node_text_from_line(line))
            elif line.startswith('intermediate_effect_'):
                frt.add_intermediate_effect(get_node_text_from_line(line))
            elif line.startswith('negative_effect_'):
                try:
                    _, injection_id, node_text = line.split(':', maxsplit=2)
                except ValueError as e:
                    raise ValueError(line) from e
                frt.add_negative_effect(
                    first(i for i in frt.__injections if i.id == injection_id),
                    node_text.strip()
                )
            elif line:
                raise ValueError(f'Cannot parse line: {line}')
        return frt
    