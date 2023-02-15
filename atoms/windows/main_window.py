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

from gi.repository import Gtk, Gio, Adw

from atoms.views.status.no_atoms import AtomsStatusEmpty
from atoms.views.lists.atoms import AtomsList
from atoms.windows.new_atom_window import AtomsNewAtomWindow
from atoms.utils.client_bridge import GTKClientBridge
from atoms.const import *

from atoms_core.atoms import AtomsBackend


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/window.ui')
class AtomsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'AtomsWindow'

    main_leaflet = Gtk.Template.Child()
    stack_main = Gtk.Template.Child()
    btn_new = Gtk.Template.Child()
    box_main = Gtk.Template.Child()
    toasts = Gtk.Template.Child()
    settings = Gio.Settings.new(APP_ID)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__loaded = False
        self.manager = AtomsBackend(
            distrobox_support=self.settings.get_boolean('distrobox-integration'),
            client_bridge=GTKClientBridge()
        )
        self.__build_ui()

        new_action = Gio.SimpleAction(name="new_atom")
        new_action.connect("activate", self.on_btn_new_clicked)
        self.add_action(new_action)
    
    def __build_ui(self):
        self.atoms_list = AtomsList(self)
        self.atoms_empty = AtomsStatusEmpty(self)

        self.stack_main.add_named(self.atoms_list, 'list-atoms')
        self.stack_main.add_named(self.atoms_empty, 'no-atoms')

        if self.manager.has_atoms:
            self.stack_main.set_visible_child_name('list-atoms')
        else:
            self.stack_main.set_visible_child_name('no-atoms')

        if self.__loaded:
            return
            
        if BUILD_TYPE == "devel":
            self.add_css_class('devel')
            
        self.__loaded = True
    
    def show_atoms_list(self):
        self.main_leaflet.set_visible_child(self.box_main)

    def on_btn_new_clicked(self, widget, *args):
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
    
    def reload_atoms(self):
        self.atoms_list.reload()

    def re_init_manager(self):
        self.manager = AtomsBackend(
            distrobox_support=self.settings.get_boolean('distrobox-integration'),
            client_bridge=GTKClientBridge()
        )
        self.atoms_list.clear()
        self.stack_main.remove(self.atoms_list)
        self.stack_main.remove(self.atoms_empty)
        self.__build_ui()
        
