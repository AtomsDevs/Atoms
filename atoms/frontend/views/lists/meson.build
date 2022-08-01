pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
listdir = join_paths(pkgdatadir, 'atoms/frontend/views/lists')

bottles_sources = [
  '__init__.py',
  'atoms.py',
]

install_data(bottles_sources, install_dir: listdir)