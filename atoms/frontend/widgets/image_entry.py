# creation_step_entry.py
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


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/entry-image.ui')
class ImageEntry(Adw.ActionRow):
    __gtype_name__ = 'ImageEntry'

    def __init__(self, image:'AtomsImage', **kwargs):
        super().__init__()
        self.image = image
        self.__build_ui()

    def __build_ui(self):
        self.set_title(self.image.name)
        self.set_subtitle(self.image.human_size)
