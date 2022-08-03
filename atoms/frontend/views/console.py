from gi.repository import Gtk, Gdk, GLib, Vte, Pango


CONF_FONT = "Source Code Pro Regular 12"

class AtomsConsole(Vte.Terminal):

    def __init__(self, atom, *args, **kwds):
        super(AtomsConsole, self).__init__(*args, **kwds)  
        self.atom = atom
        self.__build_ui()
        self.run_command(["/bin/bash"])

    def __build_ui(self):
        gesture_controller = Gtk.GestureClick(button=Gdk.BUTTON_SECONDARY)
        
        self.set_halign(Gtk.Align.FILL)
        self.set_valign(Gtk.Align.FILL)
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.set_mouse_autohide(True)
        self.set_font(Pango.FontDescription(CONF_FONT))
        self.add_controller(gesture_controller)
    
    def run_command(self, command: list, environment: list=None, working_directory: str=None):
        if environment is None:
            environment = []
        if working_directory is None:
            working_directory = ""
        self.spawn_async(
            Vte.PtyFlags.DEFAULT,
            working_directory,
            command,
            environment,
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None
        )
