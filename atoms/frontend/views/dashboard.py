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

from atoms.frontend.views.status.detached_console import AtomsStatusDetachedConsole
from atoms.frontend.windows.detached_window import AtomsDetachedWindow
from atoms.frontend.views.console import AtomsConsole
from atoms.frontend.utils.threading import RunAsync


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/dashboard.ui')
class AtomDashboard(Adw.Bin):
    __gtype_name__ = 'AtomDashboard'

    btn_back = Gtk.Template.Child()
    btn_detach = Gtk.Template.Child()
    btn_browse = Gtk.Template.Child()
    stack_atom = Gtk.Template.Child()
    stack_console = Gtk.Template.Child()
    box_console = Gtk.Template.Child()
    img_distribution = Gtk.Template.Child()
    label_name = Gtk.Template.Child()
    label_distribution = Gtk.Template.Child()
    row_destroy = Gtk.Template.Child()

    def __init__(self, window, atom: 'Atom', **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.atom = atom
        self.__detach_status = False
        self.__detached_window = None
        self.__current_color_scheme = Adw.ColorScheme.DEFAULT
        self.__build_ui()
    
    def __build_ui(self):
        self.console = AtomsConsole(self.atom)
        self.label_name.set_text(self.atom.name)
        self.label_distribution.set_text(self.atom.distribution.name)
        self.img_distribution.set_from_icon_name(self.atom.distribution.logo)
        self.stack_console.add_named(AtomsStatusDetachedConsole(), 'status')
        self.box_console.append(self.console)

        self.row_destroy.connect('activated', self.__on_destroy_activated)
        self.btn_back.connect('clicked', self.__on_back_clicked)
        self.btn_detach.connect('clicked', self.__on_detach_clicked)
        self.btn_browse.connect('clicked', self.__on_browse_clicked)
        self.stack_atom.connect('notify::visible-child', self.__on_visible_child_changed)

    def __on_back_clicked(self, widget):
        self.window.show_atoms_list()
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

    def __on_detach_clicked(self, widget):
        def detach(*args):
            if self.__detached_window:
                self.__detached_window.release_widget()
                self.__detached_window.close()
                self.__detached_window = None
            self.btn_detach.set_tooltip_text('Detach Console')
            self.btn_detach.set_icon_name('pip-in-symbolic')
            self.stack_console.set_visible_child_name('vte')
            self.box_console.append(self.console)
            
        def attach():
            self.btn_detach.set_tooltip_text('Attach Console')
            self.btn_detach.set_icon_name('pip-out-symbolic')
            self.stack_console.set_visible_child_name('status')
            self.box_console.remove(self.console)
            if not self.__detached_window:
                self.__detached_window = AtomsDetachedWindow(self.console, "#000000", title=self.atom.name)
                self.__detached_window.present()
                self.__detached_window.connect("close-request", detach)
            
        self.__detach_status = not self.__detach_status
        attach() if self.__detach_status else detach()

    def __on_visible_child_changed(self, *args):
        visible_child_name = self.stack_atom.get_visible_child_name()
        self.btn_detach.set_visible(visible_child_name == 'console')

        if visible_child_name == "console":
            self.__current_color_scheme = Adw.ColorScheme.FORCE_DARK
        else:
            self.__current_color_scheme = Adw.ColorScheme.DEFAULT

        Adw.StyleManager.get_default().set_color_scheme(self.__current_color_scheme)

    def __on_browse_clicked(self, widget):
        Gtk.show_uri(self.window, f"file://{self.atom.fs_path}", Gdk.CURRENT_TIME)

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
    
    def restore_color_scheme(self, *args):
        Adw.StyleManager.get_default().set_color_scheme(self.__current_color_scheme)