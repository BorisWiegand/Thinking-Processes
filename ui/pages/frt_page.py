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

from more_itertools import first

from pyscript import window
from puepy import t

from thinking_processes.future_reality_tree.future_reality_tree import FutureRealityTree
from thinking_processes.future_reality_tree.future_reality_tree import Node
from ui.app import app
from ui.pages.diagram_page import DiagramPage
from ui.services.diagram_service import DiagramService

NODE_TYPE_INJECTION = 'injection'
NODE_TYPE_INTERMEDIATE_EFFECT = 'intermediate_effect'
NODE_TYPE_DESIRABLE_EFFECT = 'desirable_effect'

@app.page("/frt")
class FrtPage(DiagramPage[FutureRealityTree]):

    def initial(self):
        return super().initial() | {
            'nodes': {
                NODE_TYPE_INJECTION: {},
                NODE_TYPE_INTERMEDIATE_EFFECT: {},
                NODE_TYPE_DESIRABLE_EFFECT: {},
            },
            'selected_nodes': {
                NODE_TYPE_INJECTION: [],
                NODE_TYPE_INTERMEDIATE_EFFECT: [],
                NODE_TYPE_DESIRABLE_EFFECT: [],
            },
            'selected_edges': [],
        }

    @override
    def _get_diagram_type_name(self) -> str: 
        return 'Future Reality Tree'

    @override
    def _populate_control_area(self):
        with t.div(classes=["flex", "flex-row", "gap-4"]):
            with t.sl_button(
                on_click=self.on_click_connect_injections_to_effects, 
                ref="connect_injections_to_effects_button", 
                style="display: none;"
            ):
                t.sl_icon(name="link", slot="prefix")
                t.raw("Connect injection(s) to effect(s)")
        with t.div(classes=["flex", "flex-row", "gap-4"]):
            t.sl_textarea(ref="node_textarea", placeholder="Add text for creating a new node")
            with t.div(classes=["flex", "flex-col", "gap-4"]):
                with t.sl_tooltip(content="Add an injection to achieve some desired effect", ref="add_injection_button"):
                    with t.sl_button('Add injection', on_click=self.add_injection):
                        t.sl_icon(name="plus", slot="prefix")
                with t.sl_tooltip(content="Add an intermediate effect caused by an injection or some other effect", ref="add_intermediate_effect_button"):
                    with t.sl_button('Add intermediate effect', on_click=self.add_intermediate_effect):
                        t.sl_icon(name="plus", slot="prefix")
                with t.sl_tooltip(content="Add a desirable effect", ref="add_desirable_effect_button"):
                    with t.sl_button('Add desirable effect', on_click=self.add_desirable_effect):
                        t.sl_icon(name="plus", slot="prefix")

    def add_injection(self, event):
        self.__add_node(
            self.get_diagram().add_injection(self.refs["node_textarea"].element.value),
            NODE_TYPE_INJECTION
        )

    def add_intermediate_effect(self, event):
        self.__add_node(
            self.get_diagram().add_intermediate_effect(self.refs["node_textarea"].element.value),
            NODE_TYPE_INTERMEDIATE_EFFECT
        )

    def add_desirable_effect(self, event):
        self.__add_node(
            self.get_diagram().add_desirable_effect(self.refs["node_textarea"].element.value),
            NODE_TYPE_DESIRABLE_EFFECT
        )

    def __add_node(self, node: Node, node_type: str):
        self.refs["node_textarea"].element.value = ""
        self.redraw_diagram()
        self.state['nodes'][node_type][node.id] = node

    @override
    def _get_diagram_type(self) -> type[FutureRealityTree]:
        return FutureRealityTree

    def on_click_graph(self, event):
        selected_node = DiagramService().get_node_by_event(event)
        if selected_node is not None:
            for node_type in [NODE_TYPE_DESIRABLE_EFFECT, NODE_TYPE_INJECTION, NODE_TYPE_INTERMEDIATE_EFFECT]:
                if selected_node.get_node_id() in self.state['nodes'][node_type]:
                    if selected_node not in self.state['selected_nodes'][node_type]:
                        selected_node.mark_as_selected()
                        self.state['selected_nodes'][node_type].append(selected_node)
                    else:
                        first(
                            s for s in self.state['selected_nodes'][node_type]
                            if s == selected_node
                        ).reset_marking()
                        self.state['selected_nodes'][node_type].remove(selected_node)

        else:
            self.__clear_selection()
        if self.state['selected_nodes'][NODE_TYPE_INJECTION] \
        and (self.state['selected_nodes'][NODE_TYPE_INTERMEDIATE_EFFECT] or self.state['selected_nodes'][NODE_TYPE_DESIRABLE_EFFECT]):
            self.show_connect_injections_to_effects_button()
        else:
            self.hide_connect_injections_to_effects_button()

    def __clear_selection(self):
        for selected_node_set in self.state['selected_nodes'].values():
            for selected_node in selected_node_set:
                selected_node.reset_marking()
            selected_node_set.clear()
        
    def hide_connect_injections_to_effects_button(self):
        self.refs["connect_injections_to_effects_button"].element.style.display = "none"

    def show_connect_injections_to_effects_button(self):
        self.refs["connect_injections_to_effects_button"].element.style.display = "block"

    def on_click_connect_injections_to_effects(self, event):
        injections = [
            self.state['nodes'][NODE_TYPE_INJECTION][injection_node.get_node_id()]
            for injection_node in self.state['selected_nodes'][NODE_TYPE_INJECTION]
        ]
        for effect_node_type in [NODE_TYPE_INTERMEDIATE_EFFECT, NODE_TYPE_DESIRABLE_EFFECT]:
            for effect_node in self.state['selected_nodes'][effect_node_type]:
                self.get_diagram().add_causal_relation(
                    injections,
                    self.state['nodes'][effect_node_type][effect_node.get_node_id()]
                )
        self.__clear_selection()
        self.redraw_diagram()
            