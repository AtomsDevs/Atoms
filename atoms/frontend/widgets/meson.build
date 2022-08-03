pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
widgetsdir = join_paths(pkgdatadir, 'atoms/frontend/widgets')

bottles_sources = [
  '__init__.py',
  'atom_entry.py',
  'creation_step_entry.py',
]

install_data(bottles_sources, install_dir: widgetsdir)