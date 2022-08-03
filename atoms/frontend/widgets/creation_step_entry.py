from gi.repository import Gtk, Gio, Adw


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/entry-creation-step.ui')
class CreationStepEntry(Adw.ActionRow):
    __gtype_name__ = 'CreationStepEntry'

    img_completed = Gtk.Template.Child()
    label_percentage = Gtk.Template.Child()
    spinner = Gtk.Template.Child()

    def __init__(self, title: str, update_func: callable = None):
        super().__init__()
        self.__title = title
        self.__update_func = update_func
        self.__build_ui()

    def __build_ui(self):
        self.set_title(self.__title)
