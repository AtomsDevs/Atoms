pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
utilsdir = join_paths(pkgdatadir, 'atoms/frontend/utils')

atoms_sources = [
  '__init__.py',
  'threading.py',
  'gtk.py',
]

install_data(atoms_sources, install_dir: utilsdir)