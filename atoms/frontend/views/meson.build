pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'atoms/frontend/views')

subdir('status')
subdir('lists')

bottles_sources = [
  '__init__.py',
  'dashboard.py',
]

install_data(bottles_sources, install_dir: viewsdir)