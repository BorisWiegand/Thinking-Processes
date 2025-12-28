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

from ui.app import app

from puepy import Page, t

from ui.pages.crt_page import CrtPage

@app.page()
class Home(Page):
    def initial(self):
        return dict(name="")

    def populate(self):
        with t.div(classes=["container", "mx-auto", "p-4"]):
            t.h1("Thinking Processes", classes=["text-2xl", "pb-4"])
            t.p("What kind of diagram do you want to draw?", classes=["pb-4"])
            with t.div(classes=["grid grid-cols-1", "md:grid-cols-2", "gap-4"]):
                self.__draw_thinking_process_navigation_card(
                    "Current Reality Tree",
                    "../crt.png",
                    "Find root causes of observed undesired effects.",
                    CrtPage
                )
                self.__draw_thinking_process_navigation_card(
                    "Future Reality Tree",
                    "../frt.png",
                    "Identify necessary injections that cause a set of desirable effects.",
                    CrtPage
                )
                self.__draw_thinking_process_navigation_card(
                    "Prerequisite Tree",
                    "../prt.png",
                    "Overcome obstacles in order to achieve a desirable effect or goal.",
                    CrtPage
                )
                self.__draw_thinking_process_navigation_card(
                    "Evaporating Cloud",
                    "../ec.png",
                    "Draw a conflict resolution diagram.",
                    CrtPage
                )

    def __draw_thinking_process_navigation_card(
            self, title: str, example_image_path: str,
            description: str, target_page: Page):
        with t.sl_card(classes=["thinking-process-navigation-card"]):
            with t.div(slot="header"):
                t.sl_text(title, classes=["text-lg"])
            t.img(
                src=example_image_path,
                alt=f"example of a {title}"
            )
            t.p(description)
            with t.div(slot='footer'):
                t.sl_button(
                    "Start", variant="primary", classes=["w-full"],
                    on_click=lambda e: self.router.navigate_to_path(self.router.reverse(target_page))
                )