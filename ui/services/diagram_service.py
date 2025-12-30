import asyncio
from pyscript import window, document

from thinking_processes.diagram import Diagram

class DiagramService:

    def draw_diagram(self, diagram: Diagram, container_id: str):
        """
        Draws the given diagram and adds it to the DOM
        """
        asyncio.create_task(self.__render_graphviz_to_html(str(diagram.to_graphviz()), container_id))

    async def __render_graphviz_to_html(self, graphviz_source: str, container_id: str):
        viz = await window.Viz.instance()
        svg_element = viz.renderSVGElement(graphviz_source)
        container = document.getElementById(container_id)
        container.innerHTML = ""
        container.append(svg_element)