import asyncio
from pyscript import window, document

from thinking_processes.diagram import Diagram
from ui.models.diagram_node import DiagramNode
from ui.services.download_service import DownloadService

class DiagramService:

    def draw_diagram(self, diagram: Diagram, container_id: str, on_drawn=None):
        """
        Draws the given diagram and adds it to the DOM
        """
        task = asyncio.create_task(
            self.__render_graphviz_to_html(str(diagram.to_graphviz()), container_id)
        )
        if on_drawn is not None:
            task.add_done_callback(lambda _: on_drawn())

    def download_diagram_as_png(self, diagram: Diagram, file_name: str = "diagram.png"):
        """
        Draws and downloads the given diagram as png
        """
        async def task():
            viz = await window.Viz.instance()
            svg_element = viz.renderSVGElement(str(diagram.to_graphviz()))
            window.saveSvgAsPng(svg_element, file_name)
        asyncio.create_task(task())

    def download_diagram_as_txt(self, diagram: Diagram, file_name: str = 'diagram.txt'):
        """
        creates a string representation of the diagram and downloads this string
        as a text file
        """
        DownloadService().download_text(diagram.to_string(), file_name)

    async def __render_graphviz_to_html(self, graphviz_source: str, container_id: str):
        viz = await window.Viz.instance()
        svg_element = viz.renderSVGElement(graphviz_source)
        container = document.getElementById(container_id)
        container.innerHTML = ""
        container.append(svg_element)

    def get_node_by_event(self, event) -> DiagramNode|None:
        current_node = event.target
        while current_node.tagName != "g":
            if not current_node.parentElement:
                return None
            current_node = current_node.parentElement
        if not current_node.classList.contains("node"):
            return None
        return DiagramNode(current_node.id)