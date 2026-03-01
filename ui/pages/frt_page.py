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

from thinking_processes.future_reality_tree.future_reality_tree import FutureRealityTree
from ui.app import app
from ui.pages.diagram_page import DiagramPage
from ui.services.diagram_service import DiagramService

@app.page("/frt")
class FrtPage(DiagramPage[FutureRealityTree]):

    def initial(self):
        return super().initial()

    @override
    def _get_diagram_type_name(self) -> str: 
        return 'Future Reality Tree'

    @override
    def _populate_control_area(self):
        with t.div(classes=["flex", "flex-row", "gap-4"]):
            t.sl_textarea(ref="injection_textarea", placeholder="Describe an injection to achieve some desired effect")
            with t.sl_tooltip(content="Add an injection", ref="add_injection_button"):
                with t.sl_button(on_click=self.add_injection):
                    t.sl_icon(name="plus")

    def add_injection(self, event):
        node = self.get_diagram().add_injection(self.refs["injection_textarea"].element.value)
        self.refs["injection_textarea"].element.value = ""
        self.redraw_diagram()
        self.state["nodes"][node.id] = node

    @override
    def _get_diagram_type(self) -> type[FutureRealityTree]:
        return FutureRealityTree

    def on_click_graph(self, event):
        pass