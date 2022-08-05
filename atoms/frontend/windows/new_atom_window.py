# new_atom_window.py
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

from gi.repository import Gtk, GObject, Adw

from atoms.backend.utils.distribution import AtomsDistributionsUtils
from atoms.backend.entities.atom import Atom

from atoms.frontend.widgets.creation_step_entry import CreationStepEntry
from atoms.frontend.utils.threading import RunAsync
from atoms.frontend.utils.gtk import GtkUtils


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/new-atom-window.ui')
class AtomsNewAtomWindow(Adw.Window):
    __gtype_name__ = 'AtomsNewAtomWindow'
    __distributions_registry = []

    btn_cancel_creation = Gtk.Template.Child()
    btn_cancel = Gtk.Template.Child()
    btn_create = Gtk.Template.Child()
    btn_finish = Gtk.Template.Child()
    entry_name = Gtk.Template.Child()
    combo_distribution = Gtk.Template.Child()
    combo_releases = Gtk.Template.Child()
    str_list_distributions = Gtk.Template.Child()
    str_list_releases = Gtk.Template.Child()
    group_steps = Gtk.Template.Child()
    stack_main = Gtk.Template.Child()
    header_bar = Gtk.Template.Child()
    status_error = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)
        self.window = window
        self.__build_ui()
    
    def __build_ui(self):
        for distribution in AtomsDistributionsUtils.get_distributions():
            self.__distributions_registry.append(distribution)
            self.str_list_distributions.append(distribution.name)
        
        self.combo_distribution.set_selected(0)
        self.__on_combo_distribution_changed()

        self.step_download = CreationStepEntry("Downloading Choosen Image…")
        self.step_configuration = CreationStepEntry("Creating new Atom Configuration…")
        self.step_unpack = CreationStepEntry("Unpacking Choosen Image…")
        self.step_finalizing = CreationStepEntry("Finalizing…")

        self.group_steps.add(self.step_download)
        self.group_steps.add(self.step_configuration)
        self.group_steps.add(self.step_unpack)
        self.group_steps.add(self.step_finalizing)

        self.entry_name.connect('changed', self.__check_entry_name)
        self.btn_cancel.connect('clicked', self.__on_btn_cancel_clicked)
        self.btn_create.connect('clicked', self.__on_btn_create_clicked)
        self.btn_cancel_creation.connect('clicked', self.__on_btn_cancel_creation_clicked)
        self.btn_finish.connect('clicked', self.__on_btn_finish_clicked)
        self.combo_distribution.connect('notify::selected', self.__on_combo_distribution_changed)
    
    def __show_error(self, error):
        self.status_error.set_description(error)
        self.stack_main.set_visible_child_name("error")
        self.set_deletable(True)
    
    def __on_btn_create_clicked(self, widget):
        def create_atom() -> 'Atom':
            distro = self.__distributions_registry[self.combo_distribution.get_selected()]
            return Atom.new(
                self.window.manager.config,
                self.entry_name.get_text(),
                distro,
                distro.architectures["x86_64"],
                distro.releases[self.combo_releases.get_selected()],
                self.step_download.update_download,
                self.step_configuration.update_status,
                self.step_unpack.update_status,
                self.step_finalizing.update_status,
                self.__show_error,
            )

        self.set_size_request(450, 505)
        self.stack_main.set_visible_child_name("creation")
        self.btn_cancel_creation.set_visible(True)
        self.btn_cancel.set_visible(False)
        self.btn_create.set_visible(False)
        self.header_bar.add_css_class("flat")

        RunAsync(create_atom, self.__finish_creation)

    def __check_entry_name(self, *_args):
        result = GtkUtils.validate_entry(self.entry_name)
        self.btn_create.set_sensitive(result)
    
    def __on_btn_finish_clicked(self, widget):
        self.close()
    
    def __on_btn_cancel_creation_clicked(self, widget):
        self.close()
    
    def __finish_creation(self, atom: 'Atom', error=False):
        self.window.insert_atom(atom)
        self.stack_main.set_visible_child_name("created")
    
    def __on_combo_distribution_changed(self, *args):
        self.str_list_releases.splice(0, len(self.str_list_releases))
        distribution = self.__distributions_registry[self.combo_distribution.get_selected()]
        
        for release in distribution.releases:
            self.str_list_releases.append(release)
        self.combo_releases.set_selected(0)

    def __on_btn_cancel_clicked(self, widget):
        self.destroy()
