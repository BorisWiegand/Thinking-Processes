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
            t.sl_textarea(ref="node_textarea", placeholder="Add text for creating a new node")
            # with t.div(classes=["flex", "flex-col", "gap-4"]):
            #     with t.sl_tooltip(content="Add an injection to achieve some desired effect", ref="add_injection_button"):
            #         with t.sl_button('Add injection', on_click=self.add_injection):
            #             t.sl_icon(name="plus", slot="prefix")
            #     with t.sl_tooltip(content="Add an intermediate effect caused by an injection or some other effect", ref="add_intermediate_effect_button"):
            #         with t.sl_button('Add intermediate effect', on_click=self.add_intermediate_effect):
            #             t.sl_icon(name="plus", slot="prefix")
            #     with t.sl_tooltip(content="Add a desirable effect", ref="add_desirable_effect_button"):
            #         with t.sl_button('Add desirable effect', on_click=self.add_desirable_effect):
            #             t.sl_icon(name="plus", slot="prefix")

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
        pass