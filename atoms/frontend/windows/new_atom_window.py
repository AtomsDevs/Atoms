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

from gi.repository import Gtk, GObject, Adw


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/new-atom-window.ui')
class AtomsNewAtomWindow(Adw.Window):
    __gtype_name__ = 'AtomsNewAtomWindow'

    btn_cancel = Gtk.Template.Child()
    btn_create = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)
        self.__build_ui()
    
    def __build_ui(self):
        self.btn_cancel.connect('clicked', self.__on_btn_cancel_clicked)

    def __on_btn_cancel_clicked(self, widget):
        self.destroy()
