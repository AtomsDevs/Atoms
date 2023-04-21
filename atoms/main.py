# main.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
import gettext

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Vte', '3.91')

from gi.repository import Gtk, Gio, Adw

from atoms.windows.main_window import AtomsWindow
from atoms.windows.preferences_window import AtomsPreferences
from atoms.utils.translations import get_translations
from atoms.const import *


_ = get_translations()

class AtomsApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='pm.mirko.Atoms',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.close, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

        self.set_accels_for_action('win.new_atom', ['<Ctrl>n'])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = AtomsWindow(application=self)
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Atoms',
                                application_icon='pm.mirko.Atoms',
                                developer_name='Mirko Brombin',
                                license='gpl-3.0-only',
                                website='https://github.com/mirkobrombin/Atoms',
                                issue_url='https://github.com/mirkobrombin/Atoms/issues',
                                version='1.1.1',
                                developers=['Mirko Brombin https://github.com/mirkobrombin/'],
                                artists=['Allaeddine Boulefaat https://github.com/allaeddineomc'],                                
                                translator_credits= _("translator_credits"),
                                copyright='© 2023 Mirko Brombin')
        about.add_credit_section(
            _("Contributors"),
            [
                "Hari Rana (TheEvilSkeleton) https://theevilskeleton.gitlab.io/",
                "axtlos https://axtloss.github.io/"
            ]
        )
        about.add_credit_section(
            _("Third-Party Libraries and Special Thanks"),
            [
                "PRoot https://github.com/proot-me/PRoot",
                "orjson https://github.com/ijl/orjson",
                "distrobox https://github.com/89luca89/distrobox",
                "servicectl https://github.com/smaknsk/servicectl"
            ]
        )
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        preferences_window = AtomsPreferences(self.props.active_window)
        preferences_window.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
    
    def close(self, *args):
        """Close the application."""
        self.quit()


def main(version):
    """The application's entry point."""
    app = AtomsApplication()
    return app.run(sys.argv)
