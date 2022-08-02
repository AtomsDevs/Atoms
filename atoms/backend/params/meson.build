pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
paramsdir = join_paths(pkgdatadir, 'atoms/backend/params')

bottles_sources = [
  '__init__.py',
  'paths.py',
]

install_data(bottles_sources, install_dir: paramsdir)