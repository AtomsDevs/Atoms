pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
paramsdir = join_paths(pkgdatadir, 'atoms/backend/params')

atoms_sources = [
  '__init__.py',
  'paths.py',
]

install_data(atoms_sources, install_dir: paramsdir)