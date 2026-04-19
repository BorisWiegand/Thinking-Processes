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

from thinking_processes.evaporating_cloud import EvaporatingCloud
from ui.app import app
from ui.pages.diagram_page import DiagramPage
from ui.services.diagram_service import DiagramService

@app.page("/ec")
class EcPage(DiagramPage[EvaporatingCloud]):

    def initial(self):
        return super().initial() | {
        }

    @override
    def _get_diagram_type_name(self) -> str: 
        return 'Evaporating Cloud'

    @override
    def _populate_control_area(self):
        self.redraw_diagram()
        with t.div(classes=["flex", "flex-row", "gap-4"]):
            t.sl_textarea(ref="node_textarea", placeholder="Add text for creating a new node", style="display: none")
            with t.div(classes=["flex", "flex-col", "gap-4"]):
                with t.sl_tooltip(
                    content="Save edited text", 
                    style="display: none;",
                    ref="save_edited_node_text_button"
                ):
                    with t.sl_button(on_click=self.save_edited_node_text):
                        t.sl_icon(name="floppy")

    @override
    def _get_diagram_type(self) -> type[EvaporatingCloud]:
        return lambda: EvaporatingCloud(
            'What is the common objective?',
            'What is the need behind conflicting option A?',
            'What is the need behind conflicting option B?',
            'What is the conflicting option A?',
            'What is the conflicting option B?',
        )
            
    @override
    def on_click_graph(self, event):
        selected_node = DiagramService().get_node_by_event(event)
        if selected_node is not None:
            self.show_node_textfield()
            selected_node.mark_as_selected()
            if selected_node.get_node_id() == 'objective':
                node_text = self.get_diagram().objective
            elif selected_node.get_node_id() == 'need_a':
                node_text = self.get_diagram().need_a
            elif selected_node.get_node_id() == 'need_b':
                node_text = self.get_diagram().need_b
            elif selected_node.get_node_id() == 'conflict_part_a':
                node_text = self.get_diagram().conflict_part_a
            elif selected_node.get_node_id() == 'conflict_part_b':
                node_text = self.get_diagram().conflict_part_b
            else:
                raise NotImplementedError(f'unknown node id "{selected_node.get_node_id()}"')
            self.refs["node_textarea"].element.placeholder = node_text
        else:
            self.clear_selection()

    def hide_node_textfield(self):
        self.refs["node_textarea"].element.style.display = "none"

    def show_node_textfield(self):
        self.refs["node_textarea"].element.style.display = "block"

    def clear_selection(self):
        pass

    def save_edited_node_text(self, event):
        pass