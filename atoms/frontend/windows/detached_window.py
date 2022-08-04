# window.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk, GObject, Adw


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/detached-window.ui')
class AtomsDetachedWindow(Adw.Window):
    __gtype_name__ = 'AtomsDetachedWindow'
    __gsignals__ = {
        "widget-released": (GObject.SIGNAL_RUN_FIRST, None, (bool,))
    }

    box_content = Gtk.Template.Child()

    def __init__(self, widget, bg_color: str = None, dark: bool = True, title: str = None, **kwargs):
        super().__init__(**kwargs)
        self.__widget = widget
        self.__bg_color = bg_color
        self.__dark = dark
        self.__title = title
        self.__build_ui()
    
    def __build_ui(self):
        if self.__bg_color is not None:
            style = ".tinted_window{background-color: %s;}" % self.__bg_color
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(str.encode(style))
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(), css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            self.add_css_class('tinted_window')
        
        if self.__dark:
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        
        if self.__title:
            self.set_title(self.__title)

        self.box_content.append(self.__widget)
    
    def release_widget(self):
        self.box_content.remove(self.__widget)
