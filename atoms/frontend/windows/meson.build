pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
windowsdir = join_paths(pkgdatadir, 'atoms/frontend/windows')

bottles_sources = [
  '__init__.py',
  'detached_window.py',
  'new_atom_window.py',
  'main_window.py',
]

install_data(bottles_sources, install_dir: windowsdir)