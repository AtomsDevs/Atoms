import os
from pathlib import Path


class AtomsPaths:
    xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.join(Path.home(), ".local/share"))
    app_data = os.path.join(xdg_data_home, "atoms")

    atoms = os.path.join(app_data, "atoms")
    config_file = os.path.join(app_data, "config.json")
    