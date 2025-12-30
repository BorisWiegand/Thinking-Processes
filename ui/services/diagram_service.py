import asyncio
from pyscript import window, document

from thinking_processes.diagram import Diagram
from ui.models.diagram_node import DiagramNode

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