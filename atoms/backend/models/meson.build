pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
modelsdir = join_paths(pkgdatadir, 'atoms/backend/models')

bottles_sources = [
  '__init__.py',
  'result.py',
  'distribution.py',
]

install_data(bottles_sources, install_dir: modelsdir)