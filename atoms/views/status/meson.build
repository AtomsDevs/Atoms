pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
statusdir = join_paths(pkgdatadir, 'atoms/views/status')

atoms_sources = [
  '__init__.py',
  'no_atoms.py',
  'detached_console.py',
]

install_data(atoms_sources, install_dir: statusdir)