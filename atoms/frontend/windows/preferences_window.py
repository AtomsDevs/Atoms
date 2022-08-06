# preferences_window.py
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

from atoms.frontend.widgets.image_entry import ImageEntry


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/preferences-window.ui')
class AtomsPreferences(Adw.PreferencesWindow):
    __gtype_name__ = 'AtomsPreferences'

    switch_update_date = Gtk.Template.Child()
    row_atoms_path = Gtk.Template.Child()
    row_images_path = Gtk.Template.Child()
    btn_atoms_path_reset = Gtk.Template.Child()
    btn_images_path_reset = Gtk.Template.Child()
    group_images = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.__build_ui()
        import random
        self.test = random.randint(0, 100)
    
    def __build_ui(self):
        self.set_transient_for(self.window)

        for image in self.window.manager.local_images:
            self.group_images.add(ImageEntry(image))

        self.switch_update_date.set_active(self.window.settings.get_boolean("update-date"))

        self.switch_update_date.connect('state-set', self.__on_switch_update_date_state_set)
        self.btn_atoms_path_reset.connect('clicked', self.__on_btn_atoms_path_reset_clicked)
        self.btn_images_path_reset.connect('clicked', self.__on_btn_images_path_reset_clicked)
        self.row_atoms_path.connect('activate', self.__on_row_atoms_path_activate)
        self.row_images_path.connect('activate', self.__on_row_images_path_activate)

    def __on_switch_update_date_state_set(self, switch, state):
        # NOTE: not using bind() because it doesn't work as expected
        #       it keep multiple bindings instead of replacing them        
        #       making a new AtomsPreferences object instance, resulting
        #       in multiple updates to the settings. I also tried to unbind
        #       the old binding, but it didn't work.
        self.window.settings.set_boolean("update-date", state)
        self.window.reload_atoms()

    def __on_btn_atoms_path_reset_clicked(self, button):
        self.window.manager.config.restore_default("atoms.path")
        self.window.show_toast("Atoms path reset to default.")

    def __on_btn_images_path_reset_clicked(self, button):
        self.window.manager.config.restore_default("images.path")
        self.window.show_toast("Images path reset to default.")

    def __on_row_atoms_path_activate(self, row):
        pass

    def __on_row_images_path_activate(self, row):
        pass
