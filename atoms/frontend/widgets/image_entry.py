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

from gi.repository import Gtk, Adw
from atoms.frontend.utils.threading import RunAsync


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/entry-image.ui')
class ImageEntry(Adw.ActionRow):
    __gtype_name__ = 'ImageEntry'

    def __init__(self, window, image:'AtomsImage', **kwargs):
        super().__init__()
        self.window = window
        self.image = image
        self.__build_ui()

    def __build_ui(self):
        self.set_title(self.image.name)
        self.set_subtitle(self.image.human_size)

        self.connect('activated', self.__on_activated)

    def __on_activated(self, widget):
        def on_destroy_done(*args):
            self.get_parent().remove(self)

        def handle_response(_widget, response_id):
            if response_id == "ok":
                RunAsync(self.image.destroy, on_destroy_done)

        dialog = Adw.MessageDialog.new(
            self.window,
            _("Confirm"),
            _("Are you sure you want to delete this image?"),
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("ok", _("Confirm"))
        dialog.connect("response", handle_response)
        dialog.present()
