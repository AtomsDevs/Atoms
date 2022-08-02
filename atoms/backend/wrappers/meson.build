pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
wrappersdir = join_paths(pkgdatadir, 'atoms/backend/wrappers')

bottles_sources = [
  '__init__.py',
  'proot.py',
]

install_data(bottles_sources, install_dir: wrappersdir)