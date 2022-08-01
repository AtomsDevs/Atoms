from gi.repository import Gtk, Gio, Adw

from atoms.frontend.views.dashboard import AtomsDashboard


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/entry-atom.ui')
class AtomEntry(Adw.ActionRow):
    __gtype_name__ = 'AtomEntry'

    btn_open = Gtk.Template.Child()
    img_distribution = Gtk.Template.Child()

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.dashboard = AtomsDashboard(window)
        self.__build_ui()

    def __build_ui(self):
        self.set_title('My First Atom')
        self.img_distribution.set_from_icon_name('alpine-linux-symbolic')
        self.window.main_leaflet.append(self.dashboard)
        
        self.btn_open.connect('clicked', self.__on_open_clicked)

    def __on_open_clicked(self, widget):
        self.window.main_leaflet.set_visible_child(self.dashboard)
