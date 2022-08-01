from gi.repository import Gtk, Adw

from atoms.frontend.views.status.detached_console import AtomsStatusDetachedConsole

@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/dashboard.ui')
class AtomsDashboard(Adw.Bin):
    __gtype_name__ = 'AtomsDashboard'

    btn_back = Gtk.Template.Child()
    btn_detach = Gtk.Template.Child()
    stack_atom = Gtk.Template.Child()
    stack_console = Gtk.Template.Child()
    label_console = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.__detach_status = False
        self.__build_ui()

    def __build_ui(self):
        self.stack_console.add_named(AtomsStatusDetachedConsole(), 'status')
        self.btn_back.connect('clicked', self.__on_back_clicked)
        self.btn_detach.connect('clicked', self.__on_detach_clicked)
        self.stack_atom.connect('notify::visible-child', self.__on_visible_child_changed)

    def __on_back_clicked(self, widget):
        self.window.main_leaflet.navigate(Adw.NavigationDirection.BACK)

    def __on_detach_clicked(self, widget):
        self.__detach_status = not self.__detach_status
        if self.__detach_status:
            self.btn_detach.set_tooltip_text('Attach Console')
            self.btn_detach.set_icon_name('pip-out-symbolic')
            self.stack_console.set_visible_child_name('status')
        else:
            self.btn_detach.set_tooltip_text('Detach Console')
            self.btn_detach.set_icon_name('pip-in-symbolic')
            self.stack_console.set_visible_child_name('vte')

    def __on_visible_child_changed(self, *args):
        visible_child_name = self.stack_atom.get_visible_child_name()
        self.btn_detach.set_visible(visible_child_name == 'console')
