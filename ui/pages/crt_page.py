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
from puepy import Page, t

from thinking_processes.current_reality_tree.current_reality_tree import CurrentRealityTree

from ui.app import app
from ui.services.diagram_service import DiagramService

@app.page("/crt")
class CrtPage(Page):

    def initial(self):
        return dict(
            crt=CurrentRealityTree(),
            selected_effect_list=[],
            selected_causes_list=[],
            nodes={}
        )

    def populate(self):
        with t.div(classes=["container", "mx-auto", "p-4"]):
            with t.div(classes=["grid grid-cols-1 gap-4"]):
                with t.sl_breadcrumb():
                    t.sl_breadcrumb_item("Thinking Processes", href=".")
                    t.sl_breadcrumb_item("Current Reality Tree")
                t.div(id="graph", on_click=self.on_click_graph)
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
                with t.div(classes=["flex", "flex-row", "gap-4"]):
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
                    with t.sl_tooltip(content="Save edited text", ref="save_edited_node_text_button"):
                        with t.sl_button(on_click=self.save_edited_node_text):
                            t.sl_icon(name="floppy")

    def add_new_node(self, event):
        node = self.__get_crt().add_node(self.refs["node_textarea"].element.value)
        self.refs["node_textarea"].element.value = ""
        DiagramService().draw_diagram(
            self.__get_crt(), 'graph', on_drawn=self.on_diagram_drawn)
        self.state["nodes"][node.id] = node

    def save_edited_node_text(self, event):
        self.state["nodes"][self.state["selected_effect_list"][0].get_node_id()].text = self.refs["node_textarea"].element.value

    def on_diagram_drawn(self):
        for node in self.state["selected_effect_list"]:
            node.mark_as_selected()

    def on_click_graph(self, event):
        if self.refs["cancel_connect_to_causes_button"].element.style.display == "none":
            self.__select_node_as_effect(event)
        else:
            print('cause')
            self.__select_node_as_cause(event)

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
        else:
            self.hide_connect_to_causes_button()
            self.hide_delete_node_button()
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

    def hide_connect_to_causes_button(self):
        self.refs["connect_to_causes_button"].element.style.display = "none"

    def show_connect_to_causes_button(self):
        self.refs["connect_to_causes_button"].element.style.display = "block"

    def on_click_connect_to_causes(self, event):
        self.hide_connect_to_causes_button()
        for node in self.state["selected_effect_list"]:
            node.reset_marking()
        self.show_cancel_connect_to_causes_button()

    def hide_confirm_connect_to_causes_button(self):
        self.refs["confirm_connect_to_causes_button"].element.style.display = "none"

    def show_confirm_connect_to_causes_button(self):
        self.refs["confirm_connect_to_causes_button"].element.style.display = "block"

    def on_click_confirm_connect_to_causes(self, event):
        self.hide_confirm_connect_to_causes_button()
        self.hide_cancel_connect_to_causes_button()
        self.__get_crt().add_causal_relation(
            [
                self.state["nodes"][cause.get_node_id()] 
                for cause in self.state["selected_causes_list"]
            ],
            self.state["nodes"][self.state["selected_effect_list"][0].get_node_id()]
        )
        self.state["selected_causes_list"].clear()
        self.state["selected_effect_list"].clear()
        DiagramService().draw_diagram(
            self.__get_crt(), 'graph', on_drawn=self.on_diagram_drawn)

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

    def hide_delete_node_button(self):
        self.refs["delete_node_button"].element.style.display = "none"

    def show_delete_node_button(self):
        self.refs["delete_node_button"].element.style.display = "block"

    def on_click_delete_node(self, event):
        print("delete node")

    def __get_crt(self) -> CurrentRealityTree:
        return self.state["crt"]