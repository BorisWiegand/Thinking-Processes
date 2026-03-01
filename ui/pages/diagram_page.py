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

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pyscript import window
from puepy import Page, t

from ui.services.diagram_service import DiagramService

T = TypeVar('T')

class DiagramPage(ABC, Page, Generic[T]):

    def initial(self):
        return dict(
            diagram=self._get_diagram_type()(),
            nodes={}
        )

    def populate(self):
        with t.div(classes=["container", "mx-auto", "p-4"]):
            with t.div(classes=["grid grid-cols-1 gap-4"]):
                with t.sl_breadcrumb():
                    t.sl_breadcrumb_item("Thinking Processes", href=".")
                    t.sl_breadcrumb_item(self._get_diagram_type_name())
                self.__populate_toolbar()
                t.div(id="graph", on_click=self.on_click_graph)
                self._populate_control_area()

    @abstractmethod
    def _get_diagram_type_name(self) -> str:
        """
        which type of diagram can be drawn on this page (e.g. Current Reality Tree)?
        this name appears as last the breadcrumb item.  
        """

    @abstractmethod
    def _populate_control_area(self):
        """
        create components to control graph creation 
        """

    @abstractmethod
    def _get_diagram_type(self) -> type[T]:
        """
        gets the diagram class type
        """

    @abstractmethod
    def on_click_graph(self, event):
        """
        handles click events on the graph, e.g. to select nodes 
        """

    def __populate_toolbar(self):
        with t.div(classes=["button-group-toolbar"]):
            with t.sl_button_group(label="Export"):
                with t.sl_tooltip(content="Save as image"):
                    with t.sl_button(on_click=self.download_diagram_as_png):
                        t.sl_icon(name="image")
                with t.sl_tooltip(content="Save as text file"):
                    with t.sl_button(on_click=self.download_diagram_as_txt):
                        t.sl_icon(name="cloud-download")
            with t.sl_button_group(label="Import"):
                with t.sl_tooltip(content="Load diagram"):
                    with t.sl_button(on_click=lambda _: self.refs["file_input"].element.click()):
                        t.sl_icon(name="cloud-upload")
                    t.input(type="file", on_change=self.load_diagram_from_file, id="file_input", ref="file_input", style="display: none;")

    def get_diagram(self) -> T:
        return self.state['diagram']
    
    def redraw_diagram(self):
        DiagramService().draw_diagram(
            self.get_diagram(), 'graph', on_drawn=self.on_diagram_drawn)
        
    def on_diagram_drawn(self):
        pass

    def load_diagram_from_file(self, event):
        def on_file_loaded(e):
            self.state["diagram"] = self._get_diagram_type().from_string(e.target.result)
            self.redraw_diagram()
        file = self.refs["file_input"].element.files.item(0)
        if file is not None:
            reader = window.FileReader.new()
            reader.onload = on_file_loaded
            reader.readAsText(file)

    def download_diagram_as_png(self, event):
        DiagramService().download_diagram_as_png(self.get_diagram())
    
    def download_diagram_as_txt(self, event):
        DiagramService().download_diagram_as_txt(self.get_diagram())
