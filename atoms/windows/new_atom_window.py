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

from atoms_core.utils.distribution import AtomsDistributionsUtils
from atoms_core.entities.atom import Atom
from atoms_core.entities.atom_type import AtomType

from atoms.widgets.creation_step_entry import CreationStepEntry
from atoms.utils.threading import RunAsync
from atoms.utils.gtk import GtkUtils


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/new-atom-window.ui')
class AtomsNewAtomWindow(Adw.Window):
    __gtype_name__ = 'AtomsNewAtomWindow'
    __distributions_registry = []
    
    """
    Atom types:
        - 0: Atom Chroot
        - 1: Podman Container
    """

    btn_cancel_creation = Gtk.Template.Child()
    btn_cancel = Gtk.Template.Child()
    btn_create = Gtk.Template.Child()
    btn_finish = Gtk.Template.Child()
    entry_name = Gtk.Template.Child()
    entry_podman_image = Gtk.Template.Child()
    combo_distribution = Gtk.Template.Child()
    combo_releases = Gtk.Template.Child()
    combo_atom_type = Gtk.Template.Child()
    str_list_distributions = Gtk.Template.Child()
    str_list_releases = Gtk.Template.Child()
    stack_main = Gtk.Template.Child()
    header_bar = Gtk.Template.Child()
    status_error = Gtk.Template.Child()
    group_atom_chroot = Gtk.Template.Child()
    group_podman_container = Gtk.Template.Child()
    group_steps = Gtk.Template.Child()

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
        self.step_podman = CreationStepEntry("Creating new Podman Container…")
        self.step_finalizing = CreationStepEntry("Finalizing…")

        self.group_steps.add(self.step_download)
        self.group_steps.add(self.step_configuration)
        self.group_steps.add(self.step_unpack)
        self.group_steps.add(self.step_podman)
        self.group_steps.add(self.step_finalizing)

        self.__toggle_steps()

        self.entry_name.connect('changed', self.__check_entry_value)
        self.entry_podman_image.connect('changed', self.__check_entry_value)
        self.btn_cancel.connect('clicked', self.__on_btn_cancel_clicked)
        self.btn_create.connect('clicked', self.__on_btn_create_clicked)
        self.btn_cancel_creation.connect('clicked', self.__on_btn_cancel_creation_clicked)
        self.btn_finish.connect('clicked', self.__on_btn_finish_clicked)
        self.combo_atom_type.connect('notify::selected', self.__on_combo_atom_type_changed)
        self.combo_distribution.connect('notify::selected', self.__on_combo_distribution_changed)
    
    def __toggle_steps(self):
        is_chroot = self.atom_type == AtomType.ATOM_CHROOT
        is_container = self.atom_type == AtomType.PODMAN_CONTAINER

        self.step_download.set_visible(is_chroot)
        self.step_configuration.set_visible(is_chroot)
        self.step_unpack.set_visible(is_chroot)
        self.step_podman.set_visible(is_container)
        self.step_finalizing.set_visible(is_chroot)
    
    def __show_error(self, error):
        self.status_error.set_description(error)
        self.stack_main.set_visible_child_name("error")
        self.set_deletable(True)
    
    def __on_btn_create_clicked(self, widget):
        def create_atom() -> 'Atom':
            nonlocal self
            distro = self.__distributions_registry[self.combo_distribution.get_selected()]
            if self.atom_type == AtomType.ATOM_CHROOT:
                return self.window.manager.request_new_atom(
                    name=self.entry_name.get_text(),
                    atom_type=self.atom_type,
                    distribution=distro,
                    architecture=distro.architectures["x86_64"],
                    release=distro.releases[self.combo_releases.get_selected()],
                    download_fn=self.step_download.update_download,
                    config_fn=self.step_configuration.update_status,
                    unpack_fn=self.step_unpack.update_status,
                    finalizing_fn=self.step_finalizing.update_status,
                    error_fn=self.__show_error
                )
            elif self.atom_type == AtomType.PODMAN_CONTAINER:
                return self.window.manager.request_new_atom(
                    name=self.entry_name.get_text(),
                    atom_type=self.atom_type,
                    podman_container_image=self.entry_podman_image.get_text(),
                    podman_fn=self.step_podman.update_status,
                    finalizing_fn=self.step_finalizing.update_status,
                    error_fn=self.__show_error
                )

        self.set_size_request(450, 505)
        self.stack_main.set_visible_child_name("creation")
        self.btn_cancel_creation.set_visible(True)
        self.btn_cancel.set_visible(False)
        self.btn_create.set_visible(False)
        self.header_bar.add_css_class("flat")

        RunAsync(create_atom, self.__finish_creation)

    def __check_entry_value(self, widget, *_args):
        result = GtkUtils.validate_entry(widget)
        self.btn_create.set_sensitive(result)
    
    def __on_btn_finish_clicked(self, widget):
        self.close()
    
    def __on_btn_cancel_creation_clicked(self, widget):
        self.close()
    
    def __finish_creation(self, atom: 'Atom', error=False):
        if atom is None:
            return
        self.window.insert_atom(atom)
        self.stack_main.set_visible_child_name("created")

    def __on_combo_atom_type_changed(self, widget, _param):
        self.group_atom_chroot.set_visible(self.atom_type == AtomType.ATOM_CHROOT)
        self.group_podman_container.set_visible(self.atom_type == AtomType.PODMAN_CONTAINER)
        self.__toggle_steps()
    
    def __on_combo_distribution_changed(self, *args):
        self.str_list_releases.splice(0, len(self.str_list_releases))
        distribution = self.__distributions_registry[self.combo_distribution.get_selected()]
        
        for release in distribution.releases:
            self.str_list_releases.append(release)
        self.combo_releases.set_selected(0)

    def __on_btn_cancel_clicked(self, widget):
        self.destroy()
    
    @property
    def atom_type(self):
        return AtomType(self.combo_atom_type.get_selected())
