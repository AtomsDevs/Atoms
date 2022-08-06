pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
widgetsdir = join_paths(pkgdatadir, 'atoms/frontend/widgets')

atoms_sources = [
  '__init__.py',
  'atom_entry.py',
  'creation_step_entry.py',
  'image_entry.py',
]

install_data(atoms_sources, install_dir: widgetsdir)