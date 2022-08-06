pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'atoms/frontend/views')

subdir('status')
subdir('lists')

atoms_sources = [
  '__init__.py',
  'dashboard.py',
  'console.py',
]

install_data(atoms_sources, install_dir: viewsdir)