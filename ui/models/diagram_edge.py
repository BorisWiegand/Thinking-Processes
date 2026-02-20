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

from pyscript import document

class DiagramEdge:
    
    def __init__(self, svg_node_id: str):
        self.__svg_node_id = svg_node_id
        self.__original_edge_color = self.__get_svg_polygon().getAttribute("stroke")
        self.from_node_ids, self.to_node_ids = (
            self.__get_svg_node().getElementsByTagName('title')[0].textContent.split("->")
        )
        self.from_node_ids = list(map(int,self.from_node_ids.split(",")))
        self.to_node_ids = list(map(int,self.to_node_ids.split(",")))

    def mark_as_selected(self):
        self.__get_svg_polygon().setAttribute("stroke", "lightblue")
        self.__get_svg_polygon().setAttribute("fill", "lightblue")
        self.__get_svg_path().setAttribute("stroke", "lightblue")

    def reset_marking(self):
        self.__get_svg_polygon().setAttribute("stroke", self.__original_edge_color)
        self.__get_svg_polygon().setAttribute("fill", self.__original_edge_color)
        self.__get_svg_path().setAttribute("stroke", self.__original_edge_color)

    def __get_svg_node(self):
        return document.getElementById(self.__svg_node_id)
    
    def __get_svg_polygon(self):
        return self.__get_svg_node().getElementsByTagName('polygon')[0]
    
    def __get_svg_path(self):
        return self.__get_svg_node().getElementsByTagName('path')[0]
    
    def __eq__(self, other):
        return (
            isinstance(other, DiagramEdge) 
            and self.from_node_ids == other.from_node_ids
            and self.to_node_ids == other.to_node_ids
        )
    