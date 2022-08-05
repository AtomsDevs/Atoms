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
    toasts = Gtk.Template.Child()
    manager = AtomsBackend()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__build_ui()
    
    def __build_ui(self):
        self.atoms_list = AtomsList(self)
        self.stack_main.add_named(self.atoms_list, 'list-atoms')
        self.stack_main.add_named(AtomsStatusEmpty(self), 'no-atoms')

        if self.manager.has_atoms:
            self.stack_main.set_visible_child_name('list-atoms')
        else:
            self.stack_main.set_visible_child_name('no-atoms')

        self.btn_new.connect('clicked', self.on_btn_new_clicked)
    
    def show_atoms_list(self):
        self.main_leaflet.set_visible_child(self.box_main)

    def on_btn_new_clicked(self, widget):
        new_atom_window = AtomsNewAtomWindow(self)
        new_atom_window.present()
    
    def insert_atom(self, atom: 'Atom'):
        self.atoms_list.insert_atom(atom)
        self.stack_main.set_visible_child_name('list-atoms')
    
    def remove_atom(self, atom: 'Atom'):
        self.atoms_list.remove_atom(atom)
        if not self.atoms_list.has_atoms:
            self.stack_main.set_visible_child_name('no-atoms')

    def show_toast(self, message: str, timeout: int=3):
        toast = Adw.Toast.new(message)
        toast.props.timeout = timeout
        self.toasts.add_toast(toast)
