pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
distributionsdir = join_paths(pkgdatadir, 'atoms/backend/models/distributions')

bottles_sources = [
  '__init__.py',
  'alpinelinux.py',
  'ubuntu.py',
]

install_data(bottles_sources, install_dir: distributionsdir)