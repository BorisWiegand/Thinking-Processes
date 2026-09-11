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

from puepy import t

from thinking_processes.prerequisite_tree.node import Obstacle, Solution
from thinking_processes.prerequisite_tree.prerequisite_tree import PrerequisiteTree
from ui.app import app
from ui.models.diagram_node import DiagramNode
from ui.pages.diagram_page import DiagramPage
from ui.services.diagram_service import DiagramService

@app.page("/prt")
class PrtPage(DiagramPage[PrerequisiteTree]):

    def initial(self):
        return super().initial() | {
            'selected_nodes': [],
        }

    @override
    def _get_diagram_type_name(self) -> str: 
        return 'Prerequisite Tree'

    @override
    def _get_diagram_type(self) -> type[PrerequisiteTree]:
        return lambda: PrerequisiteTree('What is your desired goal or effect?')

    @override
    def _populate_control_area(self):
        self.redraw_diagram()
        with t.div(classes=["flex", "flex-row", "gap-4"]):
            t.sl_textarea(ref="node_textarea", style="display: none")
            with t.div(classes=["flex", "flex-col", "gap-4"]):
                with t.sl_tooltip(
                    content="Save text", 
                    style="display: none;",
                    ref="save_node_text_button"
                ):
                    with t.sl_button(on_click=self.save_node_text):
                        t.sl_icon(name="floppy")
                with t.sl_tooltip(
                    content="Add an obstacle node to the selected node", 
                    style="display: none;",
                    ref="add_obstacle_button"
                ):
                    with t.sl_button(on_click=self.add_obstacle_node):
                        t.sl_icon(name="bricks")
                with t.sl_tooltip(
                    content="Add a solution node to the selected node", 
                    style="display: none;",
                    ref="add_solution_button"
                ):
                    with t.sl_button(on_click=self.add_solution_node):
                        t.sl_icon(name="lightbulb")
                with t.sl_tooltip(
                    content="Delete node", 
                    style="display: none;",
                    ref="delete_node_button"
                ):
                    with t.sl_button(on_click=self.delete_node):
                        t.sl_icon(name="trash")
                

    @override
    def on_click_graph(self, event):
        selected_node = DiagramService().get_node_by_event(event)
        self.clear_selection()
        if selected_node is not None:
            selected_node.mark_as_selected()
            node_text = self.__get_node_text(selected_node)
            self.refs["node_textarea"].element.value = node_text
            self.state['selected_nodes'].append(selected_node)
            self.show_node_textfield()
            self.show_save_node_text_button()
            if selected_node.get_node_id() == 'objective':
                self.show_add_obstacle_button()
            else:
                node = self.get_diagram().get_node_by_id(str(selected_node.get_node_id()))
                self.show_delete_button()
                if isinstance(node, Obstacle):
                    self.show_add_solution_button()
                else:
                    self.show_add_obstacle_button()

    def __get_node_text(self, node: DiagramNode) -> str:
        if node.get_node_id() == 'objective':
            return self.get_diagram().objective
        else:
            return self.get_diagram().get_node_by_id(str(node.get_node_id())).text

    def __set_node_text(self, node: DiagramNode, text: str):
        if node.get_node_id() == 'objective':
            self.get_diagram().objective = text
        else:
            self.get_diagram().get_node_by_id(str(node.get_node_id())).text = text

    def save_node_text(self, event):
        self.__set_node_text(
            self.state['selected_nodes'][0], 
            self.refs["node_textarea"].element.value
        )
        self.clear_selection()

    def clear_selection(self):
        for node in self.state['selected_nodes']:
            node.reset_marking()
        self.state['selected_nodes'].clear()
        self.hide_node_textfield()
        self.hide_save_node_text_button()
        self.hide_add_obstacle_button()
        self.hide_add_solution_button()
        self.hide_delete_button()
        self.redraw_diagram()

    def hide_node_textfield(self):
        self.refs["node_textarea"].element.style.display = "none"

    def show_node_textfield(self):
        self.refs["node_textarea"].element.style.display = "block"

    def hide_save_node_text_button(self):
        self.refs["save_node_text_button"].element.style.display = "none"

    def show_save_node_text_button(self):
        self.refs["save_node_text_button"].element.style.display = "block"

    def hide_add_obstacle_button(self):
        self.refs["add_obstacle_button"].element.style.display = "none"

    def show_add_obstacle_button(self):
        self.refs["add_obstacle_button"].element.style.display = "block"

    def hide_add_solution_button(self):
        self.refs["add_solution_button"].element.style.display = "none"

    def show_add_solution_button(self):
        self.refs["add_solution_button"].element.style.display = "block"
    
    def hide_delete_button(self):
        self.refs["delete_node_button"].element.style.display = "none"

    def show_delete_button(self):
        self.refs["delete_node_button"].element.style.display = "block"

    def add_obstacle_node(self, event):
        selected_node = self.state['selected_nodes'][0]
        if selected_node.get_node_id() == 'objective':
            self.get_diagram().add_obstacle('New Obstacle')
        else:
            self.get_diagram().get_node_by_id(str(selected_node.get_node_id())).add_obstacle('New Obstacle')
        self.clear_selection()

    def add_solution_node(self, event):
        selected_node = self.state['selected_nodes'][0]
        node = self.get_diagram().get_node_by_id(str(selected_node.get_node_id()))
        if isinstance(node, Obstacle):
            node.add_solution('New Solution')
        else:
            raise NotImplementedError(node.get_node_id())
        self.clear_selection()

    def delete_node(self, event):
        selected_node = self.state['selected_nodes'][0]
        self.get_diagram().remove_node_by_id(str(selected_node.get_node_id()))
        self.clear_selection()


    
