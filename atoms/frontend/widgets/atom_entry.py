# atom_entry.py
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

from atoms.frontend.views.dashboard import AtomDashboard


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/entry-atom.ui')
class AtomEntry(Adw.ActionRow):
    __gtype_name__ = 'AtomEntry'

    btn_open = Gtk.Template.Child()
    img_distribution = Gtk.Template.Child()

    def __init__(self, window, atom: "Atom"):
        super().__init__()
        self.window = window
        self.atom = atom
        self.dashboard = AtomDashboard(window, atom)
        self.__build_ui()

    def __build_ui(self):
        self.set_title(self.atom.name)
        self.img_distribution.set_from_icon_name(self.atom.distribution.logo)
        self.window.main_leaflet.append(self.dashboard)
        
        self.btn_open.connect('clicked', self.__on_open_clicked)

    def __on_open_clicked(self, widget):
        self.window.main_leaflet.set_visible_child(self.dashboard)
    
    def destroy(self):
        self.get_parent().remove(self)
