# atoms.py
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

from atoms.widgets.atom_entry import AtomEntry


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/list-atoms.ui')
class AtomsList(Gtk.ScrolledWindow):
    __gtype_name__ = 'AtomsList'
    __registry = {}
    
    list_atoms = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.__build_ui()

    def __build_ui(self):
        for atom in self.window.manager.atoms.values():
            self.insert_atom(atom)
    
    def insert_atom(self, atom: 'Atom'):
        key = self.__get_registry_key(atom)
        entry = AtomEntry(self.window, atom)
        self.__registry[key] = entry
        self.list_atoms.append(entry)

    def remove_atom(self, atom: 'Atom'):
        key = self.__get_registry_key(atom)
        entry = self.__registry[key]
        self.list_atoms.remove(entry)
        del self.__registry[key]
    
    def __get_registry_key(self, atom: 'Atom') -> str:
        if atom.is_distrobox_container:
            key = atom.container_id
        else:
            key = atom.relative_path

        return key
    
    def reload(self):
        for atom in self.__registry.values():
            atom.reload_ui()
        
    def clear(self):
        temp_registry = self.__registry.copy()
        for atom in temp_registry.values():
            self.remove_atom(atom)

        self.__registry.clear()

    @property
    def has_atoms(self) -> bool:
        return len(self.__registry) > 0