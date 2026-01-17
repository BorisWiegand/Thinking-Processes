import asyncio
import re
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

    def download_diagram_as_png(self, diagram: Diagram):
        """
        Draws and downloads the given diagram as png
        """
        asyncio.create_task(
            self.__download_diagram(diagram, 'png')
        )

    async def __download_diagram(self, graphviz_source: str, format: str):
        viz = await window.Viz.instance()
        # svg = viz.render(graphviz_source, format='svg').output

        # svg = svg.strip()

        # if not svg.startswith("<svg"):
        #     svg = svg[svg.find("<svg"):]

        # def pt_to_px(match):
        #     value = float(match.group(1))
        #     return f'{int(value * 4 / 3)}'

        # svg = re.sub(r'width="([\d.]+)pt"', lambda m: f'width="{pt_to_px(m)}"', svg)
        # svg = re.sub(r'height="([\d.]+)pt"', lambda m: f'height="{pt_to_px(m)}"', svg)   
        # 

        svg = """
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
        <rect width="100" height="100" fill="red"/>
        </svg>
        """.strip()     

        svg_url = window.URL.createObjectURL(window.Blob.new([svg], {type: 'image/svg+xml'}))
        window.open(svg_url, "_blank")

        img = window.Image.new()

        def onload(_):
            # 4. Draw to canvas
            canvas = document.createElement("canvas")
            canvas.width = img.width
            canvas.height = img.height

            ctx = canvas.getContext("2d")
            ctx.drawImage(img, 0, 0)

            # 5. Convert canvas to PNG
            png_url = canvas.toDataURL("image/png")

            link = document.createElement("a")
            link.href = png_url
            link.download = "diagram.png"
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            window.URL.revokeObjectURL(svg_url)

        def onerror(e):
            print("Image failed to load", e)
            window.console.log(e)

        img.onload = onload
        img.onerror = onerror
        img.src = svg_url

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