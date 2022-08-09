from gi.repository import GLib

from atoms.backend.wrappers.client_bridge import ClientBridge


class GTKClientBridge(ClientBridge):

    def __init__(self):
        super().__init__("Atoms GTK", "gtk")

    def exec_on_main(self, func, *args):
        GLib.idle_add(func, *args)
        