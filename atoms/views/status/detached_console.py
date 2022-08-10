from gi.repository import Gtk, Adw


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/status-detached-console.ui')
class AtomsStatusDetachedConsole(Adw.Bin):
    __gtype_name__ = 'AtomsStatusDetachedConsole'