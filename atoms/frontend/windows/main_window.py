# main_window.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Adw

from atoms.frontend.views.status.no_atoms import AtomsStatusEmpty
from atoms.frontend.views.lists.atoms import AtomsList
from atoms.frontend.windows.new_atom_window import AtomsNewAtomWindow

from atoms.backend.atoms import AtomsBackend


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/window.ui')
class AtomsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'AtomsWindow'

    main_leaflet = Gtk.Template.Child()
    stack_main = Gtk.Template.Child()
    btn_new = Gtk.Template.Child()
    box_main = Gtk.Template.Child()
    manager = AtomsBackend()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__build_ui()
    
    def __build_ui(self):
        if self.manager.has_atoms:
            self.stack_main.add_named(AtomsList(self), 'list-atoms')
        else:
            self.stack_main.add_named(AtomsStatusEmpty(), 'no-atoms')

        self.btn_new.connect('clicked', self.__on_btn_new_clicked)
    
    def show_atoms_list(self):
        self.main_leaflet.set_visible_child(self.box_main)

    def __on_btn_new_clicked(self, widget):
        new_atom_window = AtomsNewAtomWindow(self)
        new_atom_window.present()
