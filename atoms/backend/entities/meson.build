pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
entitiesdir = join_paths(pkgdatadir, 'atoms/backend/entities')

bottles_sources = [
  '__init__.py',
  'config.py',
  'atom.py',
]

install_data(bottles_sources, install_dir: entitiesdir)