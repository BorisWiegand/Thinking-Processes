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
import json
import os
from tempfile import TemporaryDirectory

from graphviz import Graph
import drawpyo

class Diagram(ABC):
    """
    base class for all thinking process diagrams. 
    defines basic methods for plotting and exporting diagrams.
    """

    def plot(self, view: bool = True, filepath: str|None = None):
        """
        plots this diagram using graphviz

        Args:
            view (bool, optional): 
                set to False if you do not want to immediately view the diagram. Defaults to True.
            filepath (str | None, optional): 
                path to the file for saving the plot, e.g. 'diagram.pdf' or 'diagram.png'. 
                Defaults to None, which means the diagram will not be saved into a file.
        """
        #we do not want to see the generated .dot code 
        # => write it to a temporary file
        with TemporaryDirectory(delete=not view or filepath is not None) as tempdir:
            self.to_graphviz().render(filename=os.path.join(tempdir, 'diagram.gv'), view=view, outfile=filepath)

    def __get_layouted_graphviz_json(self) -> dict:
        with TemporaryDirectory() as tempdir:
            with open(self.to_graphviz().render(
                filename=os.path.join(tempdir, 'diagram.gv'), 
                outfile=os.path.join(tempdir, 'diagram.json'),
                view=False
            )) as dot_file:
                return json.load(dot_file)

    def save_as_drawio(self, filepath: str):
        dirname, filename = os.path.split(os.path.abspath(filepath))
        graph = self.__get_layouted_graphviz_json()
        file = drawpyo.File(file_name=filename, file_path=dirname)
        page = drawpyo.Page(file=file)
        nodes_by_id = {}
        for o in graph['objects']:
            if not o['name'].startswith('cluster'):
                x,y = (float(x) for x in o['pos'].split(','))
                nodes_by_id[o['_gvid']] = drawpyo.diagram.Object(
                    value=o['label'], 
                    page=page,
                    position=(x,-y),
                    fillColor=o.get('fillcolor', 'white'),
                    rounded='rounded' in o.get('style', ''),
                    width=int(round(float(o['width']) * 72)),
                    height=int(round(float(o['height']) * 72))
                )
            else:
                x1,y1,x2,y2 = tuple(int(round(float(x))) for x in o['bb'].split(','))
                drawpyo.diagram.Object(
                    page=page,
                    rounded='rounded' in o.get('style', ''),
                    position=(x1,-y1),
                    width=abs(x2-x1),
                    height=abs(y2-y1),
                )
        for edge in graph['edges']:
            drawpyo.diagram.Edge(
                source=nodes_by_id[edge['tail']], 
                target=nodes_by_id[edge['head']], 
                page=page,
                line_end_target=edge.get('arrowhead', None),
            )
        file.write()

    @abstractmethod
    def to_graphviz(self) -> Graph:
        """
        creates a graphviz Graph of this diagram

        Returns:
            Graph: a graphviz Graph of this diagram
        """