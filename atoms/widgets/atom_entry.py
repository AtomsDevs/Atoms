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

from gi.repository import Gtk, Adw

from atoms.views.dashboard import AtomDashboard


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/entry-atom.ui')
class AtomEntry(Adw.ActionRow):
    __gtype_name__ = 'AtomEntry'

    img_distribution = Gtk.Template.Child()

    def __init__(self, window, atom: "Atom"):
        super().__init__()
        self.window = window
        self.atom = atom
        self.__loaded = False
        self.dashboard = AtomDashboard(window, atom)
        self.__build_ui()

    def __build_ui(self):
        if self.atom.is_distrobox_container:
            self.set_title(f"{self.atom.name} (distrobox)")
            self.set_subtitle(self.atom.container_image)
        else:
            self.set_title(self.atom.name)
            if self.window.settings.get_boolean("update-date"):
                self.set_subtitle(self.atom.formatted_update_date)
            else:
                self.set_subtitle("")

        if self.__loaded:
            return

        self.img_distribution.set_from_icon_name(self.atom.distribution.logo)
        self.window.main_leaflet.append(self.dashboard)
        self.__loaded = True
        self.connect('activated', self.__on_activated)

    def __on_activated(self, widget):
        self.window.main_leaflet.set_visible_child(self.dashboard)
        self.dashboard.restore_color_scheme()
    
    def destroy(self):
        self.get_parent().remove(self)
    
    def reload_ui(self):
        self.__build_ui()
