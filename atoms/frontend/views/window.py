# window.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Adw

from atoms.frontend.views.status.no_atoms import AtomsStatusEmpty
from atoms.frontend.views.lists.atoms import AtomsList


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/window.ui')
class AtomsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'AtomsWindow'

    main_leaflet = Gtk.Template.Child()
    stack_main = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__build_ui()
    
    def __build_ui(self):
        # self.stack_main.add_named(AtomsStatusEmpty(), 'noatoms')
        self.stack_main.add_named(AtomsList(self), 'listatoms')

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Atoms'
        self.props.version = "0.1.0"
        self.props.authors = ['mirkobrombin']
        self.props.copyright = '2022 mirkobrombin'
        self.props.logo_icon_name = 'pm.mirko.Atoms'
        self.props.modal = True
        self.set_transient_for(parent)
