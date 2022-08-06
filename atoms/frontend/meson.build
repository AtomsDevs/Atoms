pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
frontenddir = join_paths(pkgdatadir, 'atoms/frontend')

subdir('views')
subdir('widgets')
subdir('windows')
subdir('utils')

atoms_sources = [
  '__init__.py',
  'main.py',
  'const.py',
]

install_data(atoms_sources, install_dir: frontenddir)