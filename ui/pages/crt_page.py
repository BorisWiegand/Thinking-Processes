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

from pyscript import window
from puepy import t

from thinking_processes.current_reality_tree.current_reality_tree import CurrentRealityTree

from ui.app import app
from ui.pages.diagram_page import DiagramPage
from ui.services.diagram_service import DiagramService

@app.page("/crt")
class CrtPage(DiagramPage[CurrentRealityTree]):

    @override
    def initial(self):
        return super().initial() | dict(
            selected_effect_list=[],
            selected_causes_list=[],
            selected_edges=[],
        )

    @override
    def _get_diagram_type(self) -> type[CurrentRealityTree]:
        return CurrentRealityTree

    @override
    def _get_diagram_type_name(self) -> str: 
        return 'Current Reality Tree'

    @override
    def _populate_control_area(self):
        with t.div(classes=["flex", "flex-row", "gap-4"]):
            with t.sl_button(
                on_click=self.on_click_connect_to_causes, 
                ref="connect_to_causes_button", 
                style="display: none;"
            ):
                t.sl_icon(name="link", slot="prefix")
                t.raw("Connect to causes")
            with t.sl_tooltip(
                content="Remove selected node",
                ref="delete_node_button", 
                style="display: none;"
            ):
                with t.sl_button(
                    on_click=self.on_click_delete_node, 
                ):
                    t.sl_icon(name="trash", slot="prefix")
            with t.sl_tooltip(
                content="Remove selected edge",
                ref="delete_edge_button", 
                style="display: none;"
            ):
                with t.sl_button(
                    on_click=self.on_click_delete_edge, 
                ):
                    t.sl_icon(name="trash", slot="prefix")
            with t.sl_tooltip(
                content="Connect selected node to its causes",
                style="display: none;",
                ref="confirm_connect_to_causes_button"):
                    with t.sl_button(on_click=self.on_click_confirm_connect_to_causes):
                        t.sl_icon(name="check")
            with t.sl_tooltip(
                content="Cancel",
                style="display: none;",
                ref="cancel_connect_to_causes_button"):
                    with t.sl_button(on_click=self.on_click_cancel_connect_to_causes):
                        t.sl_icon(name="x")
        with t.div(classes=["flex", "flex-row", "gap-4"]):
            t.sl_textarea(ref="node_textarea", placeholder="Describe an undesired effect or its cause")
            with t.sl_tooltip(content="Add new node", ref="add_node_button"):
                with t.sl_button(on_click=self.add_new_node):
                    t.sl_icon(name="plus")
            with t.sl_tooltip(
                content="Save edited text", 
                style="display: none;",
                ref="save_edited_node_text_button"
            ):
                with t.sl_button(on_click=self.save_edited_node_text):
                    t.sl_icon(name="floppy")

    def add_new_node(self, event):
        node = self.get_diagram().add_node(self.refs["node_textarea"].element.value)
        self.refs["node_textarea"].element.value = ""
        self.redraw_diagram()
        self.state["nodes"][node.id] = node

    def save_edited_node_text(self, event):
        self.state["nodes"][self.state["selected_effect_list"][0].get_node_id()].text = self.refs["node_textarea"].element.value
        self.redraw_diagram()

    @override
    def on_diagram_drawn(self):
        for node in self.state["selected_effect_list"]:
            node.mark_as_selected()

    @override
    def on_click_graph(self, event):
        if self.refs["cancel_connect_to_causes_button"].element.style.display == "none":
            self.__select_node_as_effect(event)
        else:
            self.__select_node_as_cause(event)
        self.__select_edge(event)

    def __select_node_as_effect(self, event):
        selected_node = DiagramService().get_node_by_event(event)
        for node in self.state["selected_effect_list"]:
            node.reset_marking()
        if selected_node is not None:
            if self.state["selected_effect_list"]:
                self.state["selected_effect_list"].clear()
            selected_node.mark_as_selected()
            self.state["selected_effect_list"].append(selected_node)
            self.show_connect_to_causes_button()
            self.show_delete_node_button()
            self.show_save_edited_node_text_button()
            self.hide_add_node_button()
            self.refs["node_textarea"].element.value = self.state["nodes"][self.state["selected_effect_list"][0].get_node_id()].text
        else:
            self.hide_connect_to_causes_button()
            self.hide_delete_node_button()
            self.hide_save_edited_node_text_button()
            self.show_add_node_button()
            self.state["selected_effect_list"].clear()

    def __select_node_as_cause(self, event):
        selected_node = DiagramService().get_node_by_event(event)
        if selected_node is not None and selected_node not in self.state["selected_effect_list"]:
            if selected_node not in self.state["selected_causes_list"]:
                selected_node.mark_as_selected()
                self.state["selected_causes_list"].append(selected_node)
            else:
                selected_node.reset_marking()
                self.state["selected_causes_list"].remove(selected_node)
        if self.state["selected_causes_list"]:
            self.show_confirm_connect_to_causes_button()
        else:
            self.hide_confirm_connect_to_causes_button()

    def __select_edge(self, event):
        selected_edge = DiagramService().get_edge_by_event(event)
        for edge in self.state["selected_edges"]:
            edge.reset_marking()
        self.state["selected_edges"].clear()
        if selected_edge is not None:
            self.state["selected_edges"].append(selected_edge)
            selected_edge.mark_as_selected()
            self.show_delete_edge_button()
        else:
            self.hide_delete_edge_button()

    def hide_connect_to_causes_button(self):
        self.refs["connect_to_causes_button"].element.style.display = "none"

    def show_connect_to_causes_button(self):
        self.refs["connect_to_causes_button"].element.style.display = "block"

    def on_click_connect_to_causes(self, event):
        self.hide_connect_to_causes_button()
        for node in self.state["selected_effect_list"]:
            node.reset_marking()
        self.show_cancel_connect_to_causes_button()
        self.hide_save_edited_node_text_button()
        self.hide_delete_node_button()

    def hide_confirm_connect_to_causes_button(self):
        self.refs["confirm_connect_to_causes_button"].element.style.display = "none"

    def show_confirm_connect_to_causes_button(self):
        self.refs["confirm_connect_to_causes_button"].element.style.display = "block"

    def on_click_confirm_connect_to_causes(self, event):
        self.hide_confirm_connect_to_causes_button()
        self.hide_cancel_connect_to_causes_button()
        self.get_diagram().add_causal_relation(
            [
                self.state["nodes"][cause.get_node_id()] 
                for cause in self.state["selected_causes_list"]
            ],
            self.state["nodes"][self.state["selected_effect_list"][0].get_node_id()]
        )
        self.state["selected_causes_list"].clear()
        self.state["selected_effect_list"].clear()
        self.redraw_diagram()
        self.show_add_node_button()

    def hide_cancel_connect_to_causes_button(self):
        self.refs["cancel_connect_to_causes_button"].element.style.display = "none"

    def show_cancel_connect_to_causes_button(self):
        self.refs["cancel_connect_to_causes_button"].element.style.display = "block"

    def on_click_cancel_connect_to_causes(self, event):
        self.hide_confirm_connect_to_causes_button()
        self.hide_cancel_connect_to_causes_button()
        for cause in self.state["selected_causes_list"]:
            cause.reset_marking()
        for effect in self.state["selected_effect_list"]:
            effect.reset_marking()
        self.state["selected_causes_list"].clear()
        self.state["selected_effect_list"].clear()
        self.show_add_node_button()

    def hide_delete_node_button(self):
        self.refs["delete_node_button"].element.style.display = "none"

    def show_delete_node_button(self):
        self.refs["delete_node_button"].element.style.display = "block"

    def hide_delete_edge_button(self):
        self.refs["delete_edge_button"].element.style.display = "none"

    def show_delete_edge_button(self):
        self.refs["delete_edge_button"].element.style.display = "block"

    def on_click_delete_node(self, event):
        node_to_delete = self.state["selected_effect_list"][0]
        self.get_diagram().delete_node(self.state["nodes"][node_to_delete.get_node_id()])
        self.state["selected_effect_list"].clear()
        self.hide_delete_node_button()
        self.hide_save_edited_node_text_button()
        self.show_add_node_button()
        self.redraw_diagram()

    def on_click_delete_edge(self, event):
        for edge_to_delete in self.state["selected_edges"]:
            self.get_diagram().remove_cause_from_effect(
                self.state["nodes"][edge_to_delete.from_node_id],
                self.state["nodes"][edge_to_delete.to_node_id]
            )
        self.state["selected_edges"].clear()
        self.hide_delete_edge_button()
        self.redraw_diagram()

    def hide_save_edited_node_text_button(self):
        self.refs["save_edited_node_text_button"].element.style.display = "none"
        self.refs["node_textarea"].element.value = ""

    def show_save_edited_node_text_button(self):
        self.refs["save_edited_node_text_button"].element.style.display = "block"

    def hide_add_node_button(self):
        self.refs["add_node_button"].element.style.display = "none"

    def show_add_node_button(self):
        self.refs["add_node_button"].element.style.display = "block"
