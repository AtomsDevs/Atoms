from gi.repository import Gtk, Adw

from atoms.frontend.views.status.detached_console import AtomsStatusDetachedConsole
from atoms.frontend.windows.detached_window import AtomsDetachedWindow
from atoms.frontend.views.console import AtomsConsole


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/dashboard.ui')
class AtomDashboard(Adw.Bin):
    __gtype_name__ = 'AtomDashboard'

    btn_back = Gtk.Template.Child()
    btn_detach = Gtk.Template.Child()
    stack_atom = Gtk.Template.Child()
    stack_console = Gtk.Template.Child()
    box_console = Gtk.Template.Child()
    img_distribution = Gtk.Template.Child()
    label_name = Gtk.Template.Child()
    label_distribution = Gtk.Template.Child()

    def __init__(self, window, atom, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.atom = atom
        self.__detach_status = False
        self.__detached_window = None
        self.__build_ui()
    
    def __build_ui(self):
        self.console = AtomsConsole(self.atom)
        self.label_name.set_text(self.atom.name)
        self.label_distribution.set_text(self.atom.distribution.name)
        self.img_distribution.set_from_icon_name(self.atom.distribution.logo)
        self.stack_console.add_named(AtomsStatusDetachedConsole(), 'status')
        self.box_console.append(self.console)

        self.btn_back.connect('clicked', self.__on_back_clicked)
        self.btn_detach.connect('clicked', self.__on_detach_clicked)
        self.stack_atom.connect('notify::visible-child', self.__on_visible_child_changed)

    def __on_back_clicked(self, widget):
        self.window.main_leaflet.navigate(Adw.NavigationDirection.BACK)

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
                self.__detached_window = AtomsDetachedWindow(self.console, "#000000")
                self.__detached_window.present()
                self.__detached_window.connect("close-request", detach)
            
        self.__detach_status = not self.__detach_status
        attach() if self.__detach_status else detach()

    def __on_visible_child_changed(self, *args):
        visible_child_name = self.stack_atom.get_visible_child_name()
        self.btn_detach.set_visible(visible_child_name == 'console')
