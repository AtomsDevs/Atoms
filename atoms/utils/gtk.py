

# gtk.py
#
# Copyright 2022 brombinmirko <send@mirko.pm>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, in version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re


class GtkUtils:

    @staticmethod
    def validate_entry(entry, allow:list = None) -> bool:
        text = entry.get_text()
        esc_chars = "[@!#$%^&*()<>?/|}{~:.;,'\"]"

        if allow is not None:
            for char in allow:
                esc_chars = esc_chars.replace(char, "")

        if re.search(esc_chars, text) or len(text) == 0 or text.isspace():
            entry.add_css_class("error")
            return False
        else:
            entry.remove_css_class("error")
            return True
            