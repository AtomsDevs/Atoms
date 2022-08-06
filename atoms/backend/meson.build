pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
backenddir = join_paths(pkgdatadir, 'atoms/backend')

subdir('params')
subdir('wrappers')
subdir('exceptions')
subdir('entities')
subdir('utils')

atoms_sources = [
  '__init__.py',
  'atoms.py',
]

install_data(atoms_sources, install_dir: backenddir)