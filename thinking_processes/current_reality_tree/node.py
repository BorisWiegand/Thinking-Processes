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

class Node:
    """
    node of a current reality tree 
    """
    def __init__(self, id: int, text: str):
        self.__id = id
        self.__text = text

    @property
    def id(self) -> int:
        """
        id of this node
        """
        return self.__id
    
    @property
    def text(self) -> str:
        """
        text of this node
        """
        return self.__text
    
    @text.setter
    def text(self, new_text: str):
        """
        sets the text of this node to new_text

        Args:
            new_text (str): 
                new text of this node
        """
        self.__text = new_text

    def __str__(self) -> str:
        return f'{self.__id}: {self.__text}'
    
    def __eq__(self, value: object) -> bool:
        return isinstance(value, Node) and self.__id == value.id
    
    def __hash__(self) -> int:
        return hash(self.__id)