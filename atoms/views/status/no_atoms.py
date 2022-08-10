from gi.repository import Gtk, Adw


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/status-no-atoms.ui')
class AtomsStatusEmpty(Adw.Bin):
    __gtype_name__ = 'AtomsStatusEmpty'

    btn_new = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.__build_ui()

    def __build_ui(self):
        self.btn_new.connect('clicked', self.window.on_btn_new_clicked)
