from gi.repository import Gtk, Adw

from atoms.frontend.widgets.atom_entry import AtomEntry


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/list-atoms.ui')
class AtomsList(Gtk.ScrolledWindow):
    __gtype_name__ = 'AtomsList'
    
    list_atoms = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.__build_ui()

    def __build_ui(self):
        self.list_atoms.append(AtomEntry(self.window))
