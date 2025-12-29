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
import re
from typing import override

from graphviz import Digraph, Graph

from thinking_processes.current_reality_tree.causal_relation import CausalRelation
from thinking_processes.current_reality_tree.node import Node
from thinking_processes.diagram import Diagram

NODE_ID_PATTERN = re.compile(r'[1-9]\d*')
NODE_LINE_PATTERN = re.compile(rf'{NODE_ID_PATTERN.pattern}:.+')
RIGHT_ARROW_PATTERN = re.compile(r'(->|=>)')
LEFT_ARROW_PATTERN = re.compile(r'(<-|<=)')
Y_CAUSED_BY_X_LINE_PATTERN = re.compile(rf'[1-9]\d*\s*{LEFT_ARROW_PATTERN.pattern}(\s*[1-9]\d*,?)+')
X_CAUSES_Y_LINE_PATTERN = re.compile(rf'(\s*[1-9]\d*,?)+\s*{RIGHT_ARROW_PATTERN.pattern}\s*([1-9]\d*)')
RELATION_LINE_PATTERN = re.compile(rf'({X_CAUSES_Y_LINE_PATTERN.pattern}|{Y_CAUSED_BY_X_LINE_PATTERN.pattern})\s*')
NODE_ID_LIST_SEPARATOR_PATTERN = re.compile(r'(\s*,\s*|\s+)')

class CurrentRealityTree(Diagram):
    """
    you can use current reality tree to analyze the root-causes of a set of undesired effects (problems).

    https://en.wikipedia.org/wiki/Current_reality_tree_(theory_of_constraints)
    """

    def __init__(self):
        self.__nodes: list[Node] = []
        self.__causal_relations: list[CausalRelation] = []
    
    def add_node(self, text: str, id: int|None = None) -> Node:
        """
        adds a node to this current reality tree

        Args:
            text (str): 
                text of the new node
        Returns:
            Node: the newly created node
        """
        new_node = Node(
            len(self.__nodes) if id is None else id,
            text
        )
        self.__nodes.append(new_node)
        return new_node

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
        self.__causal_relations.append(CausalRelation(causes, effect))
        
    @override
    def to_graphviz(self) -> Graph:
        graph = Digraph(graph_attr=dict(rankdir="BT"))
        for node in self.__nodes:
            if not any(c.effect == node for c in self.__causal_relations):
                node_attributes = dict(fillcolor='lightgreen', style='filled')
            elif not any(node in c.causes for c in self.__causal_relations):
                node_attributes = dict(fillcolor='yellow', style='filled')
            else:
                node_attributes = {}
            graph.node(
                str(node.id), 
                node.text,
                shape='rect',
                **node_attributes
            )
        for i,causal_relation in enumerate(self.__causal_relations):
            if len(causal_relation.causes) == 1:
                graph.edge(str(causal_relation.causes[0].id), str(causal_relation.effect.id))
            else:
                with graph.subgraph(name=f'cluster_{i}', graph_attr=dict(style='rounded')) as subgraph:
                    for cause in causal_relation.causes:
                        mid_of_edge_id = f'{cause.id}-{causal_relation.effect.id}'
                        subgraph.node(mid_of_edge_id, label='', margin='0', height='0', width='0')
                        graph.edge(str(cause.id), mid_of_edge_id, arrowhead='none')
                        graph.edge(mid_of_edge_id, str(causal_relation.effect.id))
        return graph

    def get_nr_of_nodes(self) -> int:
        return len(self.__nodes)

    def get_nr_of_causal_relations(self) -> int:
        return len(self.__causal_relations)
    
    @staticmethod
    def from_txt_file(path_to_txt: str) -> 'CurrentRealityTree':
        """
        creates a CurrentRealityTree from a .txt file. 
        See CurrentRealityTree.from_string for the expected file content.

        Args:
            path_to_txt (str): e.g. 'a_folder/crt.txt'

        Returns:
            CurrentRealityTree: 
            a CurrentRealityTree with nodes and relations as defined in the file content.
        """
        with open(path_to_txt, 'r') as f:
            return CurrentRealityTree.from_string(f.read())

    @staticmethod
    def from_string(s: str) -> 'CurrentRealityTree':
        """
        parses a new CurrentRealityTree from a string.

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
            CurrentRealityTree: if the format is correct
        """
        crt = CurrentRealityTree()
        nodes_by_id: dict[int, Node] = {}
        for line in s.splitlines():
            line = line.strip()
            if NODE_LINE_PATTERN.match(line):
                CurrentRealityTree._parse_node_line(line, nodes_by_id, crt)
            elif RELATION_LINE_PATTERN.match(line):
                CurrentRealityTree._parse_relation_line(line, nodes_by_id, crt)
            elif line != '':
                raise ValueError(f'Unsupported line format: "{line}"')
        return crt
    
    @staticmethod
    def _parse_node_line(line: str, nodes_by_id: dict[int, Node], crt: 'CurrentRealityTree'):
        node_id, node_text = map(str.strip, line.split(':', maxsplit=1))
        node = crt.add_node(node_text.replace('\\n', '\n'), id=int(node_id))
        if node.id in nodes_by_id:
            raise ValueError(f'Two nodes have the same id {node.id}')
        nodes_by_id[node.id] = node
    
    @staticmethod
    def _parse_relation_line(line: str, nodes_by_id: dict[int, Node], crt: 'CurrentRealityTree'):
        if X_CAUSES_Y_LINE_PATTERN.match(line):
            x, _, y = RIGHT_ARROW_PATTERN.split(line, maxsplit=1)
        else:
            y, _, x = LEFT_ARROW_PATTERN.split(line, maxsplit=1)
        try:
            x = [
                nodes_by_id[int(node_id)] 
                for node_id in NODE_ID_LIST_SEPARATOR_PATTERN.split(x)
                if NODE_ID_PATTERN.match(node_id)
            ]
            y = nodes_by_id[int(y)]
        except KeyError:
            raise ValueError(f'relation contains undefined node: {line}')
        crt.add_causal_relation(x, y)