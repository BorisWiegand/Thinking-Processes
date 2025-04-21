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

from thinking_processes.current_reality_tree.causal_relation import CausalRelation
from thinking_processes.current_reality_tree.node import Node

class CurrentRealityTree:
    """
    you can use current reality tree to analyze the root-causes of a set of undesired effects (problems).

    https://en.wikipedia.org/wiki/Current_reality_tree_(theory_of_constraints)
    """

    def __init__(self):
        self.__nodes: list[Node] = []
        self.__causal_relations: list[CausalRelation] = []
    
    def add_node(self, text: str) -> Node:
        """
        adds a node to this current reality tree

        Args:
            text (str): 
                text of the new node
        Returns:
            Node: the newly created node
        """
        new_node = Node(
            len(self.__nodes),
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
        
    def plot(self, view: bool = True, filepath: str|None = None):
        """
        plots this current reality tree.

        Args:
            view (bool, optional): set to False if you do not want to immediately view the diagram. Defaults to True.
            filepath (str | None, optional): path to the file in which you want to save the plot. Defaults to None.
        """
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
        #we do not want to see the generated .dot code 
        # => write it to a temporary file
        with TemporaryDirectory() as tempdir:
            graph.render(filename=os.path.join(tempdir, 'crt.gv'), view=view, outfile=filepath)