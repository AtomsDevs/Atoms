pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
windowsdir = join_paths(pkgdatadir, 'atoms/windows')

atoms_sources = [
  '__init__.py',
  'detached_window.py',
  'new_atom_window.py',
  'main_window.py',
  'preferences_window.py',
]

install_data(atoms_sources, install_dir: windowsdir)