# dashboard.py
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

from gi.repository import Gtk, Gdk, Gio, Adw

from atoms.views.status.detached_console import AtomsStatusDetachedConsole
from atoms.windows.detached_window import AtomsDetachedWindow
from atoms.views.console import AtomsConsole
from atoms.utils.threading import RunAsync
from atoms.utils.gtk import GtkUtils


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/dashboard.ui')
class AtomDashboard(Adw.Bin):
    __gtype_name__ = 'AtomDashboard'

    btn_back = Gtk.Template.Child()
    btn_detach = Gtk.Template.Child()
    btn_start = Gtk.Template.Child()
    stack_atom = Gtk.Template.Child()
    stack_console = Gtk.Template.Child()
    box_console = Gtk.Template.Child()
    img_distribution = Gtk.Template.Child()
    label_name = Gtk.Template.Child()
    label_distribution = Gtk.Template.Child()
    entry_name = Gtk.Template.Child()
    row_browse = Gtk.Template.Child()
    row_destroy = Gtk.Template.Child()
    row_details = Gtk.Template.Child()
    row_bindings = Gtk.Template.Child()
    switch_bind_themes = Gtk.Template.Child()
    switch_bind_icons = Gtk.Template.Child()
    switch_bind_fonts = Gtk.Template.Child()
    group_utilities = Gtk.Template.Child()
    pref_page = Gtk.Template.Child()

    def __init__(self, window, atom: 'Atom', **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.atom = atom
        self.__detach_status = False
        self.__detached_window = None
        self.__current_color_scheme = Adw.ColorScheme.DEFAULT
        self.__is_container_running = False
        self.__build_ui()
    
    def __build_ui(self):
        self.console = AtomsConsole(self.atom)
        self.label_name.set_text(self.atom.name)
        self.entry_name.set_text(self.atom.name)
        self.label_distribution.set_text(self.atom.distribution.name)
        self.img_distribution.set_from_icon_name(self.atom.distribution.logo)
        self.stack_console.add_named(AtomsStatusDetachedConsole(), 'status')
        self.box_console.append(self.console)
        self.switch_bind_themes.set_state(self.atom.bind_themes)
        self.switch_bind_icons.set_state(self.atom.bind_icons)
        self.switch_bind_fonts.set_state(self.atom.bind_fonts)

        self.row_destroy.connect('activated', self.__on_destroy_activated)
        self.row_browse.connect('activated', self.__on_browse_activated)
        self.btn_back.connect('clicked', self.__on_back_clicked)
        self.btn_detach.connect('clicked', self.__on_detach_clicked)
        self.btn_start.connect('clicked', self.__on_start_clicked)
        self.entry_name.connect('changed', self.__on_entry_changed)
        self.entry_name.connect('apply', self.__on_entry_apply)
        self.stack_atom.connect('notify::visible-child', self.__on_visible_child_changed)
        self.switch_bind_themes.connect('state-set', self.__on_switch_bind_themes)
        self.switch_bind_icons.connect('state-set', self.__on_switch_bind_icons)
        self.switch_bind_fonts.connect('state-set', self.__on_switch_bind_fonts)

        if self.atom.is_distrobox_container:
            self.group_utilities.set_visible(False)
            self.row_details.set_visible(False)
            self.row_bindings.set_visible(False)
        if self.atom.is_system_shell:
            self.pref_page.set_visible(False)

    def __on_back_clicked(self, widget):
        self.window.show_atoms_list()
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)
    
    def __on_start_clicked(self, widget):
        if self.__is_container_running:
            self.console.set_stop_status()
            self.atom.stop_distrobox_container()
            self.btn_start.set_icon_name('media-playback-start-symbolic')
        else:
            self.console.run_command(*self.atom.enter_command)
            self.btn_start.set_icon_name('media-playback-stop-symbolic')
        self.__is_container_running = not self.__is_container_running

    def __on_detach_clicked(self, widget):
        def attach(*args):
            if self.__detached_window:
                self.__detached_window.release_widget()
                self.__detached_window.close()
                self.__detached_window = None
            self.btn_detach.set_tooltip_text('Detach Console')
            self.btn_detach.set_icon_name('pip-in-symbolic')
            self.stack_console.set_visible_child_name('vte')
            self.box_console.append(self.console)
            self.window.show_toast("Atom console re-attached.")
            self.__detach_status = False
            
        def detach():
            self.btn_detach.set_tooltip_text('Attach Console')
            self.btn_detach.set_icon_name('pip-out-symbolic')
            self.stack_console.set_visible_child_name('status')
            self.box_console.remove(self.console)
            if not self.__detached_window:
                self.__detached_window = AtomsDetachedWindow(self.console, "#000000", title=self.atom.name)
                self.__detached_window.present()
                self.__detached_window.connect("close-request", attach)
            self.window.show_toast("Atom console detached.")
            self.__detach_status = True
            
        attach() if self.__detach_status else detach()

    def __on_visible_child_changed(self, *args):
        is_console = self.stack_atom.get_visible_child_name() == 'console'

        self.btn_detach.set_visible(is_console)
        if self.atom.is_distrobox_container:
            self.btn_start.set_visible(is_console)

        if is_console:
            self.__current_color_scheme = Adw.ColorScheme.FORCE_DARK
        else:
            self.__current_color_scheme = Adw.ColorScheme.DEFAULT

        Adw.StyleManager.get_default().set_color_scheme(self.__current_color_scheme)

    def __on_browse_activated(self, widget):
        Gtk.show_uri(self.window, f"file://{self.atom.fs_path}", Gdk.CURRENT_TIME)
        self.window.show_toast("File manager opened.")

    def __on_destroy_activated(self, widget):
        def on_destroy_done(*args):
            self.window.remove_atom(self.atom)
            self.window.show_atoms_list()

        def handle_response(_widget, response_id):
            if response_id == "ok":
                RunAsync(self.atom.destroy, on_destroy_done)
            _widget.destroy()

        dialog = Adw.MessageDialog.new(
            self.window,
            _("Confirm"),
            _("Are you sure you want to delete this Atom and all files?")
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("ok", _("Confirm"))
        dialog.connect("response", handle_response)
        dialog.present()
    
    def __on_entry_changed(self, widget):
        self.__renaming_allowed = GtkUtils.validate_entry(self.entry_name)
    
    def __on_entry_apply(self, widget):
        self.atom.rename(self.entry_name.get_text())
        self.label_name.set_text(self.atom.name)
        self.window.show_toast("Atom renamed successfully.")
        self.window.reload_atoms()

    def __notify_bind_switch(self, bind_name: str, state: bool):
        if state:
            self.window.show_toast(f"{bind_name} bound to Atom.")
        else:
            self.window.show_toast(f"{bind_name} unbound from Atom.")

    def __on_switch_bind_themes(self, _, state):
        self.atom.set_bind_themes(state)
        self.__notify_bind_switch("themes", state)

    def __on_switch_bind_icons(self, _, state):
        self.atom.set_bind_icons(state)
        self.__notify_bind_switch("icons", state)

    def __on_switch_bind_fonts(self, _, state):
        self.atom.set_bind_fonts(state)
        self.__notify_bind_switch("fonts", state)
    
    def restore_color_scheme(self, *args):
        Adw.StyleManager.get_default().set_color_scheme(self.__current_color_scheme)