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

from thinking_processes.current_reality_tree.current_reality_tree import CurrentRealityTree
from ui.app import app

from puepy import Page, t

@app.page("/crt")
class CrtPage(Page):
    def initial(self):
        return dict(
            new_node_text="",
            crt=CurrentRealityTree()
        )

    def populate(self):
        with t.div(classes=["container", "mx-auto", "p-4"]):
            with t.div(classes=["grid grid-col-1 md:grid-col-2 gap-4"]):
                with t.div(id="graph"):
                    self.state["crt"].get_nr_of_nodes()
                with t.div(classes=["flex", "flex-row", "gap-4"]):
                    t.sl_textarea(bind="new_node_text")
                    t.sl_button("+", on_click=self.add_new_node)

    def add_new_node(self, event):
        self.state["crt"].add_node(self.state["new_node_text"])
        self.state["new_node_text"] = ""