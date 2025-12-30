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
from pyscript import ffi
from puepy import Page, t
from puepy.core import html

from thinking_processes.current_reality_tree.current_reality_tree import CurrentRealityTree

from ui.app import app
from ui.services.diagram_service import DiagramService

@app.page("/crt")
class CrtPage(Page):

    def initial(self):
        return dict(
            crt=CurrentRealityTree()
        )

    def populate(self):
        with t.div(classes=["container", "mx-auto", "p-4"]):
            with t.div(classes=["grid grid-col-1 grid-col-2:md gap-4"]):
                t.div(id="graph", on_click=self.on_click_graph)
                with t.div(classes=["flex", "flex-row", "gap-4"]):
                    t.sl_textarea(ref="new_node_textarea")
                    t.sl_button("+", on_click=self.add_new_node)

    def add_new_node(self, event):
        self.__get_crt().add_node(self.refs["new_node_textarea"].element.value)
        self.refs["new_node_textarea"].element.value = ""
        DiagramService().draw_diagram(self.__get_crt(), 'graph')

    def on_click_graph(self, event):
        print(event.target)
        print(dir(event.target))
        if event.target.tagName == "polygon":
            event.target.setAttribute("stroke", "lightblue")

    def __get_crt(self) -> CurrentRealityTree:
        return self.state["crt"]