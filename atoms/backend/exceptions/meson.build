pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
exceptionsdir = join_paths(pkgdatadir, 'atoms/backend/exceptions')

atoms_sources = [
  '__init__.py',
  'atom.py',
  'config.py',
  'exception.py',
  'distribution.py',
  'common.py',
  'image.py',
  'download.py',
]

install_data(atoms_sources, install_dir: exceptionsdir)