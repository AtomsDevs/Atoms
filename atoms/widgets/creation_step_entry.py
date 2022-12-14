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


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/entry-creation-step.ui')
class CreationStepEntry(Adw.ActionRow):
    __gtype_name__ = 'CreationStepEntry'

    img_completed = Gtk.Template.Child()
    label_percentage = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, title: str, update_func: callable = None):
        super().__init__()
        self.__title = title
        self.__update_func = update_func
        self.__build_ui()

    def __build_ui(self):
        self.set_title(self.__title)
    
    def update_download(self, count, block_size, total_size):
        self.label_percentage.set_visible(True)

        percent = int(count * block_size * 100 / total_size)
        self.label_percentage.set_text(f'{str(percent)}%')

        if percent == 100:
            self.label_percentage.set_visible(False)
            self.img_completed.set_visible(True)
    
    def update_status(self, status: int):
        if status == 0:
            self.spinner.set_visible(True)
            self.spinner.start()
        else:
            self.spinner.set_visible(False)
            self.spinner.stop()
            self.img_completed.set_visible(True)
