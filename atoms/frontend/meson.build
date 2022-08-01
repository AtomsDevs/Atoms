pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
frontenddir = join_paths(pkgdatadir, 'atoms/frontend')

subdir('views')
subdir('widgets')

bottles_sources = [
  '__init__.py',
  'main.py',
]

install_data(bottles_sources, install_dir: frontenddir)