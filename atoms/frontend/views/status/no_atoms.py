from gi.repository import Gtk, Adw


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/status-no-atoms.ui')
class AtomsStatusEmpty(Adw.Bin):
    __gtype_name__ = 'AtomsStatusEmpty'